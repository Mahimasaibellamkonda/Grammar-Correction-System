from flask import Flask, render_template, request
import re

app = Flask(__name__)


def correct_text(text):
    text = text.strip()

    # Remove extra spaces
    corrected = re.sub(r"\s+", " ", text)

    # Capitalize first letter
    if corrected:
        corrected = corrected[0].upper() + corrected[1:]

    # Basic grammar corrections
    corrections = {
        r"\bi am\b": "I am",
        r"\bi\b": "I",
        r"\bhe go\b": "he goes",
        r"\bshe go\b": "she goes",
        r"\bhe have\b": "he has",
        r"\bshe have\b": "she has",
        r"\bthey is\b": "they are",
        r"\bwe is\b": "we are",
        r"\byou is\b": "you are",
        r"\bi has\b": "I have",
        r"\bthere is many\b": "there are many",
    }

    for pattern, replacement in corrections.items():
        corrected = re.sub(
            pattern, replacement, corrected, flags=re.IGNORECASE
        )

    # Add full stop if missing
    if corrected and corrected[-1] not in ".!?":
        corrected += "."

    return corrected


@app.route("/", methods=["GET", "POST"])
def index():
    original = ""
    corrected = ""

    if request.method == "POST":
        original = request.form.get("text", "")
        corrected = correct_text(original)

    return render_template(
        "index.html",
        original=original,
        corrected=corrected
    )


if __name__ == "__main__":
    app.run(debug=True)
