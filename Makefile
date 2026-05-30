.PHONY: audit shellcheck

audit:
	python3 scripts/audit_brain.py

shellcheck:
	shellcheck .claude/hooks/*.sh run_agent.sh.example
