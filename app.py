from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    search_type = request.form.get("search_type")
    query = request.form.get("query")

    if not search_type or not query:
        return render_template("result.html", error="Please select search type and enter a query.")

   if search_type == "book":
    url = f"https://openlibrary.org/search.json?title={query}"
    r = requests.get(url)
    data = r.json()
    if data["numFound"] == 0:
        return render_template("result.html", error="No books found.", search_type=search_type)
    book = data["docs"][0]

    # New fields: short detail, genre, rating
    short_detail = book.get("subtitle") or book.get("first_sentence") or "No description available."
    genre = book.get("subject", [])[:5]  # take first 5 genres if any
    rating = "N/A"  # Placeholder since API has no rating info

    result = {
        "title": book.get("title"),
        "author": book.get("author_name", []),
        "first_publish_year": book.get("first_publish_year"),
        "isbn": book.get("isbn", [None])[0],
        "short_detail": short_detail,
        "genre": genre,
        "rating": rating
    }
    return render_template("result.html", result=result, search_type=search_type)


    elif search_type == "author":
        url = f"https://openlibrary.org/search.json?author={query}"
        r = requests.get(url)
        data = r.json()
        if data["numFound"] == 0:
            return render_template("result.html", error="No books found.", search_type=search_type)
        books = [doc.get("title") for doc in data["docs"]]
        result = {
            "author": query,
            "books": books
        }
        return render_template("result.html", result=result, search_type=search_type)

    else:
        return render_template("result.html", error="Invalid search type.")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
