from openai import OpenAI
from typing import Iterable
from domain import ParsedDrawing
import logging
import re
import json


def connect_to_ai(api_key: str) -> OpenAI:
    return OpenAI(api_key=api_key)


def extract_json(text: str) -> dict:
    JSON_REGEX = re.compile(r"```json\n(.*?)\n```", re.DOTALL)
    matches = JSON_REGEX.search(text)
    json_text = matches.group(1)
    return json.loads(json_text)


def parse_tables(images_png_base64: Iterable[str], client: OpenAI) -> dict:
    format_description = None
    with open("table_extraction_json_schema.txt") as f:
        format_description = f.read()
    if format_description is None:
        raise ValueError("Could not read format description")

    table_extraction_prompt = f"""
You are an experienced architect and/or civil engineer. I need you to give me the data from the
provided tables, which are extracted from technical drawings of prefabbed building elements. Please,
give the data in a JSON format I will provide below. Use the data from every table. If an image
does not look like a table, disregard it.

```json
{format_description}
```

The plan key in the metadata should come from the cell labelled "Plaschluessel",
the "auftr_number" comes from the cell labelled "Auftr. Nr",
the "stat_pos" comes from the cell labelled "stat. Pos",
and the "prefab_position" comes from the cell labelled "Fergteil - Position".

The parts list should be derived from the table with columns "Pos.", "Stck", "Bezeichnung",
corresponding to the "position", "amount", and "designation" fields, respectively.

The each steel list item's positions list should be derived from the columns "Pos.", "Anz", "ø", "Laenge", "Bem.:",
corresponding respectively to the fields "position", "anz", "length", "bem".
"""
    open_ai_images = [
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/png;base64,{image}", "detail": "high"},
        }
        for image in images_png_base64
    ]
    open_ai_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": table_extraction_prompt},
                    *open_ai_images,
                ],
            }
        ],
    )

    response_text = open_ai_response.choices[0].message.content

    print("OpenAI object", open_ai_response)

    return extract_json(response_text)
