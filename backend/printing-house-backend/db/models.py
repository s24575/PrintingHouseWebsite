import enum

from sqlalchemy import (
    Enum,
    DECIMAL,
    Date,
    TIMESTAMP,
    Table,
    String,
    Integer,
    Boolean,
    Text,
    ForeignKey,
    func,
    Column,
    LargeBinary,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}  # noqa


class Address(Base):
    __tablename__ = "addresses"
    address_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    country: Mapped[str] = mapped_column(String(255))
    voivodeship: Mapped[str] = mapped_column(String(255))
    powiat: Mapped[str] = mapped_column(String(255))
    gmina: Mapped[str] = mapped_column(String(255))
    city: Mapped[str] = mapped_column(String(255))
    postal_code: Mapped[str] = mapped_column(String(20))
    street: Mapped[str] = mapped_column(String(255))
    house_number: Mapped[str] = mapped_column(String(255))
    apartment_number: Mapped[str | None] = mapped_column(String(255))


class CompanyDetail(Base):
    __tablename__ = "company_details"
    company_details_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.address_id"))
    name: Mapped[str] = mapped_column(String(255))
    acronym: Mapped[str] = mapped_column(String(255))
    bank_name: Mapped[str] = mapped_column(String(255))
    bank_account_number: Mapped[str] = mapped_column(String(255))
    nip: Mapped[str] = mapped_column(String(255))
    regon: Mapped[str] = mapped_column(String(255))
    phone_number: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(255))
    discount_percentage: Mapped[float] = mapped_column(DECIMAL(5, 2))
    is_archived: Mapped[bool] = mapped_column(Boolean)
    created_at: Mapped[str] = mapped_column(TIMESTAMP, default=func.current_timestamp())
    modified_at: Mapped[str] = mapped_column(
        TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp()
    )


class UserRole(enum.Enum):
    user = "user"
    worker = "worker"
    admin = "admin"


class User(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.address_id"))
    email: Mapped[str] = mapped_column(String(255))
    password_hash: Mapped[str] = mapped_column(String(255))
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    phone_number: Mapped[str] = mapped_column(String(20))
    role: Mapped[Enum] = mapped_column(Enum(UserRole), default=UserRole.user)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=func.current_timestamp())
    modified_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp()
    )


class Dictionary(Base):
    __tablename__ = "dictionary"
    dictionary_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    key: Mapped[str] = mapped_column(String(255))
    value: Mapped[str] = mapped_column(String(255))


class InvoiceItem(Base):
    __tablename__ = "invoice_items"
    invoice_item_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    invoice_id: Mapped[int] = mapped_column(ForeignKey("invoices.invoice_id"))
    item_description: Mapped[str] = mapped_column(String(255))
    quantity: Mapped[int] = mapped_column(Integer)
    unit_price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    total_price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    vat_rate: Mapped[float] = mapped_column(DECIMAL(5, 2))
    item_item_id: Mapped[int] = mapped_column(ForeignKey("items.item_id"))


class Invoice(Base):
    __tablename__ = "invoices"
    invoice_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_order_id: Mapped[int] = mapped_column(ForeignKey("orders.order_id"))
    company_details_id: Mapped[int] = mapped_column(ForeignKey("company_details.company_details_id"))
    billing_address_id: Mapped[int] = mapped_column(ForeignKey("addresses.address_id"))
    invoice_number: Mapped[str] = mapped_column(String(50))
    issue_date: Mapped[str] = mapped_column(Date)
    due_date: Mapped[str] = mapped_column(Date)
    total_amount: Mapped[float] = mapped_column(DECIMAL(10, 2))
    vat_rate: Mapped[float] = mapped_column(DECIMAL(5, 2))
    is_archived: Mapped[bool] = mapped_column(Boolean)
    created_at: Mapped[str] = mapped_column(TIMESTAMP, default=func.current_timestamp())
    modified_at: Mapped[str] = mapped_column(
        TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp()
    )


class File(Base):
    __tablename__ = "files"
    file_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cart_item_id: Mapped[int] = mapped_column(ForeignKey("cart_items.cart_item_id"))
    item_id: Mapped[int] = mapped_column(ForeignKey("items.item_id"))
    filename: Mapped[str] = mapped_column(String(255))
    file_data: Mapped[str] = mapped_column(LargeBinary(length=(2**32) - 1))


class ItemOption(Base):
    __tablename__ = "item_options"
    item_option_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.item_id"))
    option_id: Mapped[int] = mapped_column(ForeignKey("options.option_id"))
    name: Mapped[str] = mapped_column(String(255))
    value: Mapped[str] = mapped_column(String(255))


class Item(Base):
    __tablename__ = "items"
    item_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.product_id"))
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.order_id"))
    name: Mapped[str] = mapped_column(String(255))
    quantity: Mapped[int] = mapped_column(Integer)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))

    item_options: Mapped[list["ItemOption"]] = relationship("ItemOption", backref="Item", cascade="all, delete-orphan")


cart_item_options = Table(
    "cart_item_options",
    Base.metadata,
    Column("cart_item_id", ForeignKey("cart_items.cart_item_id"), primary_key=True),
    Column("option_id", ForeignKey("options.option_id"), primary_key=True),
)


class CartItem(Base):
    __tablename__ = "cart_items"
    cart_item_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.product_id"))
    quantity: Mapped[int] = mapped_column(Integer)

    product: Mapped["Product"] = relationship("Product")
    options: Mapped[list["Option"]] = relationship("Option", secondary="cart_item_options")


class OptionGroup(Base):
    __tablename__ = "option_groups"
    option_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.product_id"))
    name: Mapped[str] = mapped_column(String(255))
    type: Mapped[Enum] = mapped_column(Enum("select", "number"))
    title: Mapped[str] = mapped_column(String(255))
    is_mandatory: Mapped[bool] = mapped_column(Boolean)

    options: Mapped[list["Option"]] = relationship(back_populates="option_group")


class Option(Base):
    __tablename__ = "options"
    option_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    option_group_id: Mapped[int] = mapped_column(ForeignKey("option_groups.option_group_id"))
    name: Mapped[str] = mapped_column(String(255))
    price_increment: Mapped[float] = mapped_column(DECIMAL(10, 2))

    option_group: Mapped["OptionGroup"] = relationship(back_populates="options")


class OrderStatus(enum.Enum):
    created = "created"
    in_progress = "in_progress"
    completed = "completed"
    canceled = "canceled"


class ShippingMethod(enum.Enum):
    self_pickup = "self_pickup"
    inpost = "inpost"
    dhl = "dhl"


class Order(Base):
    __tablename__ = "orders"
    order_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    delivery_address_id: Mapped[int | None] = mapped_column(ForeignKey("addresses.address_id"))
    total_price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    status: Mapped[Enum] = mapped_column(Enum(OrderStatus), default=OrderStatus.created)
    shipping_method: Mapped[Enum] = mapped_column(Enum(ShippingMethod))
    shipping_date: Mapped[str] = mapped_column(Date)
    created_at: Mapped[str] = mapped_column(TIMESTAMP, default=func.current_timestamp())
    modified_at: Mapped[str] = mapped_column(
        TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp()
    )

    items: Mapped[list["Item"]] = relationship()


class Product(Base):
    __tablename__ = "products"
    product_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sku: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    image_url: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    base_price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    weight: Mapped[float] = mapped_column(DECIMAL(10, 2))
    is_archived: Mapped[bool] = mapped_column(Boolean)
    created_at: Mapped[str] = mapped_column(TIMESTAMP, default=func.current_timestamp())
    modified_at: Mapped[str] = mapped_column(
        TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp()
    )
