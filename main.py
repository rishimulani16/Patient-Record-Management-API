from fastapi import FastAPI, Path, HTTPException, Query
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field,field_validator
from typing import List, Dict, Optional, Annotated, Literal

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description = "ID of the patient", example="P001")]
    name: Annotated[str, Field(..., description = "Name of the patient")]
    city: Annotated[str, Field(..., description = "City of the patient")]
    age: Annotated[int, Field(..., description = "Age of the patient", gt=0, lt=150)]
    gender: Annotated[Literal['Male', 'Female', 'Other'], Field(..., description = "Gender of the patient")]
    height: Annotated[float, Field(..., description = "Height of the patient in meters", gt=0)]
    weight: Annotated[float, Field(..., description = "Weight of the patient in kilograms", gt=0)]

    @field_validator('gender')
    @classmethod 
    def transform_name(cls, value):
        return value.lower()

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 24.9:
            return "Normal weight"
        elif 25 <= self.bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity" 
        

class PatientUpdate (BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0, lt=150)]
    gender: Annotated[Optional[Literal['Male', 'Female', 'Other']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]
        
#load existing data from json file      
def load_data():
    with open('patients.json') as f:
        data = json.load(f)
    return data

#save data to json file
def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)


@app.get("/") 
def hello():
    return {"message": "Patient Management API"}

@app.get("/about") 
def about():
    return {"message": "Fully functional Patient Management API using FastAPI to manage patient records."}

@app.get("/view")
def view():
    data = load_data()
    return data


#Sorting patients
#For test this: /sort?sort_by=height&order=desc
@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description="Sort on the basis of height, weight or bmi"), order: str = Query('asc', description="Order can be asc or desc")):
    
    valid_fields = ['height', 'weight', 'bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort_by field. Must be one of {valid_fields}")
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid order. Must be 'asc' or 'desc'")
    
    data = load_data()
    sort_order = True if order == 'desc' else False

    sorted_data =sorted(data.values(), key = lambda x: x[sort_by], reverse=sort_order)
    return sorted_data


@app.get("/patient/{patient_id}") #path parameter
def view_patient(patient_id: str = Path(..., description="ID of patient in DB", example="P001")): #specify path parameter details
    #load all the patient
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    # return {"message": "Patient not found"}
    raise HTTPException(status_code= 404, detail="patient not found") #HTTP exception for better error handling

        
@app.post("/create")
def create_patient(patient: Patient):
    
    # Load existing data
    data = load_data()

    # Check if patient ID already exists
    if patient.id in data:
        raise HTTPException(status_code = 400, detail = "Patient ID already exists")

    # new patient data base
    data[patient.id] = patient.model_dump(exclude = ['id']) #we had convert the patient model to dictionary and exclude id field because id is key in json file

    # Save updated data
    save_data(data)

    return JSONResponse(status_code=201, content={"message": "Patient created successfully"}) 

@app.put("/update/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code = 404, detail="Patient not found")
        
    existing_patient_info = data[patient_id]

    patient_update_dict = patient_update.model_dump(exclude_unset=True) #get only the fields that are provided in the update request

    for key, value in patient_update_dict.items():
        existing_patient_info[key] = value

    patient_pydantic_obj = Patient(id=patient_id, **existing_patient_info) #recreate the patient object to recalculate bmi and verdict if height or weight is updated

    existing_patient_info = patient_pydantic_obj.model_dump(exclude=['id'])
    
    data[patient_id] = existing_patient_info

    save_data(data)

    return JSONResponse(status_code=200, content={"message": "Patient updated successfully"})

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code = 404, detail="Patient not found")
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={"message": "Patient deleted successfully"})