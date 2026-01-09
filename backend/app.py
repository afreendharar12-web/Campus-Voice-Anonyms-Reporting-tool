import hashlib
import json
import logging
import os
import random
import sys

import psycopg2
from flask import Flask, jsonify, request
from flask_cors import CORS
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

# --- CONFIGURATION ---
DB_CONNECTION_STRING = os.environ.get(
    "DATABASE_URL",
    "host=localhost port=5432 user=postgres password=postgres dbname=anonymous_report",
)
SERVER_PORT = os.environ.get("PORT", 8080)

# --- FLASK APP INITIALIZATION ---
app = Flask(__name__)
CORS(
    app,
    resources={r"/api/*": {"origins": "http://localhost:5173"}},
    supports_credentials=True,
)

# --- DATABASE CONNECTION ---
db_conn = None

def get_db_connection():
    """Establishes and returns a database connection."""
    global db_conn
    if db_conn is None or db_conn.closed:
        try:
            db_conn = psycopg2.connect(DB_CONNECTION_STRING)
            logging.info("Successfully connected to the database.")
        except psycopg2.OperationalError as e:
            logging.fatal(f"Error connecting to the database: {e}")
            sys.exit(1)
    return db_conn


# --- WORD LIST FOR CODE GENERATION ---
WORDS = [
    "ocean", "river", "breeze", "mountain", "meadow", "forest", "sun", "moon", "star", "cloud",
	"apple", "maple", "willow", "pine", "oak", "cedar", "rose", "lily", "iris", "tulip",
	"blue", "green", "red", "gold", "silver", "aqua", "coral", "plum", "ivory", "amber",
	"lion", "tiger", "eagle", "horse", "dolphin", "raven", "falcon", "koala", "panda", "otter",
]

# --- HELPER FUNCTIONS ---

def generate_access_code():
    """Creates a random, human-readable code."""
    word1 = random.choice(WORDS)
    word2 = random.choice(WORDS)
    number = random.randint(100, 999)
    return f"{word1}-{word2}-{number}"

def hash_access_code(code):
    """Computes the SHA-256 hash of a string."""
    return hashlib.sha256(code.encode()).hexdigest()

# --- DATABASE INITIALIZATION ---

def create_tables():
    """Creates the necessary database tables if they don't exist."""
    conn = get_db_connection()
    schema = """
        CREATE EXTENSION IF NOT EXISTS "pgcrypto";

        CREATE TABLE IF NOT EXISTS reports (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            category VARCHAR(100) NOT NULL,
            location VARCHAR(255),
            description TEXT NOT NULL,
            status VARCHAR(50) NOT NULL DEFAULT 'new',
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS report_access (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            report_id UUID NOT NULL REFERENCES reports(id) ON DELETE CASCADE,
            code_hash VARCHAR(64) NOT NULL UNIQUE
        );
        CREATE INDEX IF NOT EXISTS idx_code_hash ON report_access(code_hash);

        CREATE TABLE IF NOT EXISTS report_updates (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            report_id UUID NOT NULL REFERENCES reports(id) ON DELETE CASCADE,
            message TEXT,
            new_status VARCHAR(50),
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
    """
    try:
        with conn.cursor() as cur:
            cur.execute(schema)
        conn.commit()
        logging.info("Database tables are ready.")
    except Exception as e:
        conn.rollback()
        logging.fatal(f"Error creating tables: {e}")
        raise

# --- API ROUTES (STUDENT) ---

