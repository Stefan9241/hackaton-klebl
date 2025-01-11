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
    return jsonify(extract_pdf_data(pdf_data))


if __name__ == "__main__":
    app.run("0.0.0.0", 8888)
