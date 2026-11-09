import csv
import io
import re

def main(csv_text) -> dict:
    text = "\n".join(csv_text) if isinstance(csv_text, list) else csv_text
    if not text or not text.strip():
        return {"summary": "No data"}
    if text.lstrip().startswith("|"):
        rows = []
        for l in text.split("\n"):
            l = l.strip()
            if not l or set(l.replace("|", "").strip()) <= set("-: "):
                continue
            rows.append([c.strip() for c in l.strip("|").split("|")])
    else:
        rows = list(csv.reader(io.StringIO(text)))
    header, data = rows[0], rows[1:]

    def num(v):
        try:
            return float(re.sub(r"[^0-9.\-]", "", v))
        except Exception:
            return None

    num_cols = []
    for i, h in enumerate(header):
        if "id" in h.lower():
            continue
        vals = [num(r[i]) for r in data if len(r) > i and r[i].strip()]
        if vals and all(v is not None for v in vals):
            num_cols.append(i)

    cat_cols = []
    for i, h in enumerate(header):
        if i in num_cols:
            continue
        uniq = set(r[i] for r in data if len(r) > i)
        if "date" in h.lower() or 1 < len(uniq) <= 50:
            cat_cols.append(i)

    lines = [f"Rows: {len(data)}", f"Columns: {', '.join(header)}"]
    for n in num_cols:
        vals = [num(r[n]) for r in data if len(r) > n and num(r[n]) is not None]
        if vals:
            s = sum(vals)
            lines.append(f"{header[n]} overall: sum={s:g}, avg={s/len(vals):.2f}, "
                         f"min={min(vals):g}, max={max(vals):g}, count={len(vals)}")
    for c in cat_cols:
        for n in num_cols:
            groups = {}
            for r in data:
                if len(r) > max(c, n):
                    v = num(r[n])
                    if v is not None:
                        groups.setdefault(r[c], []).append(v)
            if groups:
                lines.append(f"{header[n]} by {header[c]} (sum; avg; count): " +
                             "; ".join(f"{k}={sum(v):g}; {sum(v)/len(v):.2f}; {len(v)}"
                                       for k, v in groups.items()))

    def col(name):
        for i, h in enumerate(header):
            if h.strip().lower() == name.lower():
                return i
        return None

    io_, iq, ip, it = col("OrderID"), col("Quantity"), col("UnitPrice"), col("TotalSales")
    if None not in (io_, iq, ip, it):
        bad = []
        for r in data:
            if len(r) <= max(io_, iq, ip, it):
                continue
            q, p, t = num(r[iq]), num(r[ip]), num(r[it])
            if None in (q, p, t):
                continue
            if abs(q * p - t) > 0.5:
                bad.append(f"OrderID {r[io_]}: expected {q*p:g}, recorded {t:g}, difference {t-q*p:+g}")
        lines.append("Data check (TotalSales = Quantity x UnitPrice): " +
                     ("all rows match" if not bad else f"{len(bad)} mismatch(es)"))
        lines.extend(bad)

    return {"summary": "\n".join(lines)}
