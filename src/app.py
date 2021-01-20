"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():
    body = jsonify(jackson_family._members)
    return body, 200

@app.route('/member/<int:id>', methods=['GET'])
def get_one_member(id):
    user = jackson_family.get_member(id)
    return user, 200

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    user = jackson_family.delete_member(id)
    print(user)
    return jsonify("Borrado"), 200

@app.route('/member', methods=['POST'])
def new_member():
    body= request.get_json()
    jackson_family.add_member(body)
    return 'MNuevo miembro', 200
    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
