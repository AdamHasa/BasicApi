from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route("/get-user/<user_id>", methods=["GET"])
def get_user(user_id):
    user_data = {
        "user_id": user_id,
        "name": "Test Name",
        "email": "Testmail@test.com"
    }

    extra = request.args.get("extra")
    if extra:
        user_data["extra"] = extra

    return jsonify(user_data), 200

@app.route("/create-user", methods=["POST"])
def create_user():
    filepath = "database/users.json"
    data = request.get_json()

    with open(filepath, "w") as outfile:
        json.dump(data, outfile)

    return jsonify(data), 201

@app.route('/update-user/<user_id>', methods=['PUT'])
def update_user(user_id):
    pass

@app.route('/create-message', methods=['POST'])
def create_message():
    pass

@app.route('/messages', methods=['GET'])
def get_all_messages():
    pass
    
@app.route('/messages/<user_id>', methods=['GET'])
def get_user_messages(user_id):
    pass

@app.route('/tags/<message_id>', methods=['POST'])
def add_tags(message_id):
    pass

@app.route('/tags/<message_id>', methods=['DELETE'])
def remove_tags(message_id):
    pass

@app.route('/tags', methods=['GET'])
def get_all_tags():
    pass

@app.route('/tags/<tag_name>', methods=['GET'])
def get_messages_by_tag(tag_name):
    pass

if __name__ == "__main__":
    app.run(debug=True)