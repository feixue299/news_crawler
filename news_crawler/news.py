import sys, os
sys.path.append("..")
sys.path.extend([os.path.join(root, name) for root, dirs, _ in os.walk("../") for name in dirs])
from news_crawler import Base, session
from sqlalchemy import Column, String, Integer, Float, Text, DateTime

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True)
    title = Column(Text)
    content = Column(Text)
    create_date = Column(DateTime)
    source = Column(String(128))
    source_id = Column(String(128))
    category_id = Column(Integer)

    def __init__(self, title=None, content=None, create_date=None, source=None, source_id=None, category_id=None):
        self.title = title
        self.content = content
        self.create_date = create_date
        self.source = source
        self.source_id = source_id
        self.category_id = category_id


if __name__ == '__main__':
    news = News(title="title", content="content", source="source", source_id="source_id")
    session.add(news)
    session.commit()
    session.close()
