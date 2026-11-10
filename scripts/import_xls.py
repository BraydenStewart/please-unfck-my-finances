"""Convert a bank AccountHistory .xls (Account Number, Post Date, Check, Description, Debit, Credit, Status, Balance)
into the ledger CSV schema: date,account,description,amount,category. Usage: import_xls.py in.xls out.csv"""
import csv, sys, xlrd

src, dst = sys.argv[1:3]
wb = xlrd.open_workbook(src)
s = wb.sheet_by_index(0)
hdr = [str(c.value).strip() for c in s.row(0)]
ix = {h: i for i, h in enumerate(hdr)}
n = skipped = 0
with open(dst, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["date", "account", "description", "amount", "category"])
    for r in range(1, s.nrows):
        row = s.row_values(r)
        if str(row[ix["Status"]]).strip().lower() != "posted":
            skipped += 1; continue
        d = xlrd.xldate_as_datetime(row[ix["Post Date"]], wb.datemode).date().isoformat()
        deb, cre = row[ix["Debit"]], row[ix["Credit"]]
        amt = (float(cre) if cre != "" else 0.0) - (float(deb) if deb != "" else 0.0)
        w.writerow([d, row[ix["Account Number"]], " ".join(str(row[ix["Description"]]).split()), f"{amt:.2f}", ""])
        n += 1
print(f"wrote {n} rows to {dst}, skipped {skipped} non-posted")
