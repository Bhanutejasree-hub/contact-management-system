
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

# Load environment variables
load_dotenv()

app = Flask(__name__)


# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        port=int(os.environ.get("DB_PORT", 3306)),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME")
    )


# Home page
@app.route('/')
def home():
    return render_template('home.html')


# Display contacts
@app.route('/contacts')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    search = request.args.get('search', '')

    if search:
        cursor.execute(
            "SELECT * FROM contacts WHERE name LIKE %s",
            ('%' + search + '%',)
        )
    else:
        cursor.execute("SELECT * FROM contacts")

    contacts = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('index.html', contacts=contacts)


# Add new contact
@app.route('/add', methods=['GET', 'POST'])
def add_contact():

    if request.method == 'POST':

        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO contacts (name, phone, email, address) VALUES (%s, %s, %s, %s)",
            (name, phone, email, address)
        )

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for('index'))

    return render_template('add_contact.html')


# Edit contact
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_contact(id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':

        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']

        cursor.execute(
            "UPDATE contacts SET name=%s, phone=%s, email=%s, address=%s WHERE id=%s",
            (name, phone, email, address, id)
        )

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for('index'))

    cursor.execute(
        "SELECT * FROM contacts WHERE id=%s", (id,)
    )

    contact = cursor.fetchone()

    cursor.close()
    conn.close()

    if contact is None:
        return "Contact not found", 404

    return render_template('edit_contact.html', contact=contact)


# Delete contact
@app.route('/delete/<int:id>')
def delete_contact(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM contacts WHERE id=%s", (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('index'))


# Run Flask application
if __name__ == '__main__':
    app.run(debug=True)







