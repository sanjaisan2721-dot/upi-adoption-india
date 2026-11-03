import pdfplumber

with pdfplumber.open("data/raw/population_projections.pdf") as pdf:
    for p in [86, 87, 88]:
        print("=== PDF PAGE", p, "===")
        lines = (pdf.pages[p - 1].extract_text() or "").split("\n")
        for line in lines[:8]:
            print(line[:120])
