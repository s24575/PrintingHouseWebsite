from pydantic import BaseModel, EmailStr
from datetime import date, datetime


class AddressModel(BaseModel):
    address_id: int
    country: str
    voivodeship: str
    powiat: str
    gmina: str
    city: str
    postal_code: str
    street: str
    house_number: str
    apartment_number: str | None


class CompanyDetailModel(BaseModel):
    company_details_id: int
    user_id: int
    address_id: int
    name: str
    acronym: str
    bank_name: str
    bank_account_number: str
    nip: str
    regon: str
    phone_number: str
    email: EmailStr
    discount_percentage: float
    is_archived: bool
    created_at: datetime
    modified_at: datetime


class DictionaryModel(BaseModel):
    dictionary_id: int
    key: str
    value: str


class InvoiceItemModel(BaseModel):
    invoice_item_id: int
    invoice_id: int
    item_description: str
    quantity: int
    unit_price: float
    total_price: float
    vat_rate: float
    item_item_id: int


class InvoiceModel(BaseModel):
    invoice_id: int
    order_order_id: int
    company_details_id: int
    billing_address_id: int
    invoice_number: str
    issue_date: date
    due_date: date
    total_amount: float
    vat_rate: float
    is_archived: bool
    created_at: datetime
    modified_at: datetime


class ItemOptionModel(BaseModel):
    item_option_id: int
    item_id: int
    option_id: int


class ItemModel(BaseModel):
    item_id: int
    product_id: int
    order_id: int | None
    cart_user_id: int | None
    quantity: int
    price: float
    user_comment: str


class OptionGroupModel(BaseModel):
    option_group_id: int
    product_id: int
    name: str
    type: str
    title: str
    is_mandatory: bool


class OptionModel(BaseModel):
    option_id: int
    option_group_id: int
    name: str
    price_increment: float


class OrderModel(BaseModel):
    order_id: int
    user_id: int
    delivery_address_id: int
    delivery_method: str
    total_price: float
    created_at: datetime
    modified_at: datetime


class ProductModel(BaseModel):
    product_id: int
    sku: str
    name: str
    image_url: str
    description: str
    base_price: float
    weight: float
    is_archived: bool
    created_at: datetime
    modified_at: datetime


class UserModel(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    created_at: datetime
    modified_at: datetime
