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

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def upload_page():
    return render_template("upload.html")

@app.route("/ask", methods=["POST"])
def ask_question():

    try:

        data = request.get_json()

        question = data.get("question", "")

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
                "error": "Gemini API quota exceeded. Please wait and try again later."
            }), 429

        return jsonify({
            "error": "Something went wrong in the chatbot backend."
        }), 500
    
if __name__ == "__main__":
    app.run(
        debug=False,
        host="127.0.0.1",
        port=5000
    )