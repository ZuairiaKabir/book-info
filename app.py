from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Search book by title
@app.route("/book")
def get_book_by_title():
    title = request.args.get("title")
    if not title:
        return jsonify({"error": "Please provide a title"}), 400
    
    url = f"https://openlibrary.org/search.json?title={title}"
    r = requests.get(url)
    data = r.json()

    if data["numFound"] == 0:
        return jsonify({"message": "No books found"}), 404

    book = data["docs"][0]
    return jsonify({
        "title": book.get("title"),
        "author": book.get("author_name", []),
        "first_publish_year": book.get("first_publish_year"),
        "isbn": book.get("isbn", [None])[0]
    })

# Search books by author
@app.route("/author")
def get_books_by_author():
    author = request.args.get("name")
    if not author:
        return jsonify({"error": "Please provide an author name"}), 400

    url = f"https://openlibrary.org/search.json?author={author}"
    r = requests.get(url)
    data = r.json()

    if data["numFound"] == 0:
        return jsonify({"message": "No books found"}), 404

    books = [doc.get("title") for doc in data["docs"]]
    return jsonify({"author": author, "books": books})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
