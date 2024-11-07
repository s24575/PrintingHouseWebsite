from sqlalchemy import Enum, DECIMAL, Date, TIMESTAMP

from .db import db


class Address(db.Model):
    __tablename__ = "addresses"
    address_id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(255), nullable=False)
    voivodeship = db.Column(db.String(255), nullable=False)
    powiat = db.Column(db.String(255), nullable=False)
    gmina = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    street = db.Column(db.String(255), nullable=False)
    house_number = db.Column(db.String(255), nullable=False)
    apartment_number = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            "address_id": self.address_id,
            "country": self.country,
            "voivodeship": self.voivodeship,
            "powiat": self.powiat,
            "gmina": self.gmina,
            "city": self.city,
            "postal_code": self.postal_code,
            "street": self.street,
            "house_number": self.house_number,
            "apartment_number": self.apartment_number,
        }


class CompanyDetail(db.Model):
    __tablename__ = "company_details"
    company_details_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    address_id = db.Column(
        db.Integer, db.ForeignKey("addresses.address_id"), nullable=False
    )
    name = db.Column(db.String(255), nullable=False)
    acronym = db.Column(db.String(255), nullable=False)
    bank_name = db.Column(db.String(255), nullable=False)
    bank_account_number = db.Column(db.String(255), nullable=False)
    nip = db.Column(db.String(255), nullable=False)
    regon = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    discount_percentage = db.Column(DECIMAL(5, 2), nullable=False)
    is_archived = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(
        TIMESTAMP, nullable=False, default=db.func.current_timestamp()
    )
    modified_at = db.Column(
        TIMESTAMP,
        nullable=False,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    def to_dict(self):
        return {
            "company_details_id": self.company_details_id,
            "user_id": self.user_id,
            "address_id": self.address_id,
            "name": self.name,
            "acronym": self.acronym,
            "bank_name": self.bank_name,
            "bank_account_number": self.bank_account_number,
            "nip": self.nip,
            "regon": self.regon,
            "phone_number": self.phone_number,
            "email": self.email,
            "discount_percentage": str(self.discount_percentage),
            "is_archived": self.is_archived,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
        }


class Dictionary(db.Model):
    __tablename__ = "dictionary"
    dictionary_id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(255), nullable=False)
    value = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            "dictionary_id": self.dictionary_id,
            "key": self.key,
            "value": self.value,
        }


class InvoiceItem(db.Model):
    __tablename__ = "invoice_items"
    invoice_item_id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(
        db.Integer, db.ForeignKey("invoices.invoice_id"), nullable=False
    )
    item_description = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(DECIMAL(10, 2), nullable=False)
    total_price = db.Column(DECIMAL(10, 2), nullable=False)
    vat_rate = db.Column(DECIMAL(5, 2), nullable=False)
    item_item_id = db.Column(db.Integer, db.ForeignKey("items.item_id"), nullable=False)

    def to_dict(self):
        return {
            "invoice_item_id": self.invoice_item_id,
            "invoice_id": self.invoice_id,
            "item_description": self.item_description,
            "quantity": self.quantity,
            "unit_price": str(self.unit_price),
            "total_price": str(self.total_price),
            "vat_rate": str(self.vat_rate),
            "item_item_id": self.item_item_id,
        }


