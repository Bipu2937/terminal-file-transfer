📦 Terminal File Transfer App

A lightweight, password-protected offline file sharing and text messaging tool built with Flask.
Designed to run locally on your phone or computer with a retro terminal-style web UI.


---

🚀 Features

🗂️ File Upload & Download
Upload one or more files via drag & drop or file picker.

🧾 Send & Save Text Notes
Type and store messages to a shared log file.

📁 Public File Sharing
Move files to a shared/ folder to make them available at /shared.

🔐 Password Protection
Only authorized users can access the dashboard.

🌐 LAN Access or Public IP Compatible
Devices on the same network can access via IP, or expose publicly via port forwarding or Ngrok.

🖥️ Terminal-Inspired UI
Built with retro green-on-black styling for hackers and nostalgia lovers.



---

🛠️ Setup

1. Clone the repo:

git clone https://github.com/your-username/terminal-transfer-app.git
cd terminal-transfer-app


2. Install dependencies:
*install python in you mechine first*

pip install flask


3. Run the app:

python app.py


4. Visit in your browser:

http://localhost:8000
or
http://<your-local-ip>:8000




---

📂 Folder Structure

├── app.py             # Main Flask backend
├── templates/         # HTML views
├── static/            # CSS files
├── uploads/           # Received files and messages
├── shared/            # Publicly downloadable files
└── .gitignore


---

🧠 Customization

Change login password in app.py:

PASSWORD = '1234'

Customize port or add HTTPS support for secure external sharing.



---

🧑‍💻 Author

Made by @mdabusaim
Terminal-style lives forever 💚
