import os
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
from .paths import BASE_DIR

Base = declarative_base()
engine = create_engine("sqlite:///" + os.path.join(BASE_DIR, "utils", "posts.db"), echo=False)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


class Post(Base):
    """
    DB table to store Craigslist Housing information fitting to criteria
    """

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, unique=True)
    title = Column(String)
    url = Column(String, unique=True)
    date = Column(DateTime)
    price = Column(Float)
    location = Column(String)
    has_image = Column(String)
    bedrooms = Column(String)
    area = Column(String)


def get_new_posts(filtered_posts):   
    new_posts = pd.DataFrame(columns=list(filtered_posts))
    for _, post in filtered_posts.iterrows():
        post_session = session.query(Post).filter_by(post_id=post.get("post_id")).first()
        # Don't add posting to db if it already exists
        if post_session:
            continue
        write_to_db(post)
        # add new posts to pandas dataframe
        new_posts = new_posts.append(post)
    
    return new_posts


def write_to_db(post):
    post = Post(
        post_id=post.get("post_id"),
        title=post.get("title"),
        url=post.get("url"),
        date=post.get("date_posted"),
        price="%.0f" % post.get("price"),
        location=post.get("location"),
        has_image=post.get("post_has_image"),
        bedrooms=post.get("bedrooms"),
        area=post.get("area"),
    )
    session.add(post)
    session.commit()


# if __name__ == "__main__":
#     engine = create_engine("sqlite:///posts.db", echo=False)
#     Base.metadata.create_all(engine)

#     Session = sessionmaker(bind=engine)
#     session = Session()
#     df = pd.read_csv("test.csv")
#     get_new_posts(df)
