# Contributing to please-unfck-my-finances

Thanks for being here. Most of what makes this useful is small, specific knowledge: what a bank's
export looks like, what a merchant string really is, which fee is negotiable. Adding one more piece
of that is a real contribution, and it is usually a ten-line PR.

## The one rule

**The agent never touches money and never invents a number.**

Rejected on sight, regardless of quality:
- Anything that logs into a bank, card, loan or brokerage site, or stores a credential.
- Anything that pays, transfers, cancels, disputes or opens/closes an account.
- Anything that fills a gap with a guess instead of asking or marking it `ASSUMED`.
- Specific investment picks, tax-filing positions, or legal conclusions.

## Good first contributions

**Merchant rules** (`config/categories.example.json`). A merchant string that lands in the wrong
category or in `uncategorized`. Add the regex to the right rule. Keep it generic: chains and
services, never a person's name, employer or account number.

**Importers** (`scripts/`). Your bank exports a format the agent struggles with. Write a small
script that converts it to `date,account,description,amount,category`, like `import_xls.py`.

**Spec and docs** (`config/spec.md`, `README.md`). If a step confused you, it confuses everyone.
Fix the sentence.

## What not to send

- Personal data. Yours or anyone's. No real statements, reports, profiles or merchant strings that
  identify a person.
- A rewrite of `CLAUDE.md` or `config/spec.md` into a different structure. Add to them.
- Heavy dependencies. Python 3 plus `xlrd`/`openpyxl` is the ceiling.

## Before you open a PR

```bash
# 1. Nothing personal is staged. This must print nothing.
git ls-files | grep -Ev '\.example\.|README|spec|\.gitkeep' | grep -E 'config/|data/|reports/|state/|logs/'

# 2. Shell still parses.
bash -n run.sh

# 3. Config templates still parse.
for f in config/*.example.json; do python3 -m json.tool "$f" > /dev/null; done
```

## Style

- Prose: concise, specific, no marketing words. Say what the numbers say, then the next step.
- Never shame the user in anything the agent writes.
- Commits: one change per commit, present tense.

## Reporting a problem

Open an issue with the bank or card, the export format, what the agent did, and what you expected.
Never paste real transactions, balances or account numbers. Make up a row with the same shape.
