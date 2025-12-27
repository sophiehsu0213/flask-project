import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import mysql.connector

load_dotenv()

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/items", methods=["GET"])
def get_items():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT id, name FROM items")
    rows = cur.fetchall()
    cur.close()
    db.close()
    return jsonify(rows)

@app.route("/items", methods=["POST"])
def add_item():
    data = request.get_json()
    name = data.get("name", "").strip()
    if not name:
        return jsonify({"error": "name required"}), 400

    db = get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO items (name) VALUES (%s)", (name,))
    db.commit()
    item_id = cur.lastrowid
    cur.close()
    db.close()
    return jsonify({"id": item_id, "name": name}), 201

@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM items WHERE id=%s", (item_id,))
    db.commit()
    deleted = cur.rowcount
    cur.close()
    db.close()

    if deleted == 0:
        return jsonify({"error": "not found"}), 404
    return jsonify({"message": "deleted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
