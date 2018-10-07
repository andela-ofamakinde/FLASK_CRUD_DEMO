from flask import Flask, jsonify, request, Response
import json

app = Flask(__name__)

books = [
    {
        'name': 'Things fall apart',
        'price': 20.99,
        'isbn': 9090909
    },
    {
        'name': 'Power of now',
        'price': 20.99,
        'isbn': 9090908
    }
]
def validBookObject(bookObject):
    if ("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
        return True
    else:
        return False
        
@app.route('/books')
def get_books():
    return jsonify({'books': books})

@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if(validBookObject(request_data)):
        new_book = {
            'name': request_data['name'],
            'price': request_data['price'],
            'isbn': request_data['isbn']
        }
        books.insert(0, new_book)
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = "/books/" + str(new_book['isbn'])
        return response
    else:
        invalidBookErrorMessage = {
            "error": "Invalid book object passed in request",
            "helpString": "Refer to documentation for correct format"
        }
        response = Response(json.dumps(invalidBookErrorMessage), status=400,  mimetype='application/json')
        return response
        
@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = {}
    for book in books:
        if book['isbn'] == isbn:
            return_value = {
                'name': book['name'],
                'isbn': book['isbn'],
                'price': book['price']
            }
    return jsonify(return_value)
    
    
@app.route('/books/<int:isbn>', methods=['PUT'])
def replaceBooks(isbn):
    request_data = request.get_json()
    new_book = {
        'name' : request_data['name'],
        'price' : request_data['price'],
        'isbn' : isbn
    }
    if (not validBookObject(new_book)):
        invalidBookErrorMessage = {
            "error": "Invalid book object passed in request",
            "helpString": "Refer to documentation for correct format"
        }
        response = Response(json.dumps(invalidBookErrorMessage), status=400,  mimetype='application/json')
        return response
    
    i = 0
    for book in books:
        current_isbn = book['isbn']
        if current_isbn == isbn:
            books[i] = new_book
        i += 1
    response = Response('', status=204)
    return response

@app.route('/books/<int:isbn>', methods=['PATCH'])
def updateBooks(isbn):
    request_data =  request.get_json()
    can_update = ['name', 'price']
    if all(item in can_update for item in request_data):
        for book in books:
            if book["isbn"] == isbn:
                book.update(request_data)
        response = Response("", status=204)
        response.headers['Location'] = "/books/" + str(isbn)
        return response
    else:
        invalidBookErrorMessage = {
            "error": "Invalid book object passed in request",
            "helpString": "Refer to documentation for correct format"
        }
        response = Response(json.dumps(invalidBookErrorMessage), status=400,  mimetype='application/json')
        return response

@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    i = 0
    for book in books:
        if book["isbn"] == isbn:
            books.pop(i)
            response = Response("", status=204)
            return response
        i += 1
    invalidBookErrorMessage = {
        "error": "Book with Provided ISBN was not found"
    }
    response = Response(json.dumps(invalidBookErrorMessage), status=400,  mimetype='application/json')
    return response    
     
app.run(port=5000)