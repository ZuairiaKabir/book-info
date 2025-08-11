# 📚 Book Info API

A simple Flask API to search books by title or author using the Open Library API.  
Deployable to Render for free.

## 📌 Features
- Search for a book by its title.
- List all books by a specific author.
- Uses [Open Library API](https://openlibrary.org/developers/api) (free, no authentication required).
- Ready to deploy on [Render](https://render.com).

## 🚀 Endpoints
- `/book?title=Book+Name` → Returns details of the first matching book.
- `/author?name=Author+Name` → Returns a list of books by that author.

### Example Requests:
https://yourapp.onrender.com/book?title=Harry+Potter  
https://yourapp.onrender.com/author?name=J.K.+Rowling

### Example JSON Response for `/book?title=Harry+Potter`
```json
{
  "title": "Harry Potter and the Philosopher's Stone",
  "author": ["J.K. Rowling"],
  "first_publish_year": 1997,
  "isbn": "9780747532699"
}
```
