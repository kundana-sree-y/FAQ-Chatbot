
from flask import Flask, render_template, request, jsonify
import re

from conversation import get_conversation_response
from translation_engine import (
    get_translation_engine,
    LANGUAGES,
    SCRIPT_PATTERNS
)

app = Flask(__name__)


def detect_student_language(message):

    # Detect languages written in their native scripts first.
    for pattern, code in SCRIPT_PATTERNS:
        if re.search(pattern, message):
            return code

    # English/ASCII messages skip expensive translation.
    # This also prevents langdetect misclassifying short phrases.
    if message.isascii():
        return "en"

    return "en"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json(silent=True) or {}
        message = data.get("message", "").strip()

        if not message:
            return jsonify({
                "response": "Please enter a question.",
                "language": "en"
            }), 400

        language_code = detect_student_language(message)
        english_message = message

        print("\nStudent:", message)
        print("Detected language:", language_code)

        # Only load translation model for non-English scripts
        if language_code != "en":

            try:

                engine = get_translation_engine()

                english_message = engine.translate(
                    message,
                    language_code,
                    "en"
                )

                print("English question:", english_message)

            except Exception as error:

                print("Input translation error:", error)

                return jsonify({
                    "response": "I couldn't understand that message. Please try again in English.",
                    "language": language_code
                }), 500

        # Generate chatbot response
        english_response = get_conversation_response(english_message)

        print("CampusAI:", english_response)

        return jsonify({
            "response": english_response,
            "language": language_code,
            "language_name": LANGUAGES.get(
                language_code,
                ("eng_Latn", "English")
            )[1]
        })

    except Exception as error:

        print("Chat error:", error)

        return jsonify({
            "response": "Something went wrong. Please try again.",
            "language": "en"
        }), 500


@app.route("/translate", methods=["POST"])
def translate_response():

    try:

        data = request.get_json(silent=True) or {}

        text = data.get("text", "").strip()
        target_language = data.get("target_language", "en").strip()

        if not text:
            return jsonify({
                "error": "There is no answer to translate."
            }), 400

        if target_language not in LANGUAGES:
            return jsonify({
                "error": "This language is not supported."
            }), 400

        if target_language == "en":
            return jsonify({
                "translation": text,
                "language": "English"
            })

        engine = get_translation_engine()

        translated_text = engine.translate(
            text,
            "en",
            target_language
        )

        return jsonify({
            "translation": translated_text,
            "language": LANGUAGES[target_language][1]
        })

    except Exception as error:

        print("Translation error:", error)

        return jsonify({
            "error": "Translation failed. Please try again."
        }), 500


if __name__ == "__main__":

    print("\n====================================")
    print("             CAMPUSAI")
    print("====================================")
    print("College Assistant is starting...")
    print("English messages: Fast processing")
    print("Translation: On demand")
    print("Open: http://127.0.0.1:5000")
    print("====================================\n")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
