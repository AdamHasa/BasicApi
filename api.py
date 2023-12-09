from flask import Flask, request, jsonify, make_response
import dataset

app = Flask(__name__)
db = dataset.connect('sqlite:///twitter.db')

userTable = db['users']
messageTable = db['messages']
tagsTable = db['tags']
messageTagsTable = db['messageTags']

@app.route('/api/db_populate', methods=['GET'])
def db_populate():
    userTable.insert({
        "name": "testname",
        "email": "testmail@mail.com"
    })

    messageTable.insert({
        "message": "test message",
        "userId": "1"
    })
    tagsTable.insert({
        "tag": "test tag"
    })

    messageTagsTable.insert({
        "tag_id": "1",
        "message_id": "1"
    })

    return make_response(jsonify(fetch_db_user_all()),
                         200)

def fetch_db_user(id): 
    return userTable.find_one(id=id)

def fetch_db_user_all():
    users = []
    for user in userTable:
        users.append(user)
    return users

@app.route("/get-user/<user_id>", methods=["GET"])
def get_user(user_id):
    user_data = fetch_db_user(user_id)

    return jsonify(user_data), 200

@app.route("/get-users", methods=["GET"])
def get_user_all():
    user_data = fetch_db_user_all()

    return jsonify(user_data), 200


@app.route("/create-user", methods=["POST"])
def create_user():
    data = request.get_json()

    user_id = userTable.insert(data)

    return jsonify({"userId": user_id}), 201

@app.route("/delete-user/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    if not userTable.find_one(id=user_id):
        return make_response(jsonify({"error": "User not found"}), 404)
    
    userTable.delete(id=user_id)

    return jsonify({"melding": f"gebruiker met id {user_id} verwijderd"}), 200

@app.route('/update-user/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()

    if not userTable.find_one(id=user_id):
        return make_response(jsonify({"error": "User not found"}), 404)

    data['id'] = user_id  
    userTable.update(data, ['id'])

    return jsonify(fetch_db_user(user_id)), 200

@app.route('/create-message', methods=['POST'])
def create_message():
    data = request.get_json()

    user_id = data.get('userId')
    if not userTable.find_one(id=user_id):
        return make_response(jsonify({"error": "User not found"}), 404)

    message_id = messageTable.insert(data)

    return jsonify({"messageId": message_id}), 201

@app.route('/messages', methods=['GET'])
def get_all_messages():
    messages = []
    for message in messageTable:
        messages.append(message)
    return jsonify(messages), 200
    
@app.route('/messages/<user_id>', methods=['GET'])
def get_user_messages(user_id):
    if not userTable.find_one(id=user_id):
        return make_response(jsonify({"error": "User not found"}), 404)
    user_messages = [dict(message) for message in messageTable.find(userId=user_id)]
    return jsonify(user_messages), 200

@app.route('/tags/<message_id>', methods=['POST'])
def add_tags(message_id):
    data = request.get_json()

    if not messageTable.find_one(id=message_id):
        return make_response(jsonify({"error": "Message not found"}), 404)

    for tag_name in data.get('tags', []):
        tag = tagsTable.find_one(tag=tag_name)
        if not tag:
            tag = tagsTable.insert({"tag": tag_name})

        if isinstance(tag, dict):
            existing_tag_message = messageTagsTable.find_one(tag_id=tag['id'], message_id=message_id)
            if not existing_tag_message:
                messageTagsTable.insert({"tag_id": tag['id'], "message_id": message_id})

    return jsonify({"messageId": message_id}), 201

@app.route('/tags/<message_id>', methods=['DELETE'])
def remove_tags(message_id):
    data = request.get_json()

    if not messageTable.find_one(id=message_id):
        return make_response(jsonify({"error": "Message not found"}), 404)

    for tag_name in data.get('tags', []):
        tag = tagsTable.find_one(tag=tag_name)
        if tag:
            messageTagsTable.delete(message_id=message_id, tag_id=tag['id'])

    return jsonify({"messageId": message_id}), 200

@app.route('/tags', methods=['GET'])
def get_all_tags():
    all_tags = [dict(tag) for tag in tagsTable.all()]
    return jsonify(all_tags), 200

@app.route('/tags/<tag_name>', methods=['GET'])
def get_messages_by_tag(tag_name):
    tag = tagsTable.find_one(tag=tag_name)

    if not tag:
        return make_response(jsonify({"error": "Tag not found"}), 404)
    
    tag_messages = messageTagsTable.find(tag_id=tag['id'])

    messages = []
    for tag_message in tag_messages:
        message_id = tag_message['message_id']
        message = messageTable.find_one(id=message_id)
        if message:
            messages.append(dict(message))

    return jsonify(messages), 200

@app.route('/tagMessage', methods=['GET'])
def get_all_tagMessage():
    tagMessages = []
    for tagMessage in messageTagsTable:
        tagMessages.append(tagMessage)
    return jsonify(tagMessages), 200

if __name__ == "__main__":
    app.run(debug=True)