.PHONY: audit shellcheck test

audit:
	python3 scripts/audit_brain.py

test:
	python3 -m unittest discover -s tests

shellcheck:
	shellcheck .claude/hooks/*.sh run_agent.sh.example
