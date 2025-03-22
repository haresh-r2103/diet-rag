from fastapi import FastAPI, HTTPException
import google.generativeai as genai
import chromadb
import os

load_dotenv()

app = FastAPI()

# ✅ Configure Google API Key
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key) # Replace with actual key

# ✅ Connect to ChromaDB (Vector DB)
try:
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    collection = chroma_client.get_or_create_collection("recipe_embeddings")
except Exception as e:
    print("❌ ERROR: ChromaDB connection failed:", str(e))

@app.get("/")
def home():
    return {"message": "Welcome to the Diet Chatbot API! Use /docs to explore endpoints."}

@app.get("/get_ai_recipe/")
def get_ai_recipe(query: str):
    """Retrieve similar recipes and enhance response using Gemini LLM."""
    try:
        # Convert user query into an embedding
        response = genai.embed_content(model="models/text-embedding-004", content=query)
        query_embedding = response["embedding"]

        # Retrieve similar recipes from ChromaDB
        results = collection.query(query_embeddings=[query_embedding], n_results=3)

        # If no results found
        if not results["metadatas"]:
            return {"message": "No matching recipes found. Try another search!"}

        recipes = results["metadatas"]

        # ✅ Corrected Gemini API call
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        gemini_response = model.generate_content(f"""
        The user is looking for a recipe similar to: '{query}'.
        Based on our database, here are similar recipes:
        {recipes}
        Please provide a detailed response with:
        1. Recipe explanation
        2. Step-by-step cooking instructions
        3. Nutritional insights
        4. Possible ingredient replacements
        5. Cooking tips
        """)

        return {"AI_Response": gemini_response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.get("/ask_ai/")
def ask_ai(question: str):
    """Answer follow-up questions using Gemini."""
    try:
        model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
        ai_response = model.generate_content(f"The user asked: '{question}' about a recipe. Provide a concise, expert response.")

        return {"AI_Answer": ai_response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

