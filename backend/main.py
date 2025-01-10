from pdf_processing import load_document

if __name__ == "__main__":
    import base64
    b64_data = None
    with open("../drawings/Hackathon/01_Pfetten/FT_XX_01-104_a_F.pdf", "rb") as pdf_file:
        content = pdf_file.read()
        b64_data = base64.b64encode(content).decode('ascii')
    
    document = load_document(b64_data)
    print(document[0])