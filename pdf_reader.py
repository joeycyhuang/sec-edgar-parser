from pypdf import PdfReader

reader = PdfReader("./data/Form 10-Q.pdf")
for i  in range(len(reader.pages)):
    page_text = reader.pages[i].extract_text()
    print(page_text)
