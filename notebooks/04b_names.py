import pdfplumber

with pdfplumber.open("data/raw/population_projections.pdf") as pdf:
    for pno in range(86, 99):
        lines = (pdf.pages[pno - 1].extract_text() or "").split("\n")
        idx = [i for i, l in enumerate(lines) if l.strip() == "Year"]
        if not idx:
            print(pno, "-- no Year line")
            continue
        head = [l for l in lines[:idx[0]]
                if not any(k in l for k in ("TABLE", "Projected", "Territories"))]
        print(pno, "|", " // ".join(head))
