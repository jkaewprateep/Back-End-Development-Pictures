from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():

    # print(">>>>>>>>>>>>>", data)

    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    # pass
    if data:
        return jsonify(dict(status="OK")), 200

    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    # pass
    if data:

        # find target picture in data
        if id in [ item["id"] for item in data ] :

            item = [ x for x in data if x["id"] == id ];

            return jsonify(item[0]), 200;
        else :
            return jsonify(dict(id=id)), 404;

    return {"message": "Internal server error"}, 500

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    # pass
    if data:
        new_picture = request.json["pic_url"];
        new_id = request.json["id"];
        max_id = max([ item["id"] for item in data ]);
        # print(">>>>>>>>>>>>>", [ item["pic_url"] for item in data ])
        # print(">>>>>>>>>>>>>", new_picture)
        # {'id': 200, 'pic_url': 'http://dummyimage.com/230x100.png/dddddd/000000', 
        # 'event_country': 'United States', 'event_state': 'California', 
        # 'event_city': 'Fremont', 'event_date': '11/2/2030'}

        # find target picture in data
        # if new_picture.strip() in [ item["pic_url"] for item in data ] :
        if new_id in [ item["id"] for item in data ] :
            ### Update values
            _temp = request.json;
            _temp["id"] = new_id;
            # data.append( _temp );

            
            return jsonify(dict(Message=f"picture with id {new_id} already present")), 302;
        else :
            ### Update values
            _temp = request.json;
            # _temp["id"] = max_id + 1;
            data.append( _temp );

            return jsonify(dict(id=new_id)), 201;

        return jsonify(dict(id=new_id)), 201;

    return {"message": "Internal server error"}, 500

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    # pass
    if data:
        new_picture = request.json["pic_url"];
        new_id = request.json["id"];
        new_event_state = request.json["event_state"];

        if new_id in [ item["id"] for item in data ] :
            ### Update values
            for idx, item in enumerate(data) :
                if item["id"] == new_id :
                    
                    data[idx] = request.json;
                    # print("<<<<<<<<<<<<<<<<<<", data)


            return {"event_state": new_event_state}, 200

        else:
            return {"message": "picture not found"}, 404

    return {"message": "Internal server error"}, 500

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    # pass
    if data:

        if id in [ item["id"] for item in data ] :
            ### delete values
            # for idx, item in enumerate(data) :
            #     if item["id"] == new_id :
                    # data = data.remove(request.json);
            
            del data[id];
            return {"message": "HTTP_204_NO_CONTENT"}, 204

        else :

            # data = [{}]
            return {"message": "picture not found"}, 404

    return {"message": "Internal server error"}, 500
