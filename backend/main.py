from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from openai import OpenAI
import os

app = FastAPI()

# Initialize the OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
  # Replace with your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure OpenAI API (you'll need to set up your API key)
# openai.api_key = "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"

class SearchQuery(BaseModel):
    query: str

class Pokemon(BaseModel):
    id: int
    name: str
    image: str
    description: str

class SearchResponse(BaseModel):
    found: bool
    pokemon: Optional[Pokemon] = None

@app.post("/api/search", response_model=SearchResponse)
async def search_pokemon(search_query: SearchQuery):
    try:
        # Use OpenAI's GPT to process the query
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that processes Pokemon search queries."},
                {"role": "user", "content": f"Process this Pokemon search query: {search_query.query}"}
            ]
        )
        
        processed_query = response.choices[0].text.strip()
        
        # TODO: Implement actual Pokemon search logic here
        # For now, we'll just return a mock response
        if "pikachu" in processed_query.lower():
            return SearchResponse(
                found=True,
                pokemon=Pokemon(
                    id=25,
                    name="Pikachu",
                    image="https://example.com/pikachu.png",
                    description="An Electric-type Pokémon"
                )
            )
        else:
            return SearchResponse(found=False)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8880)



