# DeepBlue - Statistics Dashboard
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://statdbl.streamlit.app/)

# 📊 Local Setup & Running the App

## 🛠️ One-Time Environment Setup

To set up the virtual environment and install dependencies (only required the first time), run the following commands from the root of the project:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

This will create a `.venv` directory with an isolated Python environment and install all required packages.

---

## 🚀 Running the Streamlit Application

Each time you want to run the app:

1. Activate the virtual environment:

```bash
.venv\Scripts\activate
```

2. Start the Streamlit application:

```bash
streamlit run main.py
```

---

## ⚠️ Notes

- Make sure you have **Python 3.8 or higher** installed.
- If you encounter permission issues in PowerShell when activating the virtual environment, run the following command:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

- To deactivate the environment:

```bash
deactivate
```
