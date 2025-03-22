import fitz  # PyMuPDF
import json

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF and structure it as JSON."""
    doc = fitz.open(pdf_path)
    recipes = []
    
    current_recipe = {}
    for page in doc:
        text = page.get_text("text").strip()
        lines = text.split("\n")
        
        for line in lines:
            if any(keyword in line for keyword in ["Yield", "Ingredients", "Instructions"]):
                if current_recipe:
                    recipes.append(current_recipe)
                current_recipe = {"recipe_name": line.strip()}
            elif line.startswith("Yield:"):
                current_recipe["yield"] = line.replace("Yield:", "").strip()
            elif line.startswith("Ingredients:"):
                current_recipe["ingredients"] = []
            elif line.startswith("Instructions:"):
                current_recipe["instructions"] = []
            elif "ingredients" in current_recipe and line.strip():
                current_recipe["ingredients"].append(line.strip())
            elif "instructions" in current_recipe and line.strip():
                current_recipe["instructions"].append(line.strip())

    if current_recipe:
        recipes.append(current_recipe)
    
    return recipes

# Extract and save recipes
pdf_path = "DietPDF.pdf"
recipe_data = extract_text_from_pdf(pdf_path)

with open("recipes.json", "w") as f:
    json.dump(recipe_data, f, indent=4)

print("✅ Recipes extracted and saved to recipes.json")
