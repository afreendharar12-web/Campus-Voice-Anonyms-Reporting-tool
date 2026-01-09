# 🛡️ Campus Voice: Secure Anonymous Reporting System

**A Cryptographically Secure Grievance Redressal Platform**

Campus Voice is a full-stack web application designed to eliminate the fear of retaliation in student reporting. Unlike traditional "anonymous" forms that track metadata, Campus Voice uses a **"Digital Black Box"** architecture powered by **SHA-256 Hashing** to ensure that linking a report to a student is mathematically impossible.

---

## 🔐 Key Technical Concepts

### 1. Provable Anonymity via Hashing (SHA-256)
* **The Problem:** Storing user data creates a risk of identity leaks.
* **The Solution:** The system never stores the user's identity or their unique "Access Code."
* **Implementation:**
    * When a report is submitted, a unique random code is generated for the user.
    * The system calculates the **SHA-256 Hash** of this code and stores *only the hash* in the database.
    * Because SHA-256 is a one-way function, the original code cannot be reverse-engineered from the database, ensuring total privacy even if the database is compromised.

### 2. Hash Table & Indexing Principles
* **Data Structure:** The retrieval system operates on the principles of a **Hash Table** for O(1) lookups.
* **Optimization:** Utilizes **B-Tree Indexing** within PostgreSQL to efficiently query millions of hashed keys without performance degradation.

---

## 🛠️ Tech Stack

* **Frontend:** SvelteKit (JavaScript/HTML/CSS) - For a high-performance, reactive user interface.
* **Styling:** Tailwind CSS - For responsive and modern design.
* **Backend:** Python (Flask) - RESTful API handling cryptographic logic and request processing.
* **Database:** PostgreSQL - Relational database for storing encrypted report data.
* **DevOps:** Docker - Containerized environment for consistent deployment.

---

## 🚀 Features

* **🚫 Zero-Knowledge Submission:** Students can submit reports on sensitive topics (Harassment, Safety, Mental Health) without logging in or providing email addresses.
* **🔑 Secure Status Tracking:** Users receive a unique "Access Key" to track the status of their report later. The system validates this key by re-hashing it and comparing it to the stored hash.
* **👮 Admin Dashboard:** A secure, password-protected portal for administrators to triage reports, update statuses (e.g., "Under Investigation", "Resolved"), and post anonymous replies.
* **💬 Two-Way Anonymous Chat:** Allows admins to ask follow-up questions to the reporter without ever knowing who they are.

---

## ⚙️ How to Run Locally

### Prerequisites
* Python 3.8+
* Node.js & npm
* PostgreSQL installed and running locally

### 1. Backend Setup (Flask)
```bash
# Navigate to the backend folder
cd backend
# Install Python dependencies
pip install flask psycopg2-binary flask-cors
# Configure Database
# Update the DB_CONNECTION_STRING in app.py with your local Postgres credentials.
# Run the Server
python app.py
```
### 2.Frontend Setup (SvelteKit)
```bash
# Navigate to the frontend folder
cd frontend
# Install dependencies
npm install
# Start the development server
npm run dev
```
