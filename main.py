from flask import Flask, request, jsonify
# from elevenlabs import generate, set_api_key

app = Flask(__name__)

# Set your ElevenLabs API key
# set_api_key("YOUR_ELEVENLABS_API_KEY")

@app.route("/text_to_speech", methods=["POST"])
def text_to_speech():
    # try:
    #     text = request.json.get("text")
    #     if not text:
    #         return jsonify({"error": "Text is missing"}), 400

        # Generate speech using ElevenLabs
        # audio = generate(text)
        # open mp3 file and read it as binary
    with open("POC_Deepvoice.mp3", "rb") as f:
        audio = f.read()
        
        # You can save the audio to a file or stream it directly
        # For example:
        # save(audio, "output.mp3")

        return jsonify({"audio": audio})
    # except Exception as e:
    #     return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
