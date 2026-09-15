from src.pdf_loader import extract_text_from_pdf


text = extract_text_from_pdf(
    "data/DBMS.pdf"
)


print(text[:2000])