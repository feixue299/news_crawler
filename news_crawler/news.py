# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Float, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import base
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://root:w1234@81.68.242.216/common_server')
Base = declarative_base()

DBSession = sessionmaker(bind=engine)
session = DBSession()

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True)
    title = Column(Text)
    content = Column(Text)
    create_date = Column(DateTime)
    source = Column(String(20))
    source_id = Column(String(128))

    def __init__(self, title=None, content=None, create_date=None, source=None, source_id=None):
        self.title = title
        self.content = content
        self.create_date = create_date
        self.source = source
        self.source_id = source_id


if __name__ == '__main__':
    news = News(title="title", content="content", source="source", source_id="source_id")
    session.add(news)
    session.commit()
    session.close()
