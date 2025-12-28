# 🏥 Patient Record Management API

A **basic FastAPI project** for managing patient records with BMI calculation and health verdicts. The project demonstrates REST API design, data validation with **Pydantic**, CRUD operations, and JSON file persistence — perfect for learners building practical FastAPI skills.

---

## 🚀 Features

- **Create**, **Read**, **Update**, and **Delete** patient records.  
- Computes **BMI** and assigns a health **verdict** automatically.  
- Supports **sorting** by height, weight, or BMI (ascending or descending).  
- Data is persisted in a simple local JSON file (`patients.json`).  
- Implements **input validation** and exception handling using FastAPI best practices.

---

## 📁 Project Structure

patient-records-api/

├── main.py # Main FastAPI application

├── patients.json # JSON file storing all patient records

└── README.md # Project documentation

---

## ⚙️ Installation & Setup

### 1. Clone the repository

git clone https://github.com/<your-username>/patient-records-api.git

cd patient-records-api

### 2. Create a virtual environment (recommended)
python -m venv env

source env/bin/activate # On macOS/Linux

env\Scripts\activate # On Windows

### 3. Install dependencies
pip install fastapi uvicorn pydantic

### 4. Run the FastAPI app
uvicorn main:app --reload

