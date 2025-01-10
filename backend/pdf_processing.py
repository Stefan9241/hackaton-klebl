import pymupdf
from pymupdf.table import Table
from pymupdf import Page, Document
import base64


def load_document(base64_data: str) -> Document:
    bytes_data = base64.b64decode(base64_data)
    return Document(stream=bytes_data)
