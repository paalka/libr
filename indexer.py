import os
from pdf import pdf_from_file

def find_files(folder_path):
    files = []
    for f in os.scandir(folder_path):
        if f.is_file():
            files.append(f)

    return files

def index_documents(doc_path):
    files = find_files(doc_path)
    entries = {}
    for fp in files:
        path = os.path.join(doc_path, fp.name)
        pdf = pdf_from_file(path)
        if pdf and pdf.slug:
            e = Entry(pdf.title, pdf.subject, pdf.keywords, pdf.slug, path)
            entries[e.id] = e

    return Index(entries)

class Index:
    def __init__(self, entries):
        self.entries = entries

    def find(self, query):
        matches = []
        for e in self.entries.values():
            if e.title and query in e.title.lower():
                matches.append(e)
            elif e.keywords and query in e.keywords.lower():
                matches.append(e)

        return matches

class Entry:

    def __init__(self, title, category, keywords, id, filepath):
        self.title = title
        self.category = category
        self.keywords = keywords
        self.filepath = filepath
        self.id = id

    @property
    def filename(self):
        return os.path.basename(self.filepath)
