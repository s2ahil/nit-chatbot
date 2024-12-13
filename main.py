from fastapi import FastAPI, Form, HTTPException
from pydantic import BaseModel
from typing import Annotated
from mtranslate import translate
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai

# Configure the GenAI library with your API key
genai.configure(api_key="AIzaSyAz_D5tOqMFTdtmp-N-Yeu3DpHVXXI5Pv4")
model = genai.GenerativeModel("gemini-1.5-flash")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def first():
    return {"message": "Hello, World!"}

@app.post("/")
def generate_text(request_data: Annotated[str, Form()]):
    try:
        p = request_data
        response = model.generate_content(p)
        return {"generated_text": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating text: {str(e)}")

class Input(BaseModel):
    request_data: str

@app.post("/json")
def generate_text_with_translation(request_data: Input):
    try:
        # Translate input prompt to English
        prompt = request_data.request_data
        translated_prompt = translate(prompt, "en")
        
        # Generate response
        response = model.generate_content(translated_prompt)
        english_text = response.text
        
        # Translate response to Hindi
        hindi_translation = translate(english_text, "hi")

        return {
            "generated_text": english_text,
            "hindi_translation": hindi_translation
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")
