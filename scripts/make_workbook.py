"""Build templates/finances.xlsx: one sheet per thing the agent needs. Re-run to regenerate."""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

SHEETS = {
    "Income": ["source", "type (w2/1099/other)", "gross_monthly", "net_per_paycheck", "pay_frequency", "next_payday"],
    "Bills": ["name", "amount", "due_day", "autopay (Y/N)", "account", "can_cancel (Y/N)"],
    "Debts": ["name", "balance", "apr_percent", "min_payment", "due_day", "in_collections (Y/N)"],
    "Accounts": ["name", "kind", "institution", "last4", "current_balance", "as_of"],
    "Transactions": ["date", "account", "description", "amount (+in / -out)", "category"],
    "Goals": ["name", "target_amount", "target_date", "saved_so_far"],
}
wb = Workbook(); wb.remove(wb.active)
for name, cols in SHEETS.items():
    ws = wb.create_sheet(name); ws.append(cols); ws.freeze_panes = "A2"
    for i, c in enumerate(ws[1], 1):
        c.font = Font(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor="1F3A5F")
        ws.column_dimensions[get_column_letter(i)].width = max(16, len(c.value) + 4)
wb.save("templates/finances.xlsx")
