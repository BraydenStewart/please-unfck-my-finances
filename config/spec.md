# Run contract

## Hard rules
1. **Read-only.** Never log into a bank, broker or card site. Never move, send, pay or transfer money.
   Never open, close or change an account. Work only from files the user placed in `data/statements/`
   and facts in `config/profile.json`.
2. **Never invent a number.** Every figure in a report cites its source file and row range, or is
   marked `ASSUMED` with the assumption stated. If statements are missing, say which and stop short.
3. **No credentials.** Never ask for, store, echo or write a password, full account number, SSN or
   card number. If one appears in a statement, redact it (keep last 4) in everything you write.
4. **No advice that needs a license.** Budgeting, debt ordering and cash-flow math are in scope.
   Specific securities, tax filings positions and legal questions: lay out the tradeoffs, name what a
   CPA / fiduciary would decide, and do not decide for them.
5. **Don't shame.** State what the numbers say, then the smallest next action.

## Per-run procedure
1. Read `config/settings.json`, `config/profile.json`, `state/status.md` (if present).
2. Inventory `data/statements/`; list new files since last run. Parse CSV/PDF/OFX into one ledger
   (`state/ledger.csv`: date, account, description, amount, category, source_file).
3. Dedupe against the existing ledger by (date, account, amount, description).
4. Categorize. Anything ambiguous goes to `reports/questions.md`, not a guess.
5. Compute: income vs spend by month, savings rate, recurring charges (and new ones), fees and
   interest paid, debt payoff order per `analysis.debt_strategy`, emergency-fund runway.
6. Write `reports/YYYY-MM-DD.md` (format below) and append one line to `logs/runs.md`.
7. Update `state/status.md` with what was processed and what is still blocked.

## Report format
- **Where you stand**: net monthly cash flow, savings rate, runway in months.
- **What's bleeding**: fees, interest, unused subscriptions, with amounts and sources.
- **Do this week** (max 3 actions, each under 30 minutes).
- **Debt plan**: order, minimums, extra-payment target.
- **Questions for you**: ambiguous items.
- **Assumptions**: every `ASSUMED` figure.