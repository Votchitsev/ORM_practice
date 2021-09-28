import sqlalchemy as sq
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker, declarative_base, mapper, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = sq.create_engine('postgresql://votchitsev:55555@localhost:5432/music_platform_orm')
connection = engine.connect()

Session = sessionmaker(bind=engine)


class Artist(Base):
    __tablename__ = 'artist'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(40), nullable=False)


class Genre(Base):
    __tablename__ = 'genre'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(40), nullable=False)


class Album(Base):
    __tablename__ = 'album'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String, nullable=False)
    release_year = sq.Column(sq.Integer, nullable=False, )


class Track(Base):
    __tablename__ = 'track'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(40), nullable=False)
    length = sq.Column(sq.Integer, nullable=False)
    album_id = relationship('Album', backref='track', uselist=False)


class Collection(Base):
    __tablename__ = 'collection'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(40), nullable=False)
    release_year = sq.Column(sq.Integer, nullable=False)
    

if __name__ == '__main__':
    session = Session()
    Base.metadata.create_all(engine)
    session.commit()

