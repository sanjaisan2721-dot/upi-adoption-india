import pdfplumber

key = "Projected total population by sex as on 1st July"

with pdfplumber.open("data/raw/population_projections.pdf") as pdf:
    print("Total pages:", len(pdf.pages))
    hits = []
    for i, page in enumerate(pdf.pages):
        text = page.extract_text() or ""
        if key in text:
            hits.append(i + 1)
    print("Pages with the table title:", hits)

    if hits:
        first = hits[0]
        print("---- Text of page", first, "----")
        print((pdf.pages[first - 1].extract_text() or "")[:2500])
