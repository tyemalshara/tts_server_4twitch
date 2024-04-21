from flask import Flask, Response,render_template
import pyaudio
import socket

app = Flask(__name__)


FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5

 
audio1 = pyaudio.PyAudio()
 
def TwitchConnect(channel_name, myusername, my_oauth_token):
    # Connect to the Twitch chat server
    sock = socket.create_connection(('irc.chat.twitch.tv', 6667))

    # Log in to the server
    sock.send(f'PASS oauth:{my_oauth_token}\r\n'.encode())
    sock.send(f'NICK {myusername}\r\n'.encode())

    # Join the channel
    sock.send(f'JOIN #{channel_name}\r\n'.encode())
    return sock 
 
def add_silence(audio_data, duration_seconds, sample_rate):
    # Calculate the number of samples for the desired duration
    num_samples = int(duration_seconds * sample_rate)
    print(num_samples)
    # Append zeros to the audio data
    silence = 0 * num_samples
    silence = silence.to_bytes(2, byteorder='big')
    print(silence)
    return audio_data + silence


def genHeader(sampleRate, bitsPerSample, channels):
    datasize = 2000*10**6
    o = bytes("RIFF",'ascii')                                               # (4byte) Marks file as RIFF
    o += (datasize + 36).to_bytes(4,'little')                               # (4byte) File size in bytes excluding this and RIFF marker
    o += bytes("WAVE",'ascii')                                              # (4byte) File type
    o += bytes("fmt ",'ascii')                                              # (4byte) Format Chunk Marker
    o += (16).to_bytes(4,'little')                                          # (4byte) Length of above format data
    o += (1).to_bytes(2,'little')                                           # (2byte) Format type (1 - PCM)
    o += (channels).to_bytes(2,'little')                                    # (2byte)
    o += (sampleRate).to_bytes(4,'little')                                  # (4byte)
    o += (sampleRate * channels * bitsPerSample // 8).to_bytes(4,'little')  # (4byte)
    o += (channels * bitsPerSample // 8).to_bytes(2,'little')               # (2byte)
    o += (bitsPerSample).to_bytes(2,'little')                               # (2byte)
    o += bytes("data",'ascii')                                              # (4byte) Data Chunk Marker
    o += (datasize).to_bytes(4,'little')                                    # (4byte) Data size in bytes
    return o

@app.route('/audio')
def audio():
    # start Recording
    def sound():
    
        # print("recording...")
        # with open("POC_Deepvoice.mp3", "rb") as f:
        #     audio = f.read()
        # return audio
        first_run = True
        while True:
            if first_run:
                with open("POC_Deepvoice.mp3", "rb") as f:
                    audio = f.read()
                framerate = 48000 # or whatever you prefer
                silenceduration = 1 # or how many seconds you want to produce
                bytesperframe = 2 # 2 -> 16 bit
                silence = bytes(
                        0 for i in range(int(silenceduration * framerate) * bytesperframe))
                audio = audio + silence
                first_run = False
                yield(audio)
            else:
               # yield empty bytes to keep the connection alive for streaming audio 
                audio = b''
                yield(audio)

    return Response(sound())

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

      
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, threaded=True,port=5000)