from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from make_call import make_vapi_call  # Ensure correct import

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any domain
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

class ContactRequest(BaseModel):
    name: str
    phone: str
    email: str

@app.post("/submit")
async def submit_contact(request: ContactRequest):
    try:
        result = make_vapi_call(request.name, request.phone, request.email)
        return {"message": "Form submitted successfully!", "call_result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
