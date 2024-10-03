from sqlalchemy import Column, Integer, String, Date
import datetime as dt
from sqlalchemy.orm import declarative_base

Base_main_plate = declarative_base()


class Plate(Base_main_plate):
    __tablename__ = "Plates"

    id = Column("id", Integer, primary_key=True, autoincrement=True) 
    type = Column("type", String, nullable=False)
    image = Column("image", String, nullable=False)
    url = Column("url", String, nullable=False)

    def toJSON(self):
        return {
            "id":self.id,
            "type":self.type,
            "image":self.image,
            "url":self.url
        }