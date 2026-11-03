import pdfplumber

with pdfplumber.open("data/raw/population_projections.pdf") as pdf:
    for i in range(79, 110):
        text = pdf.pages[i].extract_text() or ""
        first = text.replace("\n", " ")[:70]
        print(i + 1, len(text), first)
