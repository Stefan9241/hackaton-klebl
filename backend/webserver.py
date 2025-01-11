from flask import Flask, request, jsonify
from main import extract_pdf_data

app = Flask(__name__)


@app.route("/data-extract", methods=["POST"])
def extract_pdf_data():
    request_body = request.get_json()
    pdf_data = request_body["document_data"]
    return jsonify(extract_pdf_data(pdf_data))


if __name__ == "__main__":
    app.run("0.0.0.0", 8888)
