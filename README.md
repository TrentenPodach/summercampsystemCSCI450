# 🏕️ Summer Camp Registration System - Starter Guide

Welcome! This project is a Django-based web app for managing summer camp registrations.

----------------------------------------
## QUICK START INSTRUCTIONS
----------------------------------------

### 1. Clone the Repository
```
git clone https://github.com/TrentenPodach/summercampsystemCSCI450.git
cd summercampsystemCSCI450
```

### 2. Set Up the Project

If you are on Windows:
- Run the file: winmake.bat
- Choose:
  1 → Setup
  2 → Run the server

If you are on Mac/Linux:
- Use the terminal:
  make setup
  make run

### 3. Open the Application
- Admin Panel: http://127.0.0.1:8000/admin/
- Registration Page: http://127.0.0.1:8000/register/

Default Admin Login:
- Username: riley
- Password: 1234

----------------------------------------
## COMANDS
----------------------------------------

| Task                     | Windows Command     | Mac/Linux Command  |
|---------------------------|----------------------|--------------------|
| Setup environment         | winmake.bat → 1      | make setup         |
| Run Django server         | winmake.bat → 2      | make run           |
| Freeze dependencies       | winmake.bat → 3      | make freeze        |
| Delete virtual environment| winmake.bat → 4      | make clean         |

----------------------------------------
## NOTES
----------------------------------------

- If you install new Python packages, update the requirements.txt by using the Freeze option.
- Always activate your virtual environment if running Django manually:
  - Windows: .\env\Scripts\activate
  - Mac/Linux: source env/bin/activate

----------------------------------------

Created by: Trenten Podach, John Parker, and Riley Pence
GitHub Repo: https://github.com/TrentenPodach/summercampsystemCSCI450
