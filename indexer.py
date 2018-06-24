import os
from pdf import pdf_from_file, get_checksum

def find_files(folder_path):
    files = []
    for f in os.scandir(folder_path):
        if f.is_file():
            files.append(f)

    return files

class Index:
    def __init__(self, entries={}):
        self.entries = entries

    def find(self, query):
        query = query.lower()
        matches = []
        for e in self.entries.values():
            if e.title and query in e.title.lower():
                matches.append(e)
            elif e.keywords and query in e.keywords.lower():
                matches.append(e)

        return matches

    def index_documents(self, doc_path):
        files = find_files(doc_path)
        entries = {}
        for fp in files:
            docpath = os.path.join(doc_path, fp.name)
            with open(docpath, "rb") as fh:
                cs = get_checksum(fh)

                # Don't re-read the file if we have already indexed it.
                if self.entries.get(cs):
                    entries[cs] = self.entries[cs]
                    continue

                pdf = pdf_from_file(fh, docpath, cs)

            if pdf and pdf.slug:
                e = Entry(pdf.title, pdf.subject, pdf.keywords, pdf.slug, docpath, pdf.checksum)
                entries[e.checksum] = e

        self.entries = entries

class Entry:

    def __init__(self, title, category, keywords, id, filepath, checksum):
        self.title = title
        self.category = category
        self.keywords = keywords
        self.id = id

        self.filepath = filepath
        self.checksum = checksum

    @property
    def filename(self):
        return os.path.basename(self.filepath)
