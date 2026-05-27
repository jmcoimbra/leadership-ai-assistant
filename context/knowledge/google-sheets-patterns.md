# Google Sheets Patterns

Owner: [Brain Owner]
Pillar: Pillar 4 (AI Execution)
Last Updated: 2026-04-11

## pt_BR Locale Formula Bug

### The Problem
Google Sheets Apps Script `setFormula()` does NOT auto-translate function names for pt_BR locale spreadsheets, despite documentation claiming otherwise.

- `setFormula('=IF(A1>0,"yes","no")')` → `#ERROR!` (commas interpreted as decimal separators)
- `setFormula('=SE(A1>0;"sim";"não")')` → `#NAME?` (PT-BR function name not recognized by engine)
- English functions with `;` separators → `#ERROR!` or `#NAME?` depending on function

### The Fix
Never use `setFormula()` for formulas in pt_BR spreadsheets. Use MCP `write_formula` tool instead.

### MCP `write_formula` Translation Table

The MCP tool internally translates PT-BR → English, but NOT all functions:

| PT-BR (use this) | Internal (stored) | Status |
|---|---|---|
| `SE()` | `IF()` | Translated |
| `SOMA()` | `SUM()` | Translated |
| `MAIOR()` | `LARGE()` | Translated |
| `SOMARPRODUTO()` | `SUMPRODUCT()` | Translated |
| `CONT.VALORES()` | `COUNTA()` | Translated |
| `CONT.SE()` | `COUNTIF()` | Translated |
| `CORRESP()` | `MATCH()` | Translated |
| `SOMASES()` | `SUMIFS()` | Translated |
| `CONT.SES()` | `COUNTIFS()` | Translated |
| `SEERRO()` | `IFERROR()` | Translated |
| `E()` | `AND()` | Translated |
| `SEQUÊNCIA()` | ❌ NOT translated | Breaks with `#NAME?` |
| `FILTRO()` | ❌ NOT translated | Breaks with `#NAME?` |
| `MÁXIMOSES()` | ❌ NOT translated | Breaks with `#NAME?` |
| `MÍNIMOSES()` | ❌ NOT translated | Breaks with `#NAME?` |

**Workaround for untranslated functions:** Expand manually. Instead of `SOMARPRODUTO(MAIOR(range;SEQUÊNCIA(10)))`, write 10 individual `MAIOR(range;1)+MAIOR(range;2)+...+MAIOR(range;10)`.

### Safe Apps Script Operations
- `setNumberFormat()` — works fine, no locale issues
- `setValues()` — works fine for static data
- `deleteRow()` / `insertRow()` — works fine
- `getRange().getValue()` — works fine

### Unsafe Apps Script Operations
- `setValue("=== text ===")` — leading `=` makes Sheets interpret as formula → `#ERROR!`. Prefix with `'` or use a different marker character.
- Bulk row iteration without structural row filtering — always exclude rows matching Subtotal/TOTAL/header patterns when updating data columns.

### Separator Rules
Always use `;` as argument separator in PT-BR formulas. Commas are decimal separators.

### Currency Formatting (Apps Script)
- BRL: `setNumberFormat('R$ #,##0.00')`
- USD: `setNumberFormat('[$$]#,##0.00')`
- Percentage: `setNumberFormat('0.00%')` or `setNumberFormat('0.0%')`

**Common mistake:** `R$ #.##0,00` (pt_BR display convention) does NOT work. `setNumberFormat` uses ICU/Java DecimalFormat patterns where `.` = decimal and `,` = grouping, regardless of spreadsheet locale.

### `generate_apps_script` Limitation
The MCP `generate_apps_script` tool returns generic templates, not production code. Write scripts manually based on known sheet structure.

## Data Consolidation Pattern

When consolidating multiple spreadsheets into one (zero IMPORTRANGE):
1. Read source data via Apps Script `getValues()`
2. Map columns to unified schema (add Corretora, Moeda columns)
3. Write via `setValues()` (safe, no locale issues)
4. Apply formatting via `setNumberFormat()` (safe)
5. Write formulas ONLY via MCP `write_formula` tool (never `setFormula()`)

