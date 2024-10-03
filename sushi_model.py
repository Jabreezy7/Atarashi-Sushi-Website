from sqlalchemy import Column, Integer, String, Date
import datetime as dt
from sqlalchemy.orm import declarative_base

Base_sushi = declarative_base()


class Sushi(Base_sushi):
    __tablename__ = "Sushis"

    id = Column("id", Integer, primary_key=True, autoincrement=True) 
    type = Column("type", String, nullable=False)
    image = Column("image", String, nullable=False)
    price = Column("price", Integer, nullable=False)

    def toJSON(self):
        return {
            "id":self.id,
            "type":self.type,
            "image":self.image,
            "price":self.price
        }