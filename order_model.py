from sqlalchemy import Column, Integer, String, Date
import datetime as dt
from sqlalchemy.orm import declarative_base

Base_order = declarative_base()


class Order(Base_order):
    __tablename__ = "Orders"

    id = Column("id", Integer, primary_key=True, autoincrement=True) 
    customer_name = Column("customer_name", String, nullable=False)
    orders = Column("orders", String, nullable=False)
    date_created = Column("date_created", Date, nullable=False, default=dt.datetime.utcnow)

    def toJSON(self):
        return {
            "id":self.id,
            "customer_name": self.customer_name,
            "orders" : self.orders,
            "date_created" : self.date_created
        }