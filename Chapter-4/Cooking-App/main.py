import uuid
from pydantic import BaseModel
from sanic import Sanic, Request, json, exceptions, HTTPResponse
from sanic_ext import Extend,openapi
from enum import Enum
import json
import os
from datetime import datetime
import csv
import io


app = Sanic("Cooking-App")

Extend(app)

DATA_FILE = 'recipes.json'

class CategoryEnum(str, Enum):
    BREAKFAST = "Breakfast",
    LAUNCH = "Launch",
    DRINK = "Drink",
    DESSERT = "Dessert"

class ExportType(str, Enum):
    CSV = "CSV",
    JSON = "JSON"

class CreateModel(BaseModel):
    title: str
    category: CategoryEnum
    description: str
    estimated_time: int
    difficulty: int
    ingredients: list

class OriginModel(CreateModel):
    id : str

def save_recipes(recipes):
    with open(DATA_FILE, 'w',encoding='utf-8') as f:
        json.dump(recipes, f, ensure_ascii=False, indent=2)

def load_recipes():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE,'r',encoding='utf-8') as f:
            recipes = json.load(f)
            if isinstance(recipes, list):
                return recipes
            else:
                return []
    except (json.decoder.JSONDecodeError , Exception):
        return []


@app.post("/recipes")
@openapi.body(CreateModel)
async def recipes_create(request: Request):
    data = request.json
    recipe = CreateModel(**data)
    new_recipe = {
        "id":str(uuid.uuid4()),
        "title": recipe.title,
        "category": recipe.category.value,
        "description": recipe.description,
        "estimated_time": recipe.estimated_time,
        "difficulty": recipe.difficulty,
        "ingredients": recipe.ingredients,
    }
    recipes = load_recipes()
    recipes.append(new_recipe)
    save_recipes(recipes)
    return json({"detail":"Task has been created"})

@app.get("/recipes")
async def get_recipes(request: Request):
    recipes = load_recipes()
    return json(recipes)

@app.get("/recipes/<recipe_id>")
async def get_recipe(request: Request, recipe_id: str):
    recipes = load_recipes()
    for recipe in recipes:
        if recipe["id"] == recipe_id:
            return json(recipe)
    raise exceptions.NotFound("Recipe not found")

@app.put("/recipes/<recipe_id>")
@openapi.body(CreateModel)
async def update_recipe(request: Request, recipe_id: str):
    recipe_ser = CreateModel(**request.json)
    recipes=  load_recipes()
    for recipe in recipes:
        if recipe["id"] == recipe_id:
            recipe.update({
                    "title": recipe_ser.title,
                    "category": recipe_ser.category.value,
                    "description": recipe_ser.description,
                    "estimated_time": recipe_ser.estimated_time,
                    "difficulty": recipe_ser.difficulty,
                    "ingredients": recipe_ser.ingredients,
            })
            save_recipes(recipes)
            return json(recipe)
    raise exceptions.NotFound("Recipe not found")

@app.delete("/recipes/<recipe_id>")
async def delete_recipe(request: Request, recipe_id: str):
    recipes = load_recipes()
    recipes = [recipe for recipe in recipes if recipe["id"] != recipe_id]
    save_recipes(recipes)
    return json({"detail":"Recipe has been deleted"})


@app.get("/recipes/export/<export_type>")
async def export_recipes(request: Request, export_type: ExportType):
    recipes = load_recipes()
    today = datetime.now().strftime('%Y-%m-%d')

    if export_type == ExportType.JSON:
        # Export as JSON
        return json(recipes)

    elif export_type == ExportType.CSV:
        # Export as CSV

        # 1. Define field names (headers) for the CSV
        fieldnames = ["id", "title", "category", "description", "estimated_time", "difficulty", "ingredients"]

        # 2. Prepare data in memory using StringIO
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames)

        # Write header row
        writer.writeheader()

        # 3. Process and write rows
        for recipe in recipes:
            # Flatten ingredients list to a single string for CSV compatibility
            row = {
                "id": recipe.get("id", ""),
                "title": recipe.get("title", ""),
                "category": recipe.get("category", ""),
                "description": recipe.get("description", ""),
                "estimated_time": recipe.get("estimated_time", ""),
                "difficulty": recipe.get("difficulty", ""),
                "ingredients": ", ".join(recipe.get("ingredients", []))  # Join list into string
            }
            writer.writerow(row)

        # 4. Create response with necessary headers for download
        csv_data = output.getvalue()
        response = HTTPResponse(body=csv_data, status=200)

        # Set headers for file download
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = f'attachment; filename="recipes_{today}.csv"'

        return response

    else:
        # Should not happen if ExportType enum is used correctly, but good for safety
        raise exceptions.InvalidUsage(f"Invalid export type specified: {export_type}")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000,debug=True)






