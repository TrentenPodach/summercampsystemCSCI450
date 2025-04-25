# Windows-specific Makefile
VENV_DIR=env

# Create virtual environment and install dependencies
setup:
	@echo "Creating virtual environment if missing..."
	@if not exist "$(VENV_DIR)" python -m venv $(VENV_DIR)
	@echo "Activating virtual environment and installing requirements..."
	@cmd /c "$(VENV_DIR)\Scripts\activate && pip install -r requirements.txt"

# Run the Django server
run:
	@echo "Starting Django development server..."
	@cmd /c "$(VENV_DIR)\Scripts\activate && python manage.py runserver"

# Remove virtual environment
clean:
	@echo "Deleting virtual environment..."
	@if exist "$(VENV_DIR)" rmdir /s /q $(VENV_DIR)

# Freeze current packages into requirements.txt
freeze:
	@cmd /c "$(VENV_DIR)\Scripts\activate && pip freeze > requirements.txt"
