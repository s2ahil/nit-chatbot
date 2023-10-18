from fastapi import FastAPI, Form, Body
from pydantic import BaseModel
import google.generativeai as palm
from typing import Annotated

from fastapi.middleware.cors import CORSMiddleware
# Configure the Palm library with your API key
palm.configure(api_key='AIzaSyA-LiZDpliZS0DWEbluHyJTbJ28XPb1d1A')

# Use the palm.list_models function to find available models:
models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def first():
    return {"message": "Hello, World!"}


@app.post("/")
def generate_text(request_data:Annotated[str, Form()]):
    p = request_data
    completion = palm.generate_text(
        model=model,
        prompt=p,
        temperature=0,
        max_output_tokens=200,
    )

    return {"generated_text": completion.result}


# You can run this FastAPI application using Uvicorn:
# uvicorn your_module_name:app --host 0.0.0.0 --port 8000
