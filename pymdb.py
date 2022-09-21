

from email import message
from nis import match
import tkinter as TK
from turtle import update
from unicodedata import name
from wsgiref.util import request_uri
from pymongo import MongoClient
from flask import Flask ,jsonify,request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from bson.json_util import dumps
from werkzeug.security import generate_password_hash,check_password_hash


app = Flask(__name__)


# data = [
#     {'name':'Anita','email':'anita@123','password':'abcd'},
#     {'name':'Meet','email':'Meet@gmail.com','password':'abcd'}
#     ]  
app.config['MONGO_DBNAME']="CRUD"
app.config['MONGO_URI']="mongodb://localhost:27017/CRUD"
mongo = PyMongo(app)


@app.route('/add', methods=['POST'])
def add_user():
	_json = request.json
	_name = _json['name']
	_email = _json['email']
	_password = _json['pwd']
	
	if _name and _email and _password and request.method == 'POST':
	
		_hashed_password = generate_password_hash(_password)
		# save details
		id = mongo.db.coll.insert_one({'name': _name, 'email': _email, 'pwd': _hashed_password})
		resp = jsonify('User added successfully!')
		resp.status_code = 200
		return resp
	else:
		return not_found()



		
@app.route('/users')
def users():
	users = mongo.db.coll.find()
	resp = dumps(users)
	return resp
		
@app.route('/user/<id>')
def user(id):
	user = mongo.db.coll.find_one({'_id': ObjectId(id)})
	resp = dumps(user)
	return resp

	

@app.route('/update/<user_id>', methods = ['PUT'])
def updateData1(user_id):
    try:
        try:
            body = request.get_json()
        except:

            return "Bad request", 400

        
        records_updated = mongo.db.coll.update_one({"_id": ObjectId(user_id)}, {'$set':body},upsert=True)

        # Check if resource is updated
        if records_updated.modified_count > 0:
            # Prepare the response as resource is updated successfully
            return "user updated", 200
        else:
        
            return "Bad request as the resource is not available to update", 404
    except:
        
        
        return "Error while trying to update the resource", 500



#user deleted by id	
@app.route('/delete/<id>', methods=['DELETE'])
def delete_user(id):
	mongo.db.coll.delete_one({'_id': ObjectId(id)})
	resp = jsonify('User deleted successfully!')
	resp.status_code = 200
	return resp


#user deleted by any value
@app.route('/delete', methods=['DELETE'])
def delete_user1():
	temp= request.get_json()
	mongo.db.coll.delete_one(temp)
	resp = jsonify('User deleted successfully!')
	resp.status_code = 200
	return resp	
		
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

if __name__ == "__main__":
    app.run(debug=True,port=8001)

    
