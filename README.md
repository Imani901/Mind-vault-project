### 🧠 MindVault - Personal Knowledge Tracker
MindVault is a full-stack personal knowledge tracker that helps you capture, review, and organize knowledge using spaced repetition and tags. It features user authentication, card creation, editing, search/filter, and review scheduling.

### 📁 Project Structure
bash
Copy
Edit
mindvault/
├── client/         # React Frontend
└── server/         # Flask Backend API
🔥 Backend - Flask API
📍 Location: server/
### 🚀 Features
JWT-based User Authentication

CRUD for Knowledge Cards

Tag-based Search & Filtering

Spaced Repetition Logic

CORS Support for Frontend

### ⚙️ Tech Stack
Flask + Flask-RESTful

Flask-JWT-Extended

SQLAlchemy

PostgreSQL

Marshmallow (for serialization)

### 📦 Setup Instructions
cd server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
### 🔑 Environment Variables (Create a .env file or set in environment)
JWT_SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://username:password@localhost:5432/mindvault_db
FLASK_ENV=development
### 🔧 Run Locally
flask db init
flask db migrate
flask db upgrade
flask run
### 📮 API Endpoints
/register	POST	Create a new user
/login	POST	Authenticate and receive JWT
/cards	GET	Get user’s knowledge cards
/cards	POST	Create a new card
/cards/<id>	PATCH	Update a card
/cards/<id>	DELETE	Delete a card
/cards/<id>/review	PATCH	Review a card (spaced logic)
/dashboard/summary	GET	Get dashboard metrics


### 💻 Frontend - React
## 📍 Location: client/
# 🎯 Features
-Login & Register
-Dashboard with Review Stats
-Create/Edit/Delete Cards
-Search & Filter by Tag
-Beautiful Responsive UI

## ⚙️ Tech Stack
-React (with Hooks)
-Axios for HTTP requests
-React Router
-JWT storage via localStorage
-Custom styling with CSS

### 📦 Setup Instructions
cd client
npm install
### 🔧 Run Locally
npm start
By default, runs on: http://localhost:3000

### 🌍 Connect to Backend
In client/src/services/api.js, set your backend base URL:
const instance = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL || "http://localhost:5555",
  headers: {
    "Content-Type": "application/json",
  },
});
### 🔑 Add Environment Variable in .env
REACT_APP_API_BASE_URL=http://localhost:5555


### 📌 To-Do / Future Enhancements
📊 Analytics Dashboard (review streaks, mastery level)

🏷️ Tag Management Interface

📂 Card Import/Export (CSV, Markdown)

📎 Attachments support (images, files)

🔔 Review Notifications

### 🧑‍💻 Author
Made with 💙 by Faith Henu

