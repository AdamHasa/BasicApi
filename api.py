from flask import Flask, request, jsonify, make_response
import dataset
import json
import os

app = Flask(__name__)
db = dataset.connect('sqlite:///twitter.db')

userTable = db['users']
messageTable = db['messages']
tagsTable = db['tags']
messageTagsTable = db['messageTags']

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

@app.route("/create-user", methods=["POST"])
def create_user():
    filepath = "database/users.json"
    data = request.get_json()

    with open(filepath, "a") as outfile:
        outfile.seek(0, os.SEEK_END)
        if outfile.tell() > 0:
            outfile.write(",\n")
        json.dump(data, outfile, indent=4)

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