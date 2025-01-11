from pdf_processing import (
    load_document,
    extract_drawing_tables,
    filter_tables,
    get_table_pixmap,
    pixmap_to_base64_png,
    save_pixmap,
)

# from ai_processing import parse_tables, connect_to_ai
from gemini_processing import parse_tables, connect_to_ai

if __name__ == "__main__":
    import base64
    import os
    from dotenv import load_dotenv
    import logging
    from pprint import pprint

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler()],
    )

    load_dotenv()

    b64_data = None
    with open(
        "../drawings/Hackathon/01_Pfetten/FT_XX_01-104_a_F.pdf", "rb"
    ) as pdf_file:
        content = pdf_file.read()
        b64_data = base64.b64encode(content).decode("ascii")

    document = load_document(b64_data)
    logging.info("Loaded document")
    page = document[0]
    tables = filter_tables(extract_drawing_tables(page))
    logging.info("Extracted tables")
    pixmaps = (get_table_pixmap(page, table) for table in tables)
    # for i, pixmap in enumerate(pixmaps):
    #     save_pixmap(pixmap, f"table-{i}.png")
    base64_images = (pixmap_to_base64_png(pixmap) for pixmap in pixmaps)

    ai_client = connect_to_ai(os.getenv("GEMINI_API_KEY"))
    ai_response = parse_tables(base64_images, ai_client)
    print("GEMINI RESPONSE")
    pprint(ai_response)
