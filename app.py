from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask_question():

    data = request.get_json()

    question = data.get("question", "")

    answer = f"Flask received your question: {question}"

    return jsonify({
        "answer": answer
    })


if __name__ == "__main__":
    app.run(
        debug=False,
        host="127.0.0.1",
        port=5000
    )