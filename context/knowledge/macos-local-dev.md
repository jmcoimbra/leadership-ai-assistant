# macOS Local Dev (Apple Silicon + Tahoe)

**Added:** 2026-05-20
**Last Updated:** 2026-05-21 (Intel Homebrew uninstall cascade pattern + Python.framework stub launcher location)
**Source:** 2026-05-20 Conductor "Python library will stop working" warning investigation. Root cause: Intel Homebrew at `/usr/local/Cellar` forcing 8 child processes under Rosetta 2; Conductor attributed as parent.
**Pillar:** Pillar 4 (AI Execution)

## Rosetta 2 deprecation diagnostic recipe

`system_profiler SPLegacySoftwareDataType` is the canonical source for "what is running under Rosetta on this Mac and which app is the responsible parent."

```bash
system_profiler SPLegacySoftwareDataType
```

The output is a tree under `Rosetta Software:`. Each leaf names the x86_64 binary; each parent name is the **Responsible App** (the macOS-attributed launcher). Use this to triage OS-level "this app uses a library that will stop working" warnings before opening upstream issues against the named app.

Filter for a specific app:

```bash
system_profiler SPLegacySoftwareDataType | awk '/Rosetta Software:/,/^$/' | grep -B1 -A4 "Responsible App: <AppName>"
```

Expected after a clean arm64 migration: no output.

## Misattributed-parent pattern (Tauri / Electron / shell-launching apps)

A Tauri or Electron app can be 100% arm64-native (verify with `file -b /Applications/<App>/Contents/MacOS/<binary>`) yet still show up as Responsible App for x86_64 children. macOS attributes child Rosetta launches to the user-launched parent, not to the actual offender. The fix lives in the user's PATH, not in the app.

Confirmed source paths to inspect when triaging:
- `/usr/local/Cellar/*` (Intel Homebrew)
- `/opt/homebrew/Cellar/*` (Apple Silicon Homebrew)
- `~/.asdf/installs/*` (asdf-managed runtimes)
- `~/.local/bin`, `~/.qlty/bin`, `/usr/local/opt/*` (PATH-side directories)

## asdf reshim does NOT change interpreter architecture

`asdf reshim` updates the shim dispatch scripts only. The interpreter binary at `~/.asdf/installs/<plugin>/<version>/bin/<binary>` keeps whatever architecture it was built for.

To migrate an asdf-managed runtime from x86_64 to arm64, full uninstall + reinstall under an arm64 shell is mandatory:

```bash
arch -arm64 zsh -ilc 'asdf uninstall <plugin> <version> && asdf install <plugin> <version>'
file -b "$(arch -arm64 zsh -ilc "asdf which <binary>")"  # confirm arm64
```

Affected plugins: python (compiles from source, 5-10 min), ruby (compiles from source, 5-10 min), nodejs (prebuilt binary, ~30s), java (prebuilt binary, ~30s). Compiled-from-source plugins require build deps already present on arm64 Homebrew (openssl@3, readline, libyaml, gmp, etc.).

Verification one-liner:

```bash
arch -arm64 zsh -ilc 'for t in git gh asdf bash python3 ruby node java; do real=$(asdf which "$t" 2>/dev/null) || real=$(which "$t" 2>/dev/null); [ -n "$real" ] && printf "%-10s %s  %s\n" "$t" "$(file -b "$real" | grep -oE "arm64|x86_64" | head -1)" "$real"; done'
```

## System Information "Kind" column is an inference, not authoritative

`/Applications/<App>/Contents/Info.plist` is the canonical source for app type. System Information's Kind column ("iOS", "Universal", "Intel") is a derived classification and can mislead.

Specifically: a Tauri Mac app with `CFBundlePackageType: APPL`, `LSMinimumSystemVersion: 10.13`, no `LSRequiresIPhoneOS` can still appear as **Kind: iOS** in System Information. The Kind value does NOT mean the app is a Designed-for-iPad / Catalyst app.

Verify type before acting:

```bash
plutil -p /Applications/<App>/Contents/Info.plist | head -30
```

Look for `CFBundlePackageType`, `LSMinimumSystemVersion`, `LSRequiresIPhoneOS`, `LSApplicationCategoryType`.

## Tauri app bundle inspection (find embedded dependencies)

Tauri apps ship the front-end `package.json` embedded as a string blob inside the main binary. To enumerate JS/agent dependencies without unpacking the app:

```bash
strings /Applications/<TauriApp>/Contents/Resources/bin/<runtime-binary> | grep -E "version|agentBinaries|dependencies"
```

Confirmed pattern for Conductor 0.54.0: embedded `package.json` revealed `agentBinaries: {claudeCode, codex, githubCli, ripgrep}` versions and full React/Radix/Tauri dependency tree.

Use this when a Tauri app's GitHub releases repo is minimal (release-tarball only, no source) and you need to see what it actually bundles.

## Intel Homebrew uninstall cascade pattern

`brew uninstall --ignore-dependencies <formula>` triggers an autoremove pass that drops every formula whose only reverse-dependency was the one just uninstalled. Useful when the goal is a directed sweep of one runtime + its now-orphan toolchain.

Confirmed 2026-05-21: removing Intel `python@3.12 python@3.13 python@3.14` from `/usr/local/Cellar` auto-removed 45 orphaned deps: aom, aribb24, cjson, flac, frei0r, fribidi, highway, imath, jpeg-xl, leptonica, libarchive, libass, libb2, libbluray, libdeflate, libmicrohttpd, libogg, librist, libsamplerate, libsndfile, libsodium, libsoxr, libssh, libudfread, libunibreak, libvidstab, libvmaf, libvorbis, mbedtls, mpg123, opencore-amr, openexr, openjph, pango, rav1e, rubberband, snappy, speex, srt, tesseract, theora, webp, xvid, zeromq, zimg. Intel Cellar dropped 171 → 123 in one command.

Pre-flight: confirm no other installed formula depends on the target:

```bash
arch -x86_64 /usr/local/bin/brew uses --installed <formula1> <formula2> ...
```

Empty output = safe to uninstall. Anything listed = will be left dangling.

## Python.framework stub launcher location

`Python.app` inside `<prefix>/Frameworks/Python.framework/Versions/<X.Y>/Resources/Python.app` is the macOS GUI launcher stub that Tkinter / matplotlib / py2app rely on. It is NOT a separate Python install. When users navigate to it in Finder ("what is this Python.app?"), the answer is: the framework build's GUI entry point.

To identify which Python install owns it:

```bash
ls -la /usr/local/Frameworks/Python.framework/Versions/    # Intel Homebrew Pythons
ls -la /opt/homebrew/Frameworks/Python.framework/Versions/ # arm64 Homebrew Pythons
ls -la /Library/Frameworks/Python.framework/Versions/      # python.org installer Pythons
```

Each `<X.Y>` is a symlink to the actual Cellar (Homebrew) or `/Library/Frameworks` location, which reveals whether the install is x86_64 or arm64.

## Cross-References

| File | Connection |
|------|-----------|
| `12_projects/rosetta_intel_homebrew_migration.md` | Personal migration from Intel Homebrew to arm64 Homebrew, full Phase A/B/C plan |
| `context/knowledge/react-native.md` | [Mobile Team]-owned ios-deploy will reinstall under arm64 Homebrew in Phase B |
| `context/knowledge/conductor.md` | Conductor app internals, sub-agent MCP access, workspace lifecycle |
