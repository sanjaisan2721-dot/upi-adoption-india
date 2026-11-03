import pdfplumber

with pdfplumber.open("data/raw/population_projections.pdf") as pdf:
    text = pdf.pages[85].extract_text() or ""
    lines = text.split("\n")
    print("PDF PAGE 86, total lines:", len(lines))
    for line in lines[:30]:
        print(line[:110])
