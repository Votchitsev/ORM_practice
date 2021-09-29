import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
engine = sq.create_engine('postgresql://votchitsev:55555@localhost:5432/music_platform_orm')
connection = engine.connect()

Session = sessionmaker(bind=engine)


class Artist(Base):
    __tablename__ = 'artist'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(40), nullable=False)
    genre = relationship('Genre', secondary='artist_to_genre', back_populates='artist')
    album = relationship('Album', secondary='artist_to_album', back_populates='artist')

    def __repr__(self):
        return self.id


class Genre(Base):
    __tablename__ = 'genre'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(40), nullable=False)
    artist = relationship(Artist, secondary='artist_to_genre', back_populates='genre')


class Album(Base):
    __tablename__ = 'album'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String, nullable=False)
    release_year = sq.Column(sq.Integer, nullable=False)
    artist = relationship(Artist, secondary='artist_to_album', back_populates='album')


class Track(Base):
    __tablename__ = 'track'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(40), nullable=False)
    length = sq.Column(sq.Integer, nullable=False)
    album = relationship(Album, uselist=False)
    album_id = sq.Column(sq.Integer, sq.ForeignKey(Album.id))
    collection = relationship('Collection', secondary='track_to_collection', back_populates='track')


class Collection(Base):
    __tablename__ = 'collection'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(40), nullable=False)
    release_year = sq.Column(sq.Integer, nullable=False)
    track = relationship(Track, secondary='track_to_collection', back_populates='collection')


artist_to_album = sq.Table(
    'artist_to_album', Base.metadata,
    sq.Column('artist_id', sq.Integer, sq.ForeignKey(Artist.id)),
    sq.Column('album_id', sq.Integer, sq.ForeignKey(Album.id))
)

artist_to_genre = sq.Table(
    'artist_to_genre', Base.metadata,
    sq.Column('artist_id', sq.Integer, sq.ForeignKey(Artist.id)),
    sq.Column('genre_id', sq.Integer, sq.ForeignKey(Genre.id))
)

track_to_collection = sq.Table(
    'track_to_collection', Base.metadata,
    sq.Column('track_id', sq.Integer, sq.ForeignKey(Track.id)),
    sq.Column('collection_id', sq.Integer, sq.ForeignKey(Collection.id))
)

if __name__ == '__main__':
    # session = Session()
    # Base.metadata.create_all(engine)

    # session.commit()
    # connection.execute("""
    # # DROP TABLE track_to_collection;""")

    # INSERT==========================================================

    artist = [
        'Kaiser_Chiefs', 'Franz_Ferdinand', 'Led_Zeppelin', 'Nirvana',
        'FKJ', 'Jose_James', 'Blink-182', 'Massive_Attack'
    ]

    genre = [
        'Indie', 'Hard_Rock', 'Grunge', 'Electronics',
        'Punk-rock', 'Jazz', 'Trip-Hop'
    ]

    album = {
        'Duck': 2019,
        'Always_Acsending': 2018,
        'Led_Zeppelin_IV': 1971,
        'Nevermind': 1991,
        'Just_Piano': 2021,
        'Lean_On_Me': 2018,
        'California': 2016,
        'Helogoland': 2010,
    }
    session = Session()
    # for i in artist:
    #     artist = Artist(name=i)
    #     session.add(artist)
    #
    # for i in genre:
    #     genre_obj = Genre(name=i)
    #     session.add(genre_obj)
    artist_genre = {
        'Kaiser_Chiefs': 'Indie', 'Franz_Ferdinand': 'Indie', 'Led_Zeppelin': 'Hard_Rock', 'Nirvana': 'Grunge',
        'FKJ': 'Electronics', 'Jose_James': 'Jazz', 'Blink-182': 'Punk-rock', 'Massive_Attack': 'Trip-Hop'
    }

    for i in artist_genre.items():
        a = session.query(Artist).filter(Artist.name == i[0]).first()
        g = session.query(Genre).filter(Genre.name == i[1]).first()
        print(a.name)


