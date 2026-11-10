<div align="center">

# please unf*ck my finances

**An agent that reads your bank statements and tells you, plainly, where the money is going.**

[![License: MIT](https://img.shields.io/badge/License-MIT-black.svg)](LICENSE)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-black.svg)](CONTRIBUTING.md)
[![Runs on Claude Code](https://img.shields.io/badge/runs%20on-Claude%20Code-black.svg)](https://claude.com/claude-code)
[![Read-only](https://img.shields.io/badge/money%20moved-never-black.svg)](#what-it-will-never-do)
[![macOS | Linux | WSL](https://img.shields.io/badge/macOS-%7C%20Linux%20%7C%20WSL-black.svg)](#quick-start)

You export your statements, drop them in a folder, and have one conversation. It builds a single
ledger across every account, finds the fees, the interest, the subscriptions you forgot about and
the habits that quietly cost you, puts your debts in order, and writes a short list of things to do
this week. It drafts the cancellation emails and fee-waiver requests too. You send them.

It never logs in anywhere, never moves a dollar, and never invents a number.

</div>

---

## Quick start

**You need:** [Claude Code](https://claude.com/claude-code) signed in · statement exports from your
bank and cards (CSV, XLS, OFX or PDF) · Python 3 for the helper scripts (`pip install xlrd openpyxl`).

```bash
git clone https://github.com/BraydenStewart/please-unfck-my-finances.git
cd please-unfck-my-finances
```

**1. Export your statements.** Log into each bank, card and loan site yourself and download the
last 3 months (12 is better) of transactions. Put every file in `data/statements/`. Checking,
savings, every credit card, every loan.

**2. Open the folder in Claude Code and say *"set me up"*.** Setup is one conversation:

1. It reads your statements and pulls out your accounts, income and recurring bills.
2. It shows you every value it found so you can correct what's wrong.
3. It asks **one list** of the questions statements can't answer, all at once: each debt's
   balance, APR and minimum, your next payday, your goals. Skip anything and it leaves it blank
   rather than guessing.
4. It runs the first review with you watching and stops.

<details>
<summary>Prefer filling in a spreadsheet?</summary>

Copy `templates/finances.xlsx` to `data/finances.xlsx` and fill in the Income, Bills, Debts,
Accounts and Goals sheets. Setup reads it first and only asks about what you left blank.

</details>

**Later runs:**

```bash
./run.sh          # one review run, headless, using your config
```

Or open the folder in Claude Code and ask for a monthly review. Drop fresh exports into
`data/statements/` first; it dedupes against what it has already seen.

---

## What you get

One dated report in `reports/`, in the same shape every time:

| Section | What's in it |
|---|---|
| **Where you stand** | Net monthly cash flow, savings rate, emergency-fund runway in months. |
| **What's bleeding** | Fees, interest, late charges, subscriptions, with amounts and the file they came from. |
| **Do this week** | At most 3 actions, each under 30 minutes. |
| **Debt plan** | Payoff order (avalanche or snowball), minimums, where extra money should go. |
| **Questions for you** | Anything ambiguous. It asks instead of guessing. |
| **Assumptions** | Every figure it couldn't source, marked `ASSUMED`. |

Plus ready-to-send drafts when it finds something worth fighting: a gym cancellation, a
subscription you don't use, a request to refund an annual fee or late fees.

## What you give it

| File | What goes in it | Where it comes from |
|---|---|---|
| `data/statements/*` | Your raw exports. | you download them |
| `config/profile.json` | Income, accounts (last 4 only), debts, fixed bills, goals. | drafted from your statements, then you correct it |
| `config/settings.json` | Lookback window, debt strategy, what counts as a large transaction. | defaults, edit if you want |
| `config/categories.json` | Merchant rules: which descriptions are groceries, gambling, BNPL, subscriptions. | copied from the example, add your own |

Each has a `.example` twin showing what belongs there. Your real files are gitignored, so nothing
about you leaves your machine.

<details>
<summary><b>Settings</b></summary>

| Key | Does what |
|---|---|
| `analysis.months_lookback` | How far back each review looks. Default 3. |
| `analysis.debt_strategy` | `avalanche` (highest APR first, cheapest) or `snowball` (smallest balance first, most motivating). |
| `analysis.large_transaction_usd` | Anything above this gets called out. Default 250. |
| `analysis.flag_new_recurring_charges` | Flag a charge the first time it looks like a subscription. |
| `analysis.flag_fees_and_interest` | Itemize every fee and interest charge. |
| `run.dry_run` | Forbids writing anything outside `reports/`, `state/` and `logs/`. On by default. |
| `privacy.redact_account_numbers_in_reports` | Last 4 only, everywhere it writes. |

</details>

## What it will never do

- Log into a bank, card or loan site, or ask for a password, SSN or full card number.
- Pay, transfer, cancel or dispute anything. It drafts the email; you send it.
- Present a guess as a fact. Every number cites its source file or is marked `ASSUMED`.
- Give advice that needs a license. Budgeting, debt order and cash-flow math are in scope. Picking
  investments, tax positions and legal calls get the tradeoffs laid out and handed to a pro.
- Shame you. It says what the numbers say, then the smallest next step.

`.claude/hooks/block-secret-read.sh` also stops the agent's shell from reading your keychain,
clipboard, password manager or SSH keys, as a guardrail.

## Why this instead of a budgeting app

Budgeting apps want your bank login, sell you a subscription, and show you pie charts. Most people
who are underwater don't need a pie chart. They need someone to look at a year of transactions and
say "you paid $165 in late fees, turn on autopay," "this gym is still charging you," and "this card
at 27% is the one to kill first."

This does that, from files you downloaded yourself, on your own machine.

<details>
<summary><b>Repo layout</b></summary>

```
please-unfck-my-finances/
├── CLAUDE.md                 # agent entry point: onboarding + every-run rules
├── run.sh                    # one bounded review run
├── config/
│   ├── spec.md               # the run contract: hard rules, procedure, report format
│   ├── profile.json          # your accounts, debts, bills, goals   (yours, gitignored)
│   ├── settings.json         # run knobs                             (yours, gitignored)
│   └── categories.json       # merchant -> category rules            (yours, gitignored)
├── data/
│   ├── statements/           # your exports                          (yours, gitignored)
│   └── finances.xlsx         # optional fill-in workbook             (yours, gitignored)
├── reports/                  # dated reports + drafts                (yours, gitignored)
├── state/                    # ledger + memory between runs          (yours, gitignored)
├── logs/                     # run history                           (yours, gitignored)
├── templates/                # blank workbook + sample CSV
└── scripts/
    ├── import_xls.py         # bank AccountHistory .xls -> ledger CSV
    ├── categorize.py         # apply categories.json to a ledger CSV
    └── make_workbook.py      # regenerate templates/finances.xlsx
```

</details>

<details>
<summary><b>FAQ</b></summary>

**Is my data sent anywhere?** Your statements are read by Claude through your own Claude Code
session, the same as any file you open with it. Nothing is uploaded to this repo, a server, or a
third party. Every personal path is gitignored.

**My bank's export format isn't recognized.** Claude reads most CSVs and PDFs directly. If yours
is odd, say so in the conversation, or contribute an importer (see CONTRIBUTING.md).

**How many months should I export?** Three is the minimum. Twelve catches annual fees and
subscriptions that only bill once a year.

**Does it work outside the US?** The math does. The defaults and merchant rules are US-flavored;
set `country` in your profile and add your own merchants to `categories.json`.

**What does a run cost?** It runs on your Claude Code subscription. No extra service, no fee.

</details>

## Contributing

Yes please. Merchant rules, importers for more bank export formats, and clearer docs are the most
useful. See [CONTRIBUTING.md](CONTRIBUTING.md).

One rule above all: **the agent never touches money and never invents a number.** A PR that lets
it log in, move funds, or present a guess as a fact gets closed.

## Credits

Built on the [`please-hire-me`](https://github.com/alecswang/please-hire-me) scaffold by Alex Wang (MIT).

## License

MIT. See [LICENSE](LICENSE).
