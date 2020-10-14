import sys, os
sys.path.append("..")
sys.path.extend([os.path.join(root, name) for root, dirs, _ in os.walk("../") for name in dirs])
from news_crawler import Base, session
from sqlalchemy import Column, String, Integer, Float, Text, DateTime

class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    category = Column(String(128))

    def __init__(self, category=None):
        self.category = category

if __name__ == "__main__":
    category = Category(category="test")
    session.add(category)
    session.commit()
    session.close()