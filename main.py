import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker, relationship, mapper
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
    track = relationship('Track', back_populates='album')


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
    sq.Column('artist_id', sq.ForeignKey(Artist.id)),
    sq.Column('genre_id', sq.ForeignKey(Genre.id))
)

track_to_collection = sq.Table(
    'track_to_collection', Base.metadata,
    sq.Column('track_id', sq.Integer, sq.ForeignKey(Track.id)),
    sq.Column('collection_id', sq.Integer, sq.ForeignKey(Collection.id))
)

if __name__ == '__main__':
    session = Session()
    Base.metadata.create_all(engine)

    session.commit()
    connection.execute("""
    # DROP TABLE track_to_collection;""")

#    ==================================================INSERT==========================================================

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
    for i in artist:
        artist = Artist(name=i)
        session.add(artist)

    for i in genre:
        genre_obj = Genre(name=i)
        session.add(genre_obj)

    for i in album.items():
        album_obj = Album(name=i[0], release_year=i[1])
        session.add(album_obj)

    artist_genre = {
        'Kaiser_Chiefs': 'Indie', 'Franz_Ferdinand': 'Indie', 'Led_Zeppelin': 'Hard_Rock', 'Nirvana': 'Grunge',
        'FKJ': 'Electronics', 'Jose_James': 'Jazz', 'Blink-182': 'Punk-rock', 'Massive_Attack': 'Trip-Hop'
    }

    for i in artist_genre.items():
        a = session.query(Artist).filter(Artist.name == i[0]).first()
        g = session.query(Genre).filter(Genre.name == i[1]).first()
        a.genre.append(g)
        session.add(a)
    artist_album = {
        'Kaiser_Chiefs': ['Duck'], 'Franz_Ferdinand': ['Always_Acsending'], 'Led_Zeppelin': ['Led_Zeppelin_IV'],
        'Nirvana': ['Nevermind'], 'FKJ': ['Just_Piano'], 'Jose_James': ['Lean_On_Me'], 'Blink-182': ['California'],
        'Massive_Attack': ['Helogoland']
    }

    for i in artist_album.items():
        artist = session.query(Artist).filter(Artist.name == i[0]).first()
        for j in i[1]:
            album = session.query(Album).filter(Album.name == j).first()
            album.artist.append(artist)
            session.add(album)

    track = [
        {'track_name': 'People_Know_How_To_Love_One_Another',
         'album': 'Duck',
         'len': 216},
        {'track_name': 'Golden_Oldies',
         'album': 'Duck',
         'len': 244},
        {'track_name': 'Wait',
         'album': 'Duck',
         'len': 230},
        {'track_name': 'Always_Acsending',
         'album': 'Always_Acsending',
         'len': 321},
        {'track_name': 'Lazy_Boy',
         'album': 'Always_Acsending',
         'len': 179},
        {'track_name': 'Paper_Cages',
         'album': 'Always_Acsending',
         'len': 220},
        {'track_name': 'Black_Dog',
         'album': 'Led_Zeppelin_IV',
         'len': 296},
        {'track_name': 'Rock_And_Roll',
         'album': 'Led_Zeppelin_IV',
         'len': 221},
        {'track_name': 'The_Battle_of_Evermore',
         'album': 'Led_Zeppelin_IV',
         'len': 352},
        {'track_name': 'Smells_Like_Teen_Spirit',
         'album': 'Nevermind',
         'len': 301},
        {'track_name': 'In_Bloom',
         'album': 'Nevermind',
         'len': 255},
        {'track_name': 'Come_As_You_Are',
         'album': 'Nevermind',
         'len': 219},
        {'track_name': 'Sundays',
         'album': 'Just_Piano',
         'len': 213},
        {'track_name': 'Anthem',
         'album': 'Just_Piano',
         'len': 157},
        {'track_name': 'Last_Hour',
         'album': 'Just_Piano',
         'len': 163},
        {'track_name': 'Lean_On_Me',
         'album': 'Lean_On_Me',
         'len': 297},
        {'track_name': 'Cynical',
         'album': 'California',
         'len': 116},
        {'track_name': "She_is_out_Of_Her_Mind",
         'album': 'California',
         'len': 163},
        {'track_name': 'Bored_to_Death',
         'album': 'California',
         'len': 236},
        {'track_name': 'Prey_For_Rain',
         'album': 'Helogoland',
         'len': 404},
        {'track_name': 'Babel',
         'album': 'Helogoland',
         'len': 320},
        {'track_name': 'Splitting_The_Atom',
         'album': 'Helogoland',
         'len': 317}
    ]

    for i in track:
        track_name = i['track_name']
        album_name = i['album']
        track_len = i['len']
        album_id = session.query(Album).filter(Album.name == album_name).first()
        track_for_add = Track(name=track_name, album_id=album_id.id, length=track_len)
        session.add(track_for_add)

    collection = [
        {'name': 'Chill',
         'year': 2019,
         'tracks': ['Sundays', 'Prey_For_Rain']},
        {'name': 'Rock',
         'year': 2020,
         'tracks': ['Bored_to_Death', 'Smells_Like_Teen_Spirit']},
        {'name': 'Electro',
         'year': 2019,
         'tracks': ['Babel', 'Anthem']},
        {'name': 'Indie',
         'year': 2018,
         'tracks': ['Golden_Oldies', 'Lazy_Boy']},
        {'name': 'Just_Hard',
         'year': 2017,
         'tracks': ['In_Bloom', 'Black_Dog', 'She_is_out_Of_Her_Mind']},
        {'name': 'New',
         'year': 2020,
         'tracks': ['Lean_On_Me', 'Sundays']},
        {'name': 'Under_Stars',
         'year': 2021,
         'tracks': ['Always_Acsending', 'Wait']},
        {'name': 'Ctrl_Alt',
         'year': 2021,
         'tracks': ['Splitting_The_Atom', 'Anthem']}
    ]

    for collect in collection:
        collection_name = collect['name']
        collection_year = collect['year']
        collection_tracks = collect['tracks']
        collection = Collection(name=collection_name, release_year=collection_year)
        session.add(collection)

    for collect in collection:
        changed_collect = session.query(Collection).filter(Collection.name == collect['name']).first()
        for track in collect['tracks']:
            track_for_add = session.query(Track).filter(Track.name == track).first()
            changed_collect.track.append(track_for_add)
        session.add(changed_collect)

    session.commit()

