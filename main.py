import sqlite3
from typing import Optional
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, EmailStr

app = FastAPI(title="Prospera Contact Form App")

# --- DATABASE SETUP ---
DB_NAME = "contacts.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            institution TEXT NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            status TEXT DEFAULT 'Pending'
        )
    """)
    conn.commit()
    conn.close()

# Run database creation on startup
init_db()

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

# --- SCHEMAS ---
class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    institution: str
    subject: str
    message: str

class ContactUpdate(BaseModel):
    name: str
    email: EmailStr
    institution: str
    subject: str
    message: str
    status: str

class LoginRequest(BaseModel):
    username: str
    password: str

# --- AUTHENTICATION HELPERS ---
HARDCODED_USER = "admin"
HARDCODED_PASS = "password123"
SECRET_TOKEN = "prospera-demo-admin-token-2026"

def verify_token(x_auth_token: Optional[str] = Header(None)):
    if x_auth_token != SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized access")
    return True

# --- API ROUTES ---

@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("index.html", "r") as f:
        return f.read()

@app.post("/api/login")
def login(credentials: LoginRequest):
    if credentials.username == HARDCODED_USER and credentials.password == HARDCODED_PASS:
        return {"token": SECRET_TOKEN, "message": "Login successful"}
    raise HTTPException(status_code=400, detail="Invalid username or password")

# PUBLIC: Create Contact Submission
@app.post("/api/contacts", status_code=201)
def create_contact(contact: ContactCreate, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO contacts (name, email, institution, subject, message) VALUES (?, ?, ?, ?, ?)",
        (contact.name, contact.email, contact.institution, contact.subject, contact.message)
    )
    db.commit()
    return {"message": "Contact form submitted successfully!"}

# PROTECTED (CRUD): Read All Contacts
@app.get("/api/contacts")
def get_contacts(authenticated: bool = Depends(verify_token), db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM contacts ORDER BY id DESC")
    rows = cursor.fetchall()
    return [dict(row) for row in rows]

# PROTECTED (CRUD): Update Contact
@app.put("/api/contacts/{contact_id}")
def update_contact(contact_id: int, contact: ContactUpdate, authenticated: bool = Depends(verify_token), db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(
        "UPDATE contacts SET name=?, email=?, institution=?, subject=?, message=?, status=? WHERE id=?",
        (contact.name, contact.email, contact.institution, contact.subject, contact.message, contact.status, contact_id)
    )
    db.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Contact entry not found")
    return {"message": "Contact entry updated successfully"}

# PROTECTED (CRUD): Delete Contact
@app.delete("/api/contacts/{contact_id}")
def delete_contact(contact_id: int, authenticated: bool = Depends(verify_token), db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
    db.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Contact entry not found")
    return {"message": "Contact entry deleted successfully"}