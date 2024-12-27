from pydantic import BaseModel

from common.models import ProductModel


class CreateProductData(BaseModel):
    name: str
    image_url: str
    description: str
    price: float
    sku: str
    weight: float


class ProcessSelectedOptionsData(BaseModel):
    selected_options: dict[int, int]


class ProcessSelectedOptionsResponse(BaseModel):
    price: float


class MultipleProductsResponse(BaseModel):
    products: list[ProductModel]


class SingleProductResponse(BaseModel):
    products: list[ProductModel]


class ProductDetailsResponse(BaseModel):
    product: ProductModel
    all_options: dict
