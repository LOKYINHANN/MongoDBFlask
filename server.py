from flask import Flask, Response, request
app = Flask(__name__)
import json
import pymongo
from bson.objectid import ObjectId
try:
    # mongo = pymongo.MongoClient(host="cluster0", port=27017, serverSelectionTimeOutMs=1000)
    client = pymongo.MongoClient("mongodb+srv://lokyinhann:20ce01@cluster0.ecmkjkk.mongodb.net/?retryWrites=true&w=majority")
    db = client["test"]
    # db = mongo.company
    # mongo.server_info() #trigger exception if cannot connect to DB
except:
    print("ERROR - Cannot connect to database")
#########################
@app.route("/users", methods=["GET"])
def get_some_users():
    try:
        data = list(db.users.find())
        for user in data:
            user["_id"] = str.dumps(data), 
        return Response(
            response= json.dumps({"message":"cannot read users"}),
            status=500,
            mimetype="application/json" 
        )
    except Exception as ex:
        print(ex)
        return Response(
            response= json.dumps({"message":"cannot read users"}),
            status=500,
            mimetype="application/json"
        )




##########################
@app.route("/users", methods=["POST"])
def create_user():
    try:
        user = {"name":"test", "lastName":"lastName"}
        dbResponse = db.users.insert_one(user)
        print(dbResponse.inserted_id)
        #for attr in dir(dbResponse):
            #print(attr)
        return Response(
            response= json.dumps({"message":"user created", "id":f"{dbResponse.inserted_id}"}),
            status=200,
            mimetype="application/json"

        )
    except Exception as ex:
        print("******")
        print(ex)
        print("******")
        
#########################
@app.route("/users/<id>", methods=["PATCH"])
def update_user(id):
    try:
        dbResponse = db.users.update_one(
            {"__id": ObjectId(id)},
            {"$set":{"name":request.form["name"]}}

        )
        for attr in dir(dbResponse):
            print(f"*******{attr}*******")
            return Response(
            response= json.dumps({"message":"User Updated", "id":f"{dbResponse.inserted_id}"}),
            status=500,
            mimetype="application/json"

        )   
    except Exception as ex:
        print("*********")
        print(ex)
        print("*********")
        # return Response(
        #     response= json.dumps({"message":"Sorry. cannot update user", "id":f"{dbResponse.inserted_id}"}),
        #     status=500,
        #     mimetype="application/json"

        # )       



#########################
if __name__ == "__main__":
    app.run(port=80, debug=True)
