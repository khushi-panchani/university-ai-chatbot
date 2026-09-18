import os

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    jsonify
)

from werkzeug.utils import secure_filename

from src.rag_engine import load_pdf, get_answer


app = Flask(__name__)

# Folder where uploaded PDFs are saved
UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# --------------------------------------------------
# FIRST PAGE: UPLOAD PDF
# --------------------------------------------------

@app.route("/")
def upload_page():

    return render_template("upload.html")


# --------------------------------------------------
# UPLOAD PDF
# --------------------------------------------------

@app.route("/upload", methods=["POST"])
def upload_pdf():

    try:

        # Check whether the user selected a file
        if "pdf" not in request.files:

            return "No PDF file selected."

        file = request.files["pdf"]

        # Check empty filename
        if file.filename == "":

            return "Please select a PDF file."

        # Allow only PDF files
        if not file.filename.lower().endswith(".pdf"):

            return "Only PDF files are allowed."

        # Make filename safe
        filename = secure_filename(file.filename)

        # Create file path
        file_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        # Save uploaded PDF
        file.save(file_path)

        print("PDF uploaded successfully!")
        print("File path:", file_path)

        # Load uploaded PDF into RAG system
        load_pdf(file_path)

        print("PDF loaded into RAG system successfully!")

        # Open second page
        return redirect(url_for("chat_page"))

    except Exception as error:

        print("ERROR IN /upload ROUTE:", error)

        return "Error while uploading PDF: " + str(error)


# --------------------------------------------------
# SECOND PAGE: CHAT
# --------------------------------------------------

@app.route("/chat")
def chat_page():

    return render_template("chat.html")


# --------------------------------------------------
# ASK QUESTION
# --------------------------------------------------

@app.route("/ask", methods=["POST"])
def ask_question():

    try:

        data = request.get_json()

        question = data.get("question", "").strip()

        if not question:

            return jsonify({
                "answer": "Please enter a question."
            }), 400

        print("Question received:", question)

        answer = get_answer(question)

        print("Answer generated successfully!")

        return jsonify({
            "answer": answer
        })

    except Exception as error:

        print("ERROR IN /ask ROUTE:", error)

        error_message = str(error)

        if "RESOURCE_EXHAUSTED" in error_message:

            return jsonify({
                "answer":
                "Gemini API quota exceeded. Please try again later."
            }), 429

        return jsonify({
            "answer":
            "Something went wrong. Please check the Flask terminal."
        }), 500


# --------------------------------------------------
# RUN APPLICATION
# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        debug=False,
        host="127.0.0.1",
        port=5000
    )