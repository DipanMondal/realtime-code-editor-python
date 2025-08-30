from flask import Flask, send_from_directory
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_cors import CORS

app = Flask(__name__, static_folder='frontend/dist', static_url_path='')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

rooms = {}

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@socketio.on('join')
def on_join(data):
    room_id = data['roomId']
    user_name = data['userName']
    join_room(room_id)

    if room_id not in rooms:
        rooms[room_id] = set()

    rooms[room_id].add(user_name)

    emit('userJoined', list(rooms[room_id]), to=room_id)

@socketio.on('codeChange')
def on_code_change(data):
    room_id = data['roomId']
    code = data['code']
    emit('codeUpdate', code, to=room_id, skip_sid=True)

@socketio.on('languageChange')
def on_language_change(data):
    room_id = data['roomId']
    language = data['language']
    emit('languageUpdate', language, to=room_id)

@socketio.on('typing')
def on_typing(data):
    room_id = data['roomId']
    user_name = data['userName']
    emit('userTyping', user_name, to=room_id, skip_sid=True)

@socketio.on('leaveRoom')
def on_leave_room():
    # This part requires session management to know which user and room to leave.
    # For simplicity, we'll handle this on the client-side disconnect.
    pass

@socketio.on('disconnect')
def on_disconnect():
    # You'll need a way to track which user disconnected from which room.
    # This can be done using Flask's session or a custom mapping.
    # For now, we'll keep it simple.
    print("User disconnected")


if __name__ == '__main__':
    socketio.run(app, debug=True)