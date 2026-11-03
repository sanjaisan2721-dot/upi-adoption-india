import pdfplumber

with pdfplumber.open("data/raw/population_projections.pdf") as pdf:
    hits = []
    for i in range(60, 140):
        text = pdf.pages[i].extract_text() or ""
        if "1st July" in text and "TABLE" in text.upper() and "Kerala" in text:
            hits.append(i + 1)
    print("Candidate PDF pages:", hits)

    if hits:
        p = hits[0]
        print("---- Text of PDF page", p, "----")
        print((pdf.pages[p - 1].extract_text() or "")[:2000])
