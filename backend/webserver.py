from flask import Flask, request, jsonify
from flask_cors import CORS
from main import extract_pdf_data
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)
load_dotenv()


@app.route("/data-extract", methods=["POST"])
def extract_drawing_data():
    request_body = request.get_json()
    pdf_data: str = request_body["document_data"]
    if pdf_data.startswith("data:application/pdf;base64,"):
        pdf_data = pdf_data[len("data:application/pdf;base64,") :]
    ai_response, table_images_base64 = extract_pdf_data(pdf_data)
    return jsonify(
        {
            "extracted_data": ai_response,
            "table_images": [
                f"data:image/png;base64,{image}" for image in table_images_base64
            ],
        }
    )


if __name__ == "__main__":
    app.run("0.0.0.0", 8888)
