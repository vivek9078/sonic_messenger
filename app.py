from flask import Flask, request, jsonify, send_from_directory
import sender
import receiver

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/send', methods=['POST'])
def send_message():
    data = request.get_json()
    message = data.get('message', '')
    
    if message:
        sender.send_message(message)
        return jsonify({'msg': 'Message sent via sound!'})
    else:
        return jsonify({'msg': 'No message to send'}), 400

@app.route('/receive', methods=['GET'])
def receive_message():
    expected_chars = 10  # or you can dynamically adjust
    message = receiver.receive_message(expected_chars)
    return jsonify({'data': message})

# Serve CSS, JS manually if needed (Flask usually auto handles static files)
@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
