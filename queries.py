from app import engine, Base, session, Customer, CreditCard, Product, Order ,select,func

# Query the database
# get all customers

query = select(Customer)
results = session.execute(query).scalars().all()
print(results)

# get all customers from the US
query = select(Customer).where(Customer.country_code == "BR")
results = session.execute(query).scalars().all()
print(results)

# select a list of countries grouped by country code
query = select(Customer.country_code, func.count(Customer.country_code)).group_by(Customer.country_code)
results = session.execute(query).all()
print(results)

# select customer name and credit card number
query = select(Customer.name, CreditCard.number).join(CreditCard)
results = session.execute(query).all()
print(results)

# select customer name with their number of orders
query = select(Customer.name, func.count(Order.id)).join(Order).group_by(Customer.name)
results = session.execute(query).all()
print(results)