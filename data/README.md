# data/

Everything here is untracked except this file.

Drop exports into `statements/`: bank/card CSVs, OFX/QFX, PDF statements, loan statements, pay stubs.
Download them yourself from each institution. The agent never logs in anywhere.
## Fill-in files
- `finances.xlsx`: fill in Income, Bills, Debts, Accounts, Goals (Transactions optional). The agent reads it instead of asking.
- `statements/*.csv`: real exports from your bank/cards. Needs `date,account,description,amount,category` (category may be blank). `example-transactions.csv` is a sample; delete it before the first real run.

Blank copies live in `templates/` (tracked).