## Tesouro Direto API
- Old endpoint `tesourodireto.com.br/json/.../treasurybondsinfo.json` returns 410 Gone (discontinued)
- Working alternative: `api.radaropcoes.com/bonds/{encoded_name}` → `unitaryRedemptionValue` (PU de Venda)
- Name normalization required: "Sellic" → "Selic" in some API responses

## GOOGLEFINANCE Ticker Prefixes
- Brazilian stocks/FIIs: `BVMF:TICKER` (e.g., `BVMF:BBAS3`)
- International: bare symbol (e.g., `SPY`, `AAPL`)
- UCITS ETFs (European-listed): `LON:TICKER` (e.g., `LON:EWSX`, `LON:IUUS`)

## GOOGLEFINANCE Dynamic Name Lookup

Use `"name"` attribute to pull fund/stock name dynamically from ticker:
```
=IFERROR(GOOGLEFINANCE(A2;"name");IFERROR(GOOGLEFINANCE("LON:"&A2;"name");""))
```
Tries US ticker first, falls back to LON: prefix for UCITS. Sector is NOT available via GOOGLEFINANCE — keep manual.

## write_formula JSON Format

The `formulas` parameter requires a strict 2D array. Each inner element must be a single-element array:
- Correct: `[["=SUM(A1:A5)"], ["=SUM(B1:B5)"]]`
- Wrong: `["=SUM(A1:A5)", "=SUM(B1:B5)"]` → `formulas.flat is not a function`

For multi-row single-column writes, each row is `["=formula"]` wrapped in the outer array.

## Exchange Rate
`=CHOOSEROWS(CHOOSECOLS(IMPORTHTML("https://www.melhorcambio.com/dolar-hoje";"table";2);2);4)` for BRL/USD live rate

## Text Date Conversion

`setValues()` preserves source cell format. If source dates are text ("dd/mm/yyyy"), they remain text in the destination. GOOGLEFINANCE date comparisons (HOJ()-365) fail silently against text dates (CONT.SES returns 0).

Fix: Apps Script function to convert text dates to Date objects:
```javascript
function corrigirDatas() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Transações');
  var range = sheet.getRange('A2:A' + sheet.getLastRow());
  var values = range.getValues();
  values.forEach(function(row) {
    if (typeof row[0] === 'string' && row[0].match(/^\d{2}\/\d{2}\/\d{4}$/)) {
      var parts = row[0].split('/');
      row[0] = new Date(parts[2], parts[1] - 1, parts[0]);
    }
  });
  range.setValues(values);
}
```

## FII Annualized Metrics Pattern

FIIs pay monthly proventos. Use payment count from Transações as month proxy for annualized DY:

- **Total Proventos:** `=SOMASES(Transações!H:H;Transações!C:C;A2;Transações!D:D;"Dividendo")+SOMASES(...;"JCP")+SOMASES(...;"Provento")`
- **Meses:** `=CONT.SES(Transações!C:C;A2;Transações!D:D;"Dividendo")+CONT.SES(...;"JCP")+CONT.SES(...;"Provento")`
- **Média Mensal:** `=Total/Meses`
- **DY Anualizado:** `=Média*12/ValorBolsaAtual`
- **Yield on Cost:** `=TotalProventos/ValorInvestido`

Three dividend types (Dividendo, JCP, Provento) must be summed explicitly for tax reporting accuracy.

## Formula Literal Decimal Separator

In pt_BR locale, formula literals must use comma as decimal separator:
- `=98,66` → 98.66 (correct)
- `=98.66` → `#ERROR! (Formula parse error.)` (period not valid)
- `=18` → 18 (integers work fine, no separator needed)

This applies to `write_formula` when writing numeric constants as formulas.

## append_rows USER_ENTERED Date Parsing Trap

