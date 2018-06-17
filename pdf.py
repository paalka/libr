from pdfrw import PdfReader, PdfWriter

import hashlib
import re
import translitcodec
import codecs

def get_checksum(fh):
    fh.seek(0)
    h = hashlib.md5()
    for block in iter(lambda: fh.read(65536), b""):
        h.update(block)
    fh.seek(0)
    return h.hexdigest()

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
def slugify(text, delim=u'-'):
    """Generates an ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        word = codecs.encode(word, 'translit/long')
        if word:
            result.append(word)
    return delim.join(result)

class Document:

    def __init__(self, title, subject, keywords, checksum, filepath):
        self.title = title
        self.subject = subject
        self.keywords = keywords
        self.filepath = filepath
        self.checksum = checksum

    @property
    def slug(self):
        if not self.title:
            return ""
        return slugify(self.title) + "-" + self.checksum[:4]

    def save(self, output_filename):
        pass

class PDF(Document):
    pass

def edit_pdf(pdf, new_title, new_keywords, new_subject):
    with open(pdf.filepath, "rb") as in_pdf:
        return store_pdf(new_title, new_keywords, new_subject, in_pdf, pdf.filepath)

def store_pdf(title, keywords, subject, fh, output_filename):
    inp = PdfReader(fh)
    inp.Info.Title = title
    inp.Info.Keywords = keywords
    inp.Info.Subject = subject

    with open(output_filename, "wb") as out_f:
        PdfWriter(out_f, trailer=inp).write()

    with open(output_filename, "rb") as pdf_fh:
        cs = get_checksum(pdf_fh)
        return pdf_from_file(pdf_fh, output_filename, cs)

def pdf_from_file(fh, filepath, checksum):
    pdf = PdfReader(fh)
    doc_info = pdf.Info

    if not doc_info.Title:
        return None

    category = doc_info.get("/Subject") or ""
    keywords = doc_info.get("/Keywords") or ""

    if keywords:
        keywords = keywords.decode()

    if category:
        category = category.decode()

    return PDF(doc_info.Title.decode(), category or "",  keywords or "", checksum, filepath)
