import json

def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200


def test_count(client):
    res = client.get("/count")
    assert res.status_code == 200
    assert res.json['length'] == 10


def test_data_contains_10_pictures(client):
    res = client.get("/count")

    # print( "***", res.json )
    assert res.json['length'] == 10
    # assert len(res.json) == 10


def test_get_picture(client):
    res = client.get("/picture")

    assert res.status_code == 200
    assert res.json['status'] == "OK"


def test_get_pictures_check_content_type_equals_json(client):
    res = client.get("/picture")
    assert res.headers["Content-Type"] == "application/json"


def test_get_picture_by_id(client):
    id_delete = 2
    res = client.get(f'/picture/{id_delete}')
    assert res.status_code == 200
    assert res.json['id'] == id_delete

    res = client.get('/picture/404')
    assert res.status_code == 404


def test_pictures_json_is_not_empty(client):
    res = client.get("/picture")
    assert len(res.json) > 0


def test_post_picture(picture, client):
    # create a brand new picture to upload
    res = client.post("/picture", data=json.dumps(picture),
                      content_type="application/json")
    assert res.status_code == 201
    assert res.json['id'] == picture['id']
    res = client.get("/count")
    assert res.status_code == 200
    assert res.json['length'] == 11
    print(picture)

def test_post_picture_duplicate(picture, client):
    # create a brand new picture to upload
    res = client.post("/picture", data=json.dumps(picture),
                      content_type="application/json")
    assert res.status_code == 302
    assert res.json['Message'] == f"picture with id {picture['id']} already present"
    print(picture)

def test_update_picture_by_id(client, picture):
    id = '2'
    res = client.get(f'/picture/{id}')
    res_picture = res.json
    assert res_picture['id'] == 2
    res_state = res_picture["event_state"]
    new_state = "*" + res_state
    res_picture["event_state"] = new_state
    res = client.put(f'/picture/{id}', data=json.dumps(res_picture),
                     content_type="application/json")
    res.status_code == 200
    res = client.get(f'/picture/{id}')
    assert res.json['event_state'] == new_state

def test_delete_picture_by_id(client):
    res = client.get("/count")
    assert res.json['length'] == 11
    res = client.delete("/picture/1")
    assert res.status_code == 204
    res = client.get("/count")
    assert res.json['length'] == 10
    res = client.delete("/picture/100")
    assert res.status_code == 404


###
# @app.route("{insert URL here}", methods="{insert HTTP method name here}")
# def {insert method name here}():
#     return jsonify({insert data list here})

# @app.route("{insert URL here}", methods=["GET"])
# def {insert method name here}(id):
#     {enumerate the data list}:
#         if picture["id"] == id:
#             return picture
#     return {"message": "{insert error message here}"}, {insert HTTP_NOT_FOUND_STATUS}

# @app.route("{insert URL here}", methods="insert list of correct method here")
# def {insert method name here}():

#     # get data from the json body
#     picture_in = {insert code to get json from the request here}

#     # if the id is already there, return 303 with the URL for the resource
#     {enumerate the picture in data list}:
#         if picture_in["id"] == picture["id"]:
#             return {
#                 "Message": f"{insert message here}"
#             }, {insert HTTP code here}

#     data.append(picture_in)
#     return picture_in, {insert HTTP content created code here}

# @app.route("{insert URL here}", methods={insert List of HTTP method here})
# def {insert method name here}(id):

#     # get data from the json body
#     picture_in = {insert code to get json from request here}

#     {insert code to enumerate picture in data list with index}:
#         if picture["id"] == id:
#             data[index] = picture_in
#             return picture, {insert HTTP code here}

#     return {"message": "insert error message here"}, {insert HTTP NOT FOUND code here}

# @app.route("{insert URL here}", methods={insert List of HTTP method here})
# def {insert method name here}(id):

#     {insert code to enumerate pictures in data}:
#         if picture["id"] == id:
#             {insert code to delete picture from data}
#             return "", {insert code to return HTTP code}

#     return {"message": "{insert error message here}"}, {insert code to return HTTP code}

# @app.route("/picture", methods=["GET"])
# def get_pictures():
#     return jsonify(data)

# @app.route("/picture/<int:id>", methods=["GET"])
# def get_picture_by_id(id):
#     for picture in data:
#         if picture["id"] == id:
#             return picture
#     return {"message": "picture not found"}, 404

# @app.route("/picture", methods=["POST"])
# def create_picture():

#     # get data from the json body
#     picture_in = request.json
#     print(picture_in)

#     # if the id is already there, return 303 with the URL for the resource
#     for picture in data:
#         if picture_in["id"] == picture["id"]:
#             return {
#                 "Message": f"picture with id {picture_in['id']} already present"
#             }, 302

#     data.append(picture_in)
#     return picture_in, 201

# @app.route("/picture/<int:id>", methods=["PUT"])
# def update_picture(id):

#     # get data from the json body
#     picture_in = request.json

#     for index, picture in enumerate(data):
#         if picture["id"] == id:
#             data[index] = picture_in
#             return picture, 201

#     return {"message": "picture not found"}, 404

# @app.route("/picture/<int:id>", methods=["DELETE"])
# def delete_picture(id):

#     for picture in data:
#         if picture["id"] == id:
#             data.remove(picture)
#             return "", 204

#     return {"message": "picture not found"}, 404