from fastapi import FastAPI, Form, Body
from pydantic import BaseModel
import google.generativeai as palm
from typing import Annotated
from mtranslate import translate
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
        max_output_tokens=1000,
    )

    return {"generated_text": completion.result}

class Input(BaseModel):
    request_data: str


@app.post("/json")
def generate_text1(request_data:Input):
    print(request_data)
    prompt = request_data.request_data
    p = translate(prompt, "en")
    # p = request_data.request_data
    
    completion = palm.generate_text(
        model=model,
        prompt=p,
        temperature=0,
        max_output_tokens=1000,
    )
    # Set your English text
    english_text = completion.result

# Translate the English text to Hindi
    hindi_translation = translate(english_text, "hi")

    return {"generated_text": completion.result,"hindi_translation": hindi_translation}

# You can run this FastAPI application using Uvicorn:
# uvicorn your_module_name:app --host 0.0.0.0 --port 8000
