# 🏕️ Summer Camp Registration System

This project is a Django-based web application for managing registrations, waitlists, and email communications for Regent University's summer camp program.

---

## ✅ How to Run the Project Locally

### 1. Open the Project in Visual Studio Code
- Open **Visual Studio Code**
- Select `File > Open Folder...`
- Choose the folder named `Riley test files`
- Make sure you see `manage.py` in the file tree

### 2. Activate the Virtual Environment
```bash
.\env\Scripts\activate
```
You should see `(env)` in your terminal prompt after running the above command.

### 3. Run the Django Server
```bash
python manage.py runserver
```
Once the server is running, open a browser and go to:  
- [Admin Panel](http://127.0.0.1:8000/admin/)  
- [Registration Page](http://127.0.0.1:8000/register/)

---

## 🔐 Default Admin Credentials
- **Username:** riley  
- **Password:** 1234

You can also create your own admin account:
```bash
python manage.py createsuperuser
```

---

## 📝 Notes
- The virtual environment must be activated each time you open a new terminal session.
- If you get an error like `ModuleNotFoundError: No module named 'django'`, activate the virtual environment again.
- All necessary files are already configured in the repo—no need to reinstall Django or start from scratch.

---

Made by Trenten Podach, John Parker, and Riley Pence  
[GitHub Repo](https://github.com/TrentenPodach/summercampsystemCSCI450)