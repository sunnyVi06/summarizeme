from flask import Flask, render_template, request, send_file
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

app = Flask(__name__)

SUMMARY_FILE = "summary.txt"

def summarize_text(text, sentences=5):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentences)
    return "\n".join(str(s) for s in summary)

@app.route("/", methods=["GET", "POST"])
def home():
    summary = ""

    if request.method == "POST":
        text = request.form.get("text")

        # If file uploaded
        file = request.files.get("file")
        if file and file.filename.endswith(".txt"):
            text = file.read().decode("utf-8")

        if text and text.strip():
            summary = summarize_text(text)

            # Save summary to file
            with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
                f.write(summary)

    return render_template("index.html", summary=summary)

@app.route("/download")
def download():
    return send_file(SUMMARY_FILE, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

