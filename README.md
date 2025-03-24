# Study Planner

## 📌 Overview
The **Study Planner** is a Django-based web application designed to help students and faculty efficiently plan and track study schedules. It provides functionalities for students to manage tasks and deadlines while allowing faculty to assign schedules and monitor student progress.

## 🚀 Features
### 🔹 User Management
- Custom authentication system with separate **Student** and **Faculty** roles.
- Admin approval system for user registrations.

### 📅 Study Planning
- Students can set study goals and track progress.
- Faculty can assign schedules, post deadlines, and provide remarks on student progress.

### 📂 Syllabus Management
- Admins can upload and manage syllabus files.

### 🔔 Notifications
- Alerts for upcoming deadlines and faculty-assigned tasks.

## 🛠️ Tech Stack
- **Backend:** Django (Python)
- **Database:** SQLite (default) - can be replaced with PostgreSQL/MySQL if needed
- **Frontend:** Django Templates (HTML, CSS, Bootstrap)

## 📂 Project Structure
```
main_project/
│── admin_panel/        # Admin functionalities like approval & syllabus management
│── study_planner/      # Core study planning logic
│── users/              # Custom user model and authentication
│── templates/          # HTML templates
│── static/             # CSS, JS, Images
│── db.sqlite3          # Database (default)
│── manage.py           # Django management script
```

## ⚡ Setup Instructions
### 1️⃣ Clone the Repository
```sh
git clone https://github.com/NehaV7613/study_planner.git
cd study_planner
```
### 2️⃣ Create and Activate a Virtual Environment
```sh
python -m venv mainenv  # Create virtual environment
source mainenv/bin/activate  # On Mac/Linux
mainenv\Scripts\activate  # On Windows
```
### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```
### 4️⃣ Apply Migrations
```sh
python manage.py migrate
```
### 5️⃣ Create a Superuser (Admin)
```sh
python manage.py createsuperuser
```
### 6️⃣ Run the Server
```sh
python manage.py runserver
```
Access the app at **http://127.0.0.1:8000/**

## 📜 Future Enhancements
- ✅ AI-based personalized study plan generator
- 📊 Graphical representation of study progress
- 🔄 API integration for mobile support

---
💡 **Contributions & Feedback**
Feel free to fork, contribute, or report issues to improve the Study Planner! 😊

