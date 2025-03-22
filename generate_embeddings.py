import json
import google.generativeai as genai
import chromadb

# Configure Google API Key
genai.configure(api_key="AIzaSyCC6EtXOk_ir4sPxVVDNuAE5Y27oNLmd1A")  # Replace with your actual API key

# Load recipes from JSON file
with open("recipes.json", "r") as f:
    recipes = json.load(f)

# Initialize ChromaDB Persistent Client
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("recipe_embeddings")

# Process and store embeddings
for recipe in recipes:
    recipe_name = recipe.get("recipe_name", "Unknown Recipe")
    ingredients = ", ".join(recipe.get("ingredients", []))
    instructions = " ".join(recipe.get("instructions", []))
    
    # Create recipe description for embedding
    text = f"{recipe_name}. Ingredients: {ingredients}. Instructions: {instructions}"
    
    # Generate embedding using Google AI
    try:
        response = genai.embed_content(model="models/text-embedding-004", content=text)
        embedding = response["embedding"]
    except Exception as e:
        print(f"❌ Failed to embed {recipe_name}: {e}")
        continue  # Skip to next recipe if embedding fails

    # Handle missing nutrient data
    nutrients = recipe.get("nutrient_content", {
        "calories": "N/A", "protein": "N/A", "carbs": "N/A", "fat": "N/A"
    })

    # Store embedding in ChromaDB
    try:
        collection.add(
            ids=[recipe_name], 
            embeddings=[embedding], 
            metadatas=[{
                "recipe_name": recipe_name, 
                "nutrients": json.dumps(nutrients)  # Convert dict to string
            }]
        )
        print(f"✅ Successfully stored embedding for {recipe_name}")
    except Exception as e:
        print(f"❌ Failed to store embedding for {recipe_name}: {e}")

print("✅ All recipe embeddings stored successfully in ChromaDB.")
