from flask import Flask, request, send_file, render_template_string
import pdfplumber
from docx import Document
import os

app = Flask(__name__)

# Simple HTML form
HTML_FORM = """
<!doctype html>
<title>PDF to Word Converter</title>
<h1>Upload PDF to Convert to Word</h1>
<form method=post enctype=multipart/form-data>
  <input type=file name=pdf_file>
  <input type=submit value=Convert>
</form>
"""

@app.route("/", methods=["GET", "POST"])
def convert_pdf():
    if request.method == "POST":
        pdf_file = request.files.get("pdf_file")
        if not pdf_file:
            return "No file uploaded!"

        # Save uploaded PDF temporarily
        pdf_path = "temp.pdf"
        pdf_file.save(pdf_path)

        # Convert PDF to Word
        doc = Document()
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    doc.add_paragraph(text)

        docx_path = "converted.docx"
        doc.save(docx_path)

        # Remove temporary PDF
        os.remove(pdf_path)

        # Send the Word file as download
        return send_file(docx_path, as_attachment=True)

    return render_template_string(HTML_FORM)

if __name__ == "__main__":
    app.run(debug=True)
