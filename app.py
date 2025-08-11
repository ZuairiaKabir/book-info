from flask import Flask, request, render_template
import requests

app = Flask(__name__)

def get_google_books_info(isbn=None, title=None):
    # Query Google Books by ISBN if available, else by title
    if isbn:
        url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    elif title:
        url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{title}"
    else:
        return {}

    resp = requests.get(url)
    data = resp.json()
    if "items" not in data:
        return {}

    volume_info = data["items"][0]["volumeInfo"]

    return {
        "description": volume_info.get("description", "No description available."),
        "categories": volume_info.get("categories", []),
        "average_rating": volume_info.get("averageRating", "N/A"),
        "ratings_count": volume_info.get("ratingsCount", 0),
        "page_count": volume_info.get("pageCount", "N/A"),
        "publisher": volume_info.get("publisher", "N/A"),
        "published_date": volume_info.get("publishedDate", "N/A"),
    }

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
        ol_url = f"https://openlibrary.org/search.json?title={query}"
        ol_resp = requests.get(ol_url)
        ol_data = ol_resp.json()
        if ol_data["numFound"] == 0:
            return render_template("result.html", error="No books found.", search_type=search_type)
        
        book = ol_data["docs"][0]
        isbn = book.get("isbn", [None])[0]

        google_info = get_google_books_info(isbn=isbn, title=book.get("title"))

        result = {
            "title": book.get("title"),
            "author": book.get("author_name", []),
            "first_publish_year": book.get("first_publish_year"),
            "isbn": isbn,
            "short_detail": book.get("subtitle") or (book.get("first_sentence") if isinstance(book.get("first_sentence"), str) else "No short description available."),
            "genre": book.get("subject", [])[:5],
            "description": google_info.get("description"),
            "categories": google_info.get("categories"),
            "average_rating": google_info.get("average_rating"),
            "ratings_count": google_info.get("ratings_count"),
            "page_count": google_info.get("page_count"),
            "publisher": google_info.get("publisher"),
            "published_date": google_info.get("published_date"),
        }
        return render_template("result.html", result=result, search_type=search_type)

    elif search_type == "author":
        ol_url = f"https://openlibrary.org/search.json?author={query}"
        ol_resp = requests.get(ol_url)
        ol_data = ol_resp.json()
        if ol_data["numFound"] == 0:
            return render_template("result.html", error="No books found.", search_type=search_type)
        
        books = [doc.get("title") for doc in ol_data["docs"]]
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
