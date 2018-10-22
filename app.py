from flask import Flask, jsonify, request, Response

from BookModel import *
from settings import *

import json

def validBookObject(bookObject):
    if ("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
        return True
    else:
        return False
        
@app.route('/books')
def get_books():
    return jsonify({'books': Book.get_all_books()})

@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if(validBookObject(request_data)):
        Book.add_book(request_data['isbn'], request_data['name'], request_data['price'])
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = "/books/" + str(request_data['isbn'])
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
    return_value = Book.get_book(isbn)
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
        
    Book.replace_book(isbn, request_data['name'], request_data['price'])
    response = Response('', status=204)
    return response

@app.route('/books/<int:isbn>', methods=['PATCH'])
def updateBooks(isbn):
    request_data =  request.get_json()
    can_update = ['name', 'price']
    if all(item in can_update for item in request_data):
        if ('price' in request_data):
            Book.update_book_price(isbn, request_data['price'])
        if ('name' in request_data):
            Book.update_book_name(isbn, request_data['name'])
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
    if (Book.delete_book(isbn)):
        response = Response('', status=204) 
        return response
        
    invalidBookErrorMessage = {
        "error": "Book with Provided ISBN was not found"
    }
    response = Response(json.dumps(invalidBookErrorMessage), status=400,  mimetype='application/json')
    return response    
     
app.run(port=5000)