from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Setup the SQLite database with multiple users and sensitive info
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Drop the existing table if it exists to avoid the error from the old schema
    cursor.execute("DROP TABLE IF EXISTS users")

    # Create the table with the correct columns (username, email, password)
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT,
                        email TEXT,
                        password TEXT)''')

    # Insert multiple users with sensitive information
    cursor.execute("INSERT INTO users (username, email, password) VALUES ('admin', 'admin@example.com', 'password123')")
    cursor.execute("INSERT INTO users (username, email, password) VALUES ('john_doe', 'john@example.com', 'johnpassword')")
    cursor.execute("INSERT INTO users (username, email, password) VALUES ('jane_smith', 'jane@example.com', 'janepassword')")
    conn.commit()
    conn.close()

# Route to handle form submission (vulnerable to SQL injection)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        
        # Vulnerable SQL query, susceptible to SQL injection
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        query = f"SELECT * FROM users WHERE username = '{username}'"  # Vulnerable to SQL injection
        cursor.execute(query)
        users = cursor.fetchall()
        conn.close()

        if users:
            result = '''
                <h2>Welcome to the User Database</h2>
                <table>
                    <tr><th>Username</th><th>Email</th><th>Password</th></tr>
            '''
            for user in users:
                result += f'<tr><td>{user[1]}</td><td>{user[2]}</td><td>{user[3]}</td></tr>'
            result += '</table>'
            return result
        else:
            return '''
                <h2>User Not Found</h2>
                <p>Sorry, no user found with that username.</p>
            '''
    return '''
        <html>
            <head>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; }
                    h2 { color: #333; }
                    table { border-collapse: collapse; width: 100%; margin-top: 20px; }
                    th, td { padding: 8px 12px; border: 1px solid #ddd; text-align: left; }
                    th { background-color: #f4f4f4; }
                    tr:hover { background-color: #f1f1f1; }
                    form { margin-top: 20px; }
                    input[type="text"] { padding: 10px; width: 250px; font-size: 16px; }
                    input[type="submit"] { padding: 10px 20px; font-size: 16px; background-color: #4CAF50; color: white; border: none; }
                    input[type="submit"]:hover { background-color: #45a049; }
                </style>
            </head>
            <body>
                <h1>SQL Injection Vulnerable User Database</h1>
                <p>Enter a username to search the database:</p>
                <form method="POST">
                    Username: <input type="text" name="username">
                    <input type="submit" value="Submit">
                </form>
            </body>
        </html>
    '''

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
