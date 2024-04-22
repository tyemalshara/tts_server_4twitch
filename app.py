from flask import Flask, Response,render_template
import socket

app = Flask(__name__)

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

@app.route('/audio')
def audio():
    # start Recording
    def sound():
    
        # print("recording...")
        # with open("POC_Deepvoice.mp3", "rb") as f:
        #     audio = f.read()
        # return audio
        first_run = True
        sock = TwitchConnect(channel_name='sharatye', myusername='sharatye', my_oauth_token='4csmm85vwecklxgxsts9npswxqjf4d')  
        while True:
            # if first_run:
            data = sock.recv(1024).decode()
            if data.startswith('PING'):
                sock.send('PONG\r\n'.encode())
            elif 'PRIVMSG' in data:
                username = data.split('!')[0][1:]
                message = str(data.split(':')[2][:-1])
                if '!tts' in message:
                    try:
                        tts_message = message.split('!tts ')[1]
                        if tts_message == '':
                            # TODO:send message to the user that the message is empty
                            continue
                        elif len(tts_message) > 0:
                            print(f'{username}: {message}')
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
                    except Exception as e:
                        # TODO: send message to the user that the message is invalid
                        print('message is invalid')
            elif 'PRIVMSG' not in data:
                audio = b''
                yield(audio)
            # else:
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