@app.route("/api/reports", methods=["POST"])
def submit_report():
    """Handles the creation of a new anonymous report."""
    data = request.get_json()
    if not data or "category" not in data or "description" not in data:
        return jsonify({"error": "Invalid request body"}), 400

    access_code = generate_access_code()
    hashed_code = hash_access_code(access_code)
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO reports (category, location, description, status) 
                VALUES (%s, %s, %s, 'new') RETURNING id;
                """,
                (data.get("category"), data.get("location"), data.get("description"))
            )
            report_id = cur.fetchone()[0]

            cur.execute(
                "INSERT INTO report_access (report_id, code_hash) VALUES (%s, %s);",
                (report_id, hashed_code)
            )
        conn.commit()
        logging.info(f"New report created with ID: {report_id}")
    except Exception as e:
        conn.rollback()
        logging.error(f"Failed to create report: {e}")
        return jsonify({"error": "Failed to create report"}), 500
    
    return jsonify({"accessCode": access_code}), 201


@app.route("/api/reports/<access_code>", methods=["GET"])
def get_report_status(access_code):
    """Retrieves a report and its updates using the access code."""
    if not access_code or not access_code.strip():
        return jsonify({"error": "Access code cannot be empty"}), 400
        
    hashed_code = hash_access_code(access_code.strip())
    conn = get_db_connection()
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT report_id FROM report_access WHERE code_hash = %s;", (hashed_code,))
            report_access_row = cur.fetchone()

            if not report_access_row:
                return jsonify({"error": "Report not found"}), 404
            
            report_id = report_access_row["report_id"]
            cur.execute("SELECT * FROM reports WHERE id = %s;", (report_id,))
            report = cur.fetchone()
            cur.execute(
                "SELECT * FROM report_updates WHERE report_id = %s ORDER BY created_at ASC;",
                (report_id,)
            )
            updates = cur.fetchall()
    except Exception as e:
        logging.error(f"Error retrieving report for hash {hashed_code}: {e}")
        return jsonify({"error": "Error querying database"}), 500

    response = {"report": report, "updates": updates}
    return jsonify(response)

# --- ADMIN ROUTES ---
# In a real-world app, use a proper user database and JWTs for auth.
# For this example, we'll use a hardcoded user and simple session management.
ADMIN_USER = {"username": "admin", "password": "password123"}

@app.route("/api/admin/login", methods=["POST"])
def admin_login():
    """Handles admin login."""
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Invalid login request"}), 400

    if (data["username"] == ADMIN_USER["username"] and 
        data["password"] == ADMIN_USER["password"]):
        logging.info("Admin login successful.")
        return jsonify({"message": "Login successful"}), 200
    else:
        logging.warning("Failed admin login attempt.")
        return jsonify({"error": "Invalid credentials"}), 401

@app.route("/api/admin/reports", methods=["GET"])
def get_all_reports():
    """Retrieves all reports for the admin dashboard."""
    # NOTE: In a real app, this endpoint would be protected by auth middleware.
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM reports ORDER BY created_at DESC;")
            reports = cur.fetchall()
    except Exception as e:
        logging.error(f"Error retrieving all reports: {e}")
        return jsonify({"error": "Error querying database"}), 500
    
    return jsonify(reports)

@app.route("/api/admin/reports/<report_id>/update", methods=["POST"])
def add_report_update(report_id):
    """Adds a status update and message to a report."""
    # NOTE: In a real app, this endpoint would be protected by auth middleware.
    data = request.get_json()
    if not data or "new_status" not in data or "message" not in data:
        return jsonify({"error": "Invalid update request body"}), 400

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO report_updates (report_id, new_status, message) 
                VALUES (%s, %s, %s);
                """,
                (report_id, data["new_status"], data["message"])
            )
            cur.execute(
                "UPDATE reports SET status = %s WHERE id = %s;",
                (data["new_status"], report_id)
            )
        conn.commit()
        logging.info(f"Report {report_id} updated to status {data['new_status']}")
    except Exception as e:
        conn.rollback()
        logging.error(f"Failed to update report {report_id}: {e}")
        return jsonify({"error": "Failed to update report"}), 500
    
    return jsonify({"message": "Update successful"}), 200


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] - %(message)s",
        handlers=[
            logging.FileHandler("backend.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    create_tables()
    app.run(host="0.0.0.0", port=int(SERVER_PORT), debug=True)

