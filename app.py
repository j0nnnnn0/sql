from typing import List, Optional

from faker import Faker
from sqlalchemy import ForeignKey, String, create_engine,select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session



class Base(DeclarativeBase):
    pass

# Add a Customer with name, fullname, email_addresses, address, country_code
class Customer(Base):
    __tablename__ = "customer"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    fullname: Mapped[Optional[str]]
    email_addresses: Mapped[str]
    address: Mapped[str]
    country_code: Mapped[str] = mapped_column(String(2))
    # add a one to one relationship to credit_card
    credit_card: Mapped["CreditCard"] = relationship("CreditCard", uselist=False, back_populates="customer")
    # add a one to many relationship to order
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="customer")

    # return a string representation of the object
    def __repr__(self):
        return f"<Customer(name={self.name!r})>"

# Add a CreditCard with customer_id, number
class CreditCard(Base):
    __tablename__ = "credit_card"
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))
    number: Mapped[str] = mapped_column(String(19))
    # add a one to one relationship to customer
    customer: Mapped[Customer] = relationship("Customer", back_populates="credit_card")
    number: Mapped[str] = mapped_column(String(19))

    # return a string representation of the object
    def __repr__(self):
        return f"<CreditCard(number={self.number!r})>"

# Add a Product with name, price, description and category
class Product(Base):
    __tablename__ = "product"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float]
    description: Mapped[str]
    category: Mapped[str] = mapped_column(String(100))
    # add a one to many relationship to order
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="product")

    # return a string representation of the object
    def __repr__(self):
        return f"<Product(name={self.name!r})>"

# Add a Order with customer_id, product_id, quantity
class Order(Base):
    __tablename__ = "order"
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))
    customer : Mapped[Customer] = relationship("Customer", back_populates="orders")
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    product: Mapped[Product] = relationship("Product", back_populates="orders")
    quantity: Mapped[int]

    # return a string representation of the object
    def __repr__(self):
        return f"<Order(quantity={self.quantity!r})>"

# setup a database connection and create tables
# use SQLite with a local file for this example
from sqlalchemy import create_engine

engine = create_engine("sqlite:///database.db", echo=True)
Base.metadata.create_all(engine)

fake = Faker(["en_US", "en_GB", "en_CA", "en_AU", "de_DE", "nl_NL", "fr_FR", "es_ES", "it_IT","pt_BR", "zh_CN", "ja_JP"])

with Session(engine) as session:
    # create 10 random products
    for i in range(10):
        product = Product(
            name=f"Product {i}",
            price=9.99,
            description="This is a product",
            category="Widgets"
        )
        session.add(product)
    # create 10 customers
    for i in range(10):        
        customer = Customer(
            name=fake.name(),
            email_addresses=fake.email(),
            address=fake.address(),
            country_code=fake.country_code()
        )
       # add customer to session
        session.add(customer)
        # create a credit card for each customer
        credit_card = CreditCard(number=fake.credit_card_number(), customer=customer)
        session.add(credit_card)
       # insert random amount of orders of ramdom product IDs using their credit card 
        for i in range(fake.random_int(min=1, max=10)):
            order = Order(customer=customer, product_id=fake.random_int(min=1, max=10), 
                          quantity=fake.random_int(min=1, max=10))
        session.add(order)
    
    # commit the session to the database
    session.commit()


# Query the database
# get all customers
# import select
from sqlalchemy import select

query = select(Customer)
results = session.execute(query).scalars().all()
print(results)

# get all customers from the US
query = select(Customer).where(Customer.country_code == "BR")
results = session.execute(query).scalars().all()
print(results)