from flask import Flask, request, jsonify, render_template
import random, os

app = Flask(__name__)

# Sample playlist data
playlists = {
    "happy": ["Happy - Pharrell Williams", "Can't Stop the Feeling - Justin Timberlake", "Good Life - OneRepublic"],
    "sad": ["Someone Like You - Adele", "Fix You - Coldplay", "Yesterday - The Beatles"],
    "energetic": ["Stronger - Kanye West", "Eye of the Tiger - Survivor", "Don't Stop Believin' - Journey"],
    "relaxed": ["Weightless - Marconi Union", "Sunset Lover - Petit Biscuit", "Better Together - Jack Johnson"]
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/playlist', methods=['POST'])
def get_playlist():
    mood = request.form.get('mood')
    if mood and mood.lower() in playlists:
        suggested_songs = random.sample(playlists[mood.lower()], len(playlists[mood.lower()]))
        return jsonify({"mood": mood, "playlist": suggested_songs})
    else:
        return jsonify({"error": "Invalid mood. Try 'happy', 'sad', 'energetic', or 'relaxed'."})

@app.route("/version")
def version():
    k_revision = os.getenv("K_REVISION", "unknown")
    return jsonify({"revision": k_revision})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
