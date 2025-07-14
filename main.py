# Import the Flask class from the flask module
from flask import Flask, make_response, request

data = [
    {
        "id": "3b58aade-8415-49dd-88db-8d7bce14932a",
        "first_name": "Tanya",
        "last_name": "Slad",
        "graduation_year": 1996,
        "address": "043 Heath Hill",
        "city": "Dayton",
        "zip": "45426",
        "country": "United States",
        "avatar": "http://dummyimage.com/139x100.png/cc0000/ffffff",
    },
    {
        "id": "d64efd92-ca8e-40da-b234-47e6403eb167",
        "first_name": "Ferdy",
        "last_name": "Garrow",
        "graduation_year": 1970,
        "address": "10 Wayridge Terrace",
        "city": "North Little Rock",
        "zip": "72199",
        "country": "United States",
        "avatar": "http://dummyimage.com/148x100.png/dddddd/000000",
    },
    {
        "id": "66c09925-589a-43b6-9a5d-d1601cf53287",
        "first_name": "Lilla",
        "last_name": "Aupol",
        "graduation_year": 1985,
        "address": "637 Carey Pass",
        "city": "Gainesville",
        "zip": "32627",
        "country": "United States",
        "avatar": "http://dummyimage.com/174x100.png/ff4444/ffffff",
    },
    {
        "id": "0dd63e57-0b5f-44bc-94ae-5c1b4947cb49",
        "first_name": "Abdel",
        "last_name": "Duke",
        "graduation_year": 1995,
        "address": "2 Lake View Point",
        "city": "Shreveport",
        "zip": "71105",
        "country": "United States",
        "avatar": "http://dummyimage.com/145x100.png/dddddd/000000",
    },
    {
        "id": "a3d8adba-4c20-495f-b4c4-f7de8b9cfb15",
        "first_name": "Corby",
        "last_name": "Tettley",
        "graduation_year": 1984,
        "address": "90329 Amoth Drive",
        "city": "Boulder",
        "zip": "80305",
        "country": "United States",
        "avatar": "http://dummyimage.com/198x100.png/cc0000/ffffff",
    }
]

app = Flask(__name__)

@app.route("/")
def index():
    return "hello world"

@app.route('/no_content')
def no_content():
    return {"message": "No content found"}, 204

@app.route('/exp')
def index_explicit():
    res = make_response({"message": "Hello Wolrd"})
    res.status_code = 200
    return res

@app.route("/data")
def get_data():
    try:
        # Check if 'data' exists and has a length greater than 0
        if data and len(data) > 0:
            # Return a JSON response with a message indicating the length of the data
            return {"message": f"Data of length {len(data)} found"}
        else:
            # If 'data' is empty, return a JSON response with a 500 Internal Server Error status code
            return {"message": "Data is empty"}, 500
    except NameError:
        # Handle the case where 'data' is not defined
        # Return a JSON response with a 404 Not Found status code
        return {"message": "Data not found"}, 404


@app.route('/name_search')
def name_search():
    q = request.args.get('q')

    if q is None:
        return {"message": "Query parameter 'q' is missing"}, 400
    if q.strip() == "" or q.isdigit():
        return {"message": "Invalid input parameter"}, 422

    for person in data:
        if q.lower() in person["first_name"].lower():
            # If a match is found, return the person as a JSON response with a 200 OK status code
            return person, 200

    return {"message": "Person not found"}, 404


@app.route("/count")
def count():
    try:
        
        return {"data count": len(data)}, 200
    except NameError:

        return {"message": "data not defined"}, 500


@app.route("/person/<var_name>")
def find_by_uuid(var_name):
    for person in data:
        if person["id"] == str(var_name):
            return person
    return {"message": "Person not found"}, 404


@app.route("/person/<uuid:id>", methods=['DELETE'])
def delete_person(id):
    for person in data:
        if person["id"] == str(id):
            data.remove(person)
            return {"message": "Person with ID deleted"}, 200
    return {"message": "Person not found"}, 404


@app.route("/person", methods=['POST'])
def create_person():
    new_person = request.get_json()

    if not new_person:
        return {"message": "Invalid input parameter"}, 422
    
    try:
        data.append(new_person)
    except NameError:
        return {"message": "data not defined"}, 500
    
    return {"message": "Person created successfully"}, 200


@app.errorhandler(404)
def api_not_found(error):
    return {"message": "API not found"},  404