from fastapi import FastAPI,status,Path,Query
from fastapi_swagger import patch_fastapi
from typing import Optional,List
import uuid
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from pydantic import BaseModel

app = FastAPI(docs_url=None,swagger_ui_oauth2_redirect_url=None)
patch_fastapi(app,docs_url="/swagger")

class ProductCreateModel(BaseModel):
    name: str
    price: float
class ProductModel(ProductCreateModel):
    id : str

products = []

@app.get("/products",response_model=List[ProductModel])
async def get_all_products(max_price: Optional[int] = Query(None,
                                                            description=
                                                            "Maximum price for filtering")):
    if max_price is None:
        return JSONResponse({"products": products},status_code=status.HTTP_200_OK)
    else:
        filtered_products = [product for product in products if product["price"] <= max_price]
        return JSONResponse({"products": filtered_products}, status_code=status.HTTP_200_OK)

@app.post("/products")
async def create_product(request_data: ProductCreateModel):
    products.append({
        "id": str(uuid.uuid4()),
        "name": request_data.name,
        "price": request_data.price,
    })
    return JSONResponse({"detail":"Product created successfully"},
                        status_code=status.HTTP_201_CREATED)

@app.get("/products/{product_id}")
async def get_product(product_id):
    for product in products:
        if product["id"] == product_id:
            return product
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Product not found")

@app.put("/products/{product_id}")
async def update_product(request_data: ProductCreateModel,product_id:str=Path()):
    for product in products:
        if product["id"] == product_id:
            product["price"] = request_data.price,
            product["name"] = request_data.name,
            return product
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Product not found")

@app.delete("/products/{product_id}")
async def delete_product(product_id):
    global products
    products = [product for product in products if product["id"] != product_id]
    return JSONResponse({},status_code=status.HTTP_204_NO_CONTENT)
