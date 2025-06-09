import fitz  # PyMuPDF
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path, page_range=(20, 40)):
    doc = fitz.open(pdf_path)
    text = ""
    for i in range(page_range[0], page_range[1]):
        text += doc[i].get_text()
    return text

def segment_sentences(text):
    doc = nlp(text)
    return [sent.text.strip() for sent in doc.sents if len(sent.text.strip()) > 10]
