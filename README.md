# Prospera Contact Application

The **Prospera Inquiry Portal** is a provides a public facing portal for institutional stakeholders to submit inquiries, alongside a secure administrative dashboard to review and manage incoming submissions.


## Features
- **Public Inquiry Form:** Allows users/partners to submit inquiries.
- **Admin Authentication:** Simple login system to secure management tools.
- **Full CRUD Functionality:** Authenticated admins can Read, Update, and Delete contact submissions.

## Tech Stack
- **Backend:** Python (FastAPI, SQLite)
- **Frontend:** HTML5, Tailwind CSS, JavaScript (Fetch API)

## How to Run Locally

### Prerequisites
* Python 3.9+ installed on your system.

### Setup Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/salsabilaf19/prospera-contact-directory.git
   cd prospera-contact-directory

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    # On Windows use: venv\Scripts\activate

3. Install dependencies:
    ```bash
    pip install fastapi uvicorn "pydantic[email-validator]"

4. Start the development server:
    ```bash
    uvicorn main:app --reload
    (Note: The SQLite database file contacts.db will automatically be generated on application startup).
    
5. Access the application:
    Open your browser and navigate to http://127.0.0.1:8000

🔐 Admin Credentials
* Username: admin
* Password: password123