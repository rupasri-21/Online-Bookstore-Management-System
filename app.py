from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            price REAL NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            customer_name TEXT NOT NULL,
            FOREIGN KEY (book_id) REFERENCES books(id)
        )
    ''')
    # Add sample books
    cursor.execute('INSERT OR IGNORE INTO books (id, title, price) VALUES (1, "Python Basics", 25.0)')
    cursor.execute('INSERT OR IGNORE INTO books (id, title, price) VALUES (2, "JavaScript Mastery", 30.0)')
    cursor.execute('INSERT OR IGNORE INTO books (id, title, price) VALUES (3, "Web Development Guide", 20.0)')
    conn.commit()
    conn.close()

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/books', methods=['GET'])
def get_books():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books')
    books = [{'id': row[0], 'title': row[1], 'price': row[2]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(books)

@app.route('/order', methods=['POST'])
def place_order():
    data = request.json
    book_id = data.get('bookId')
    customer_name = data.get('customerName')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO orders (book_id, customer_name) VALUES (?, ?)', (book_id, customer_name))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Order placed successfully!'})

# Initialize the database and run the app
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
