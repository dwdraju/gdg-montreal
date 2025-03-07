from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Ensure the API key is set, otherwise raise an error
api_key = os.getenv("AI_GOOGLE_DEV_API_KEY")
if not api_key:
    raise RuntimeError("AI_GOOGLE_DEV_API_KEY environment variable is missing.")

genai.configure(api_key=api_key)

def get_playlist_from_gemini(mood):
    try:
        model = genai.GenerativeModel("models/gemini-2.0-flash")
        prompt = f"Recommend a playlist for someone feeling {mood}. Provide a short list of songs limiting to 4."
        response = model.generate_content(prompt)
        if response and hasattr(response, 'text') and response.text:
            return [line.strip() for line in response.text.strip().split("\n") if line.strip()]
    except Exception as e:
        print(f"Error generating playlist: {e}")
    return ["No playlist found."]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/playlist", methods=["POST"])
def playlist():
    mood = request.form.get("mood")
    playlist = get_playlist_from_gemini(mood)
    return jsonify({"playlist": playlist})

@app.route("/version")
def version():
    k_revision = os.getenv("K_REVISION", "unknown")
    return jsonify({"revision": k_revision})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