In pt_BR locale, `append_rows` with `value_input_option: USER_ENTERED` parses decimal numbers as dates when format matches dd.mm or dd/mm:
- "16.04" → date serial 46128 (April 16) instead of number 16.04
- "98.66" → text (no valid date match, but not a number either)
- "18.00" → might parse as time 18:00

**Fix:** Use `write_formula` with `=16,04` after appending rows, or use `value_input_option: RAW` (but RAW won't parse dates when you need them). Best practice: append with USER_ENTERED, then overwrite decimal columns via `write_formula` with `=value` using comma separator.

## SUMIFS Floating Point with Fractional Shares

When fractional share quantities (e.g., 14.9301) are bought and sold for the same amount, `SUMIFS(Compra) - SUMIFS(Venda)` may return a tiny positive number (e.g., 1.77e-15) instead of exactly 0. This causes downstream formulas (Valor Médio = Investido/Quantidade) to produce huge nonsensical values.

**Fix:** Wrap quantity calculation with ROUND:
```
=IF(ROUND(SUMIFS(...Compra)-SUMIFS(...Venda);6)>0; ROUND(...;6); 0)
```
6 decimal places preserves fractional share precision while eliminating float noise.

## MCP Tool Limitations (verified 2026-05-19)

### `write_range`: 10-row hard cap

Single `write_range` call accepts at most 10 rows. Larger payloads fail with: `Exceeds 10 row limit (N rows provided)`. This is a tool-side guardrail, NOT a Google Sheets API limit.

**Workaround:** batch into 10-row chunks. For a 75-row dataset, dispatch 8 sequential `write_range` calls with adjacent ranges (`Sheet1!A1:O10`, `Sheet1!A11:O20`, ...). Token cost is linear; latency is bounded by sequential I/O.

For a single large dataset, prefer `append_rows` (same 10-row cap, but no range arithmetic) or generate an Apps Script that bulk-writes via `setValues()` (no cap, runs in-Sheet).

### Office `.xlsx` files unreadable

`get_sheet_structure` and downstream read tools error on Office-format files with: `This operation is not supported for this document. The document must not be an Office file.`

Affected: files uploaded as `.xlsx` (e.g., from Excel, Riveron-authored compliance trackers). Native Google Sheets (mimeType `application/vnd.google-apps.spreadsheet`) work.

**Workarounds:**
- Open the file in Google Sheets and "Save as Google Sheets" before reading.
- For Office files in `read_file` (Drive MCP), expect base64 binary back; not usable for content extraction.
- Ask vendors that author compliance trackers (Riveron) to deliver native Google Sheets rather than `.xlsx`.

### No tool to add or rename tabs

`create_sheet` creates a new workbook (one default `Sheet1` tab). No MCP tool exposes "add tab to existing workbook" or "rename Sheet1". The Apps Script generator returns generic templates only.

**Workaround for multi-tab spec compliance:** stack sections in a single `Sheet1` separated by section-divider rows. Format:

```
Row N:    SECTION 1: <name> | (empty cells)
Row N+1:  column headers
Rows...:  data
Row M:    (empty)
Row M+1:  SECTION 2: <name>
Row M+2:  column headers
Rows...:  data
```

Once the structural review pass clears, hand off to user with a generated Apps Script that splits sections into proper tabs. Do not block v1 delivery on the tab split.

### No tool to move Drive files to a folder

`create_sheet` lands the workbook at the user's My Drive root. There is no `move_file` MCP tool. `copy_file` accepts a `parentId` and creates a copy in the target folder, but that bifurcates the file ID (Sheet edits now require tracking two IDs).

**Workaround:** create the Sheet, populate it, then surface the user-facing manual step: "Drag the Sheet into `<target folder>` in Drive." Do not attempt a copy-and-delete; the original retains all edits during the work.

### No tool to share Drive files

No MCP tool exposes "set permissions" or "share with email". Same handoff: surface the manual step.

### Verified 2026-05-19, CDE System Inventory 12.5.1 drafting session.
