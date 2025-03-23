# from dotenv import load_dotenv
# from fastapi import FastAPI, HTTPException, Request, Depends
# import google.generativeai as genai
# import chromadb
# import mysql.connector
# import os

# # Load environment variables
# load_dotenv()

# # Initialize FastAPI app
# app = FastAPI()

# # Configure Google API Key
# api_key = os.getenv("GOOGLE_API_KEY")
# if not api_key:
#     raise ValueError("GOOGLE_API_KEY environment variable is not set.")
# genai.configure(api_key=api_key)

# # MySQL connection details
# MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
# MYSQL_USER = os.getenv("MYSQL_USER", "root")
# MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "gym")
# MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "diet_chatbot")

# # MySQL connection dependency
# def get_db():
#     """Dependency to get a MySQL database connection."""
#     conn = mysql.connector.connect(
#         host=MYSQL_HOST,
#         user=MYSQL_USER,
#         password=MYSQL_PASSWORD,
#         database=MYSQL_DATABASE
#     )
#     try:
#         yield conn
#     finally:
#         conn.close()

# # Store user details endpoint
# @app.post("/store_user/")
# async def store_user(request: Request, db: mysql.connector.connection.MySQLConnection = Depends(get_db)):
#     """Store user details in the database."""
#     data = await request.json()
    
#     try:
#         cursor = db.cursor()
#         cursor.execute("""
#             INSERT INTO users (name, age, weight, height, goal, diet_preference)
#             VALUES (%s, %s, %s, %s, %s, %s)
#         """, (data['name'], data['age'], data['weight'], data['height'], data['goal'], data['diet_preference']))

#         db.commit()
#         cursor.close()
#         return {"message": "User information stored successfully!"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# # Connect to ChromaDB (Vector DB)
# try:
#     chroma_client = chromadb.PersistentClient(path="./chroma_db")
#     collection = chroma_client.get_or_create_collection("recipe_embeddings")
# except Exception as e:
#     print("❌ ERROR: ChromaDB connection failed:", str(e))

# # Home endpoint
# @app.get("/")
# def home():
#     """Home endpoint."""
#     return {"message": "Welcome to the Diet Chatbot API! Use /docs to explore endpoints."}

# # Get AI recipe endpoint
# @app.get("/get_ai_recipe/")
# def get_ai_recipe(query: str):
#     """Retrieve similar recipes and enhance response using Gemini LLM."""
#     try:
#         # Convert user query into an embedding
#         response = genai.embed_content(model="models/text-embedding-004", content=query)
#         query_embedding = response["embedding"]

#         # Retrieve similar recipes from ChromaDB
#         results = collection.query(query_embeddings=[query_embedding], n_results=3)

#         # If no results found
#         if not results["metadatas"]:
#             return {"message": "No matching recipes found. Try another search!"}

#         recipes = results["metadatas"]

#         # Generate detailed response using Gemini
#         model = genai.GenerativeModel("gemini-1.5-pro-latest")
#         gemini_response = model.generate_content(f"""
#         The user is looking for a recipe similar to: '{query}'.
#         Based on our database, here are similar recipes:
#         {recipes}
#         Please provide a detailed response with:
#         1. Recipe explanation
#         2. Step-by-step cooking instructions
#         3. Nutritional insights
#         4. Possible ingredient replacements
#         5. Cooking tips
#         """)

#         return {"AI_Response": gemini_response.text}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# # Ask AI endpoint
# @app.get("/ask_ai/")
# def ask_ai(question: str):
#     """Answer follow-up questions using Gemini."""
#     try:
#         model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
#         ai_response = model.generate_content(f"The user asked: '{question}' about a recipe. Provide a concise, expert response.")

#         return {"AI_Answer": ai_response.text}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
import google.generativeai as genai
import chromadb
import os

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Configure Google API Key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable is not set.")
genai.configure(api_key=api_key)

# Connect to ChromaDB (Vector DB)
try:
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    collection = chroma_client.get_or_create_collection("recipe_embeddings")
except Exception as e:
    print("❌ ERROR: ChromaDB connection failed:", str(e))

# Home endpoint
@app.get("/")
def home():
    """Home endpoint."""
    return {"message": "Welcome to the Diet Chatbot API! Use /docs to explore endpoints."}

# Get AI recipe endpoint
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

        # Generate detailed response using Gemini
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

# Ask AI endpoint
@app.get("/ask_ai/")
def ask_ai(question: str):
    """Answer follow-up questions using Gemini."""
    try:
        model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
        ai_response = model.generate_content(f"The user asked: '{question}' about a recipe. Provide a concise, expert response.") 

        return {"AI_Answer": ai_response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
