from pydantic import BaseModel
    
# define model for post request.
class ModelParams(BaseModel):
    Hospital_code: int
    Hospital_type_code: str
    City_Code_Hospital: int
    Hospital_region_code: str
    Available_Extra_Rooms: int
    Department: str
    Ward_Type: str
    Ward_Facility_Code: str
    Bed_Grade: int
    City_Code_Patient: int
    Type_of_Admission: str
    Severity_of_Illness: str
    Visitors_with_Patient: int
    Age: str
    Admission_Deposit: float