class Invoice(db.Model):
    __tablename__ = "invoices"
    invoice_id = db.Column(db.Integer, primary_key=True)
    order_order_id = db.Column(
        db.Integer, db.ForeignKey("orders.order_id"), nullable=False
    )
    company_details_id = db.Column(
        db.Integer, db.ForeignKey("company_details.company_details_id"), nullable=False
    )
    billing_address_id = db.Column(
        db.Integer, db.ForeignKey("addresses.address_id"), nullable=False
    )
    invoice_number = db.Column(db.String(50), nullable=False)
    issue_date = db.Column(Date, nullable=False)
    due_date = db.Column(Date, nullable=False)
    total_amount = db.Column(DECIMAL(10, 2), nullable=False)
    vat_rate = db.Column(DECIMAL(5, 2), nullable=False)
    is_archived = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(
        TIMESTAMP, nullable=False, default=db.func.current_timestamp()
    )
    modified_at = db.Column(
        TIMESTAMP,
        nullable=False,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    def to_dict(self):
        return {
            "invoice_id": self.invoice_id,
            "order_order_id": self.order_order_id,
            "company_details_id": self.company_details_id,
            "billing_address_id": self.billing_address_id,
            "invoice_number": self.invoice_number,
            "issue_date": self.issue_date,
            "due_date": self.due_date,
            "total_amount": str(self.total_amount),
            "vat_rate": str(self.vat_rate),
            "is_archived": self.is_archived,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
        }


class ItemOption(db.Model):
    __tablename__ = "item_options"
    item_option_id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.item_id"), nullable=False)
    option_id = db.Column(
        db.Integer, db.ForeignKey("options.option_id"), nullable=False
    )

    def to_dict(self):
        return {
            "item_option_id": self.item_option_id,
            "item_id": self.item_id,
            "option_id": self.option_id,
        }


class Item(db.Model):
    __tablename__ = "items"
    item_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.product_id"), nullable=False
    )
    order_id = db.Column(db.Integer, db.ForeignKey("orders.order_id"), nullable=True)
    cart_user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(DECIMAL(10, 2), nullable=False)
    user_comment = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            "item_id": self.item_id,
            "product_id": self.product_id,
            "order_id": self.order_id,
            "cart_user_id": self.cart_user_id,
            "quantity": self.quantity,
            "price": str(self.price),
            "user_comment": self.user_comment,
        }


class OptionGroup(db.Model):
    __tablename__ = "option_groups"
    option_group_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.product_id"), nullable=False
    )
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(Enum("select", "number"), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    is_mandatory = db.Column(db.Boolean, nullable=False)

    def to_dict(self):
        return {
            "option_group_id": self.option_group_id,
            "product_id": self.product_id,
            "name": self.name,
            "type": self.type,
            "title": self.title,
            "is_mandatory": self.is_mandatory,
        }


class Option(db.Model):
    __tablename__ = "options"
    option_id = db.Column(db.Integer, primary_key=True)
    option_group_id = db.Column(
        db.Integer, db.ForeignKey("option_groups.option_group_id"), nullable=False
    )
    name = db.Column(db.String(255), nullable=False)
    price_increment = db.Column(DECIMAL(10, 2), nullable=False)

    def to_dict(self):
        return {
            "option_id": self.option_id,
            "option_group_id": self.option_group_id,
            "name": self.name,
            "price_increment": str(self.price_increment),
        }


class Order(db.Model):
    __tablename__ = "orders"
    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    delivery_address_id = db.Column(
        db.Integer, db.ForeignKey("addresses.address_id"), nullable=False
    )
    delivery_method = db.Column(Enum("local", "inpost", "dhl"), nullable=False)
    total_price = db.Column(DECIMAL(10, 2), nullable=False)
    created_at = db.Column(
        TIMESTAMP, nullable=False, default=db.func.current_timestamp()
    )
    modified_at = db.Column(
        TIMESTAMP,
        nullable=False,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "delivery_address_id": self.delivery_address_id,
            "delivery_method": self.delivery_method,
            "total_price": str(self.total_price),
            "created_at": self.created_at,
            "modified_at": self.modified_at,
        }


class Product(db.Model):
    __tablename__ = "products"
    product_id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    base_price = db.Column(DECIMAL(10, 2), nullable=False)
    weight = db.Column(DECIMAL(10, 2), nullable=False)
    is_archived = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(
        TIMESTAMP, nullable=False, default=db.func.current_timestamp()
    )
    modified_at = db.Column(
        TIMESTAMP,
        nullable=False,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "sku": self.sku,
            "name": self.name,
            "image_url": self.image_url,
            "description": self.description,
            "base_price": str(self.base_price),
            "weight": str(self.weight),
            "is_archived": self.is_archived,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
        }


class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        TIMESTAMP, nullable=False, default=db.func.current_timestamp()
    )
    modified_at = db.Column(
        TIMESTAMP,
        nullable=False,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
        }
