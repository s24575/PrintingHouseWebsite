from typing import List
from sqlalchemy import Enum, DECIMAL, Date, TIMESTAMP, Table, String, Integer, Boolean, Text, ForeignKey, func, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}  # noqa


class Address(Base):
    __tablename__ = "addresses"
    address_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    country: Mapped[str] = mapped_column(String(255), nullable=False)
    voivodeship: Mapped[str] = mapped_column(String(255), nullable=False)
    powiat: Mapped[str] = mapped_column(String(255), nullable=False)
    gmina: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[str] = mapped_column(String(255), nullable=False)
    postal_code: Mapped[str] = mapped_column(String(20), nullable=False)
    street: Mapped[str] = mapped_column(String(255), nullable=False)
    house_number: Mapped[str] = mapped_column(String(255), nullable=False)
    apartment_number: Mapped[str | None] = mapped_column(String(255), nullable=True)


class CompanyDetail(Base):
    __tablename__ = "company_details"
    company_details_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.address_id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    acronym: Mapped[str] = mapped_column(String(255), nullable=False)
    bank_name: Mapped[str] = mapped_column(String(255), nullable=False)
    bank_account_number: Mapped[str] = mapped_column(String(255), nullable=False)
    nip: Mapped[str] = mapped_column(String(255), nullable=False)
    regon: Mapped[str] = mapped_column(String(255), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    discount_percentage: Mapped[float] = mapped_column(DECIMAL(5, 2), nullable=False)
    is_archived: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[str] = mapped_column(TIMESTAMP, nullable=False, default=func.current_timestamp())
    modified_at: Mapped[str] = mapped_column(
        TIMESTAMP, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp()
    )


class User(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, nullable=False, default=func.current_timestamp())
    modified_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP,
        nullable=False,
        default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )


class Dictionary(Base):
    __tablename__ = "dictionary"
    dictionary_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    key: Mapped[str] = mapped_column(String(255), nullable=False)
    value: Mapped[str] = mapped_column(String(255), nullable=False)


class InvoiceItem(Base):
    __tablename__ = "invoice_items"
    invoice_item_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    invoice_id: Mapped[int] = mapped_column(ForeignKey("invoices.invoice_id"), nullable=False)
    item_description: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    total_price: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    vat_rate: Mapped[float] = mapped_column(DECIMAL(5, 2), nullable=False)
    item_item_id: Mapped[int] = mapped_column(ForeignKey("items.item_id"), nullable=False)


class Invoice(Base):
    __tablename__ = "invoices"
    invoice_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_order_id: Mapped[int] = mapped_column(ForeignKey("orders.order_id"), nullable=False)
    company_details_id: Mapped[int] = mapped_column(ForeignKey("company_details.company_details_id"), nullable=False)
    billing_address_id: Mapped[int] = mapped_column(ForeignKey("addresses.address_id"), nullable=False)
    invoice_number: Mapped[str] = mapped_column(String(50), nullable=False)
    issue_date: Mapped[str] = mapped_column(Date, nullable=False)
    due_date: Mapped[str] = mapped_column(Date, nullable=False)
    total_amount: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    vat_rate: Mapped[float] = mapped_column(DECIMAL(5, 2), nullable=False)
    is_archived: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[str] = mapped_column(TIMESTAMP, nullable=False, default=func.current_timestamp())
    modified_at: Mapped[str] = mapped_column(
        TIMESTAMP, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp()
    )


# class ItemOption(Base):
#     __tablename__ = "item_options"
#     item_option_id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     item_id: Mapped[int] = mapped_column(ForeignKey("items.item_id"), nullable=False)
#     option_id: Mapped[int] = mapped_column(ForeignKey("options.option_id"), nullable=False)
#
#
# class Item(Base):
#     __tablename__ = "items"
#     item_id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     product_id: Mapped[int] = mapped_column(ForeignKey("products.product_id"), nullable=False)
#     order_id: Mapped[int | None] = mapped_column(ForeignKey("orders.order_id"), nullable=True)
#     cart_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.user_id"), nullable=True)
#     name: Mapped[str] = mapped_column(String(255), nullable=False)
#     quantity: Mapped[int] = mapped_column(Integer, nullable=False)
#     price: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
#     user_comment: Mapped[str] = mapped_column(Text, nullable=False)
#
#     options: Mapped[List["ItemOption"]] = relationship("ItemOption", backref="item", cascade="all, delete-orphan")


cart_item_options = Table(
    "cart_item_options",
    Base.metadata,
    Column("cart_item_id", ForeignKey("cart_items.cart_item_id"), primary_key=True),
    Column("option_id", ForeignKey("options.option_id"), primary_key=True),
)


class CartItem(Base):
    __tablename__ = "cart_items"
    cart_item_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.product_id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    product: Mapped["Product"] = relationship("Product")
    options: Mapped[List["Option"]] = relationship("Option", secondary="cart_item_options")


class OptionGroup(Base):
    __tablename__ = "option_groups"
    option_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.product_id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[Enum] = mapped_column(Enum("select", "number"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    is_mandatory: Mapped[bool] = mapped_column(Boolean, nullable=False)

    options: Mapped[List["Option"]] = relationship()


class Option(Base):
    __tablename__ = "options"
    option_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    option_group_id: Mapped[int] = mapped_column(ForeignKey("option_groups.option_group_id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    price_increment: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)


class Order(Base):
    __tablename__ = "orders"
    order_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    delivery_address_id: Mapped[int] = mapped_column(ForeignKey("addresses.address_id"), nullable=False)
    delivery_method: Mapped[Enum] = mapped_column(Enum("local", "inpost", "dhl"), nullable=False)
    total_price: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    created_at: Mapped[str] = mapped_column(TIMESTAMP, nullable=False, default=func.current_timestamp())
    modified_at: Mapped[str] = mapped_column(
        TIMESTAMP, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp()
    )


class Product(Base):
    __tablename__ = "products"
    product_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sku: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    image_url: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    base_price: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    weight: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    is_archived: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[str] = mapped_column(TIMESTAMP, nullable=False, default=func.current_timestamp())
    modified_at: Mapped[str] = mapped_column(
        TIMESTAMP, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp()
    )

    cart_items: Mapped[List["CartItem"]] = relationship()
