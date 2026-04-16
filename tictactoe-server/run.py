from app import create_app, socketio
import app.sockets  # This MUST be here to register the events

app = create_app()

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
    # If you want to use NGROK, open a separate terminal and type: ngrok http 5000