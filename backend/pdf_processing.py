from pymupdf.table import Table
from pymupdf import Page, Document
import base64
from typing import Iterable


def load_document(base64_data: str) -> Document:
    bytes_data = base64.b64decode(base64_data)
    return Document(stream=bytes_data)


def extract_drawing_tables(page: Page) -> Iterable[Table]:
    return page.find_tables(
        vertical_strategy="lines_strict",
        horizontal_strategy="lines",
        intersection_tolerance=7,
        snap_tolerance=0.1,
    )


def table_width(table: Table) -> float:
    return abs(table.bbox[0] - table.bbox[2])


def table_height(table: Table) -> float:
    return abs(table.bbox[1] - table.bbox[3])


def table_area(table: Table) -> float:
    return table_width(table) * table_height(table)


def table_aspect_ratio(table: Table) -> float:
    return table_width(table) / table_height(table)


def filter_tables_by_area(tables: Iterable[Table]) -> Iterable[Table]:
    MIN_AREA = 100 * 100
    return (table for table in tables if table_area(table) > MIN_AREA)


def filter_tables_by_aspect_ratio(tables: Iterable[Table]) -> Iterable[Table]:
    MIN_ASPECT_RATIO = 1 / 15
    MAX_ASPECT_RATIO = 1 / MIN_ASPECT_RATIO
    return (
        table
        for table in tables
        if MIN_ASPECT_RATIO < table_aspect_ratio(table) < MAX_ASPECT_RATIO
    )


def filter_tables(tables: Iterable[Table]) -> Iterable[Table]:
    return filter_tables_by_aspect_ratio(filter_tables_by_area(tables))
