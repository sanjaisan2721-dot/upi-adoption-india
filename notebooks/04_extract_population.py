import re
import pdfplumber
import pandas as pd

PDF = "data/raw/population_projections.pdf"
FIRST, LAST = 86, 98          # PDF pages that hold Table 11

year_re = re.compile(r"20[1-3]\d")
num_re = re.compile(r"\d[\d,]*")


def to_int(tok):
    return int(tok.replace(",", "")) * 1000   # table is in thousands


rows, problems = [], []

with pdfplumber.open(PDF) as pdf:
    for pno in range(FIRST, LAST + 1):
        words = pdf.pages[pno - 1].extract_words()

        year_hdr = [w for w in words if w["text"] == "Year"]
        if not year_hdr:
            problems.append((pno, "no Year header"))
            continue
        year_top = min(w["top"] for w in year_hdr)

        # the year numbers sit in the left-most column
        yw = [w for w in words if year_re.fullmatch(w["text"]) and w["top"] > year_top]
        if not yw:
            problems.append((pno, "no year rows"))
            continue
        left = min(w["x0"] for w in yw)
        yw = [w for w in yw if w["x0"] <= left + 3]
        first_top = min(w["top"] for w in yw)
        last_top = max(w["top"] for w in yw)
        yw_ids = {id(w) for w in yw}

        # the 'Male' header words mark the centre of each column group
        males = sorted(
            [w for w in words if w["text"] == "Male" and year_top - 2 < w["top"] < first_top - 1],
            key=lambda w: w["x0"],
        )
        centers = [(w["x0"] + w["x1"]) / 2 for w in males]
        n = len(centers)
        if n == 0:
            problems.append((pno, "no column groups"))
            continue

        def group_of(w):
            c = (w["x0"] + w["x1"]) / 2
            return min(range(n), key=lambda i: abs(centers[i] - c))

        # area names: words between the table title and the 'Year' header
        title = [w for w in words if "000)" in w["text"] and w["top"] < year_top]
        if title:
            tb = max(w["bottom"] for w in title)
            head = [w for w in words if w["top"] >= tb - 0.5 and w["bottom"] <= year_top + 1]
        else:
            head = [w for w in words if year_top - 18 < w["top"] < year_top - 1]

        names = []
        for i in range(n):
            ws = sorted([w for w in head if group_of(w) == i],
                        key=lambda w: (round(w["top"]), w["x0"]))
            names.append(" ".join(w["text"] for w in ws).replace("*", "").strip())

        # numbers: match each to its year row (by height) and column group (by position)
        vals = [w for w in words
                if num_re.fullmatch(w["text"]) and id(w) not in yw_ids
                and first_top - 5 <= w["top"] <= last_top + 10]
        cells = {}
        for w in vals:
            cy = (w["top"] + w["bottom"]) / 2
            y = min(yw, key=lambda a: abs((a["top"] + a["bottom"]) / 2 - cy))
            cells.setdefault((y["text"], group_of(w)), []).append(w)

        for (yr, g), ws in cells.items():
            ws.sort(key=lambda w: w["x0"])
            if len(ws) != 3:
                problems.append((pno, yr, names[g], len(ws)))
                continue
            rows.append({
                "area": names[g], "year": int(yr),
                "persons": to_int(ws[0]["text"]),
                "male": to_int(ws[1]["text"]),
                "female": to_int(ws[2]["text"]),
            })

df = pd.DataFrame(rows).sort_values(["area", "year"])
df.to_csv("data/processed/population_raw.csv", index=False)

print("Rows:", len(df), "| Areas:", df["area"].nunique())
print(" | ".join(sorted(df["area"].unique())))
print("Problems:", len(problems), problems[:5])
y20 = df[df["year"] == 2020]
print("India 2020:", int(y20[y20["area"] == "INDIA"]["persons"].iloc[0]))
print("Sum of other areas 2020:", int(y20[y20["area"] != "INDIA"]["persons"].sum()))
