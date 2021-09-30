from sqlalchemy import text
from main import Session, Album, Track, Collection, Artist

session = Session()


# Запрос № 1: название и год выхода альбомов, вышедших в 2018 году

albums_from_2018 = session.query(Album).filter(Album.release_year == 2018).all()
print('Запрос № 1:')
for album in albums_from_2018:
    print(album.name, album.release_year)


# Запрос № 2: название и продолжительность самого длительного трека

print('\nЗапрос № 2:')
for track in session.query(Track).order_by(Track.length)[-1:]:
    print(track.length, track.name)


# Запрос № 3: название треков, продолжительность которых не менее 3,5 минуты

print('\nЗапрос № 3:')
for track in session.query(Track).filter(Track.length >= 210):
    print(track.name, track.length)


# Запрос № 4: названия сборников, вышедших в период с 2018 по 2020 год включительно

print('\nЗапрос № 4:')
for collection in session.query(Collection).filter(text('Collection.release_year >= 2018 and '
                                                        'Collection.release_year <= 2020')).\
        order_by(Collection.release_year):
    print(collection.name, collection.release_year)


# Запрос № 5: исполнители, чье имя состоит из 1 слова

print('\nЗапрос № 5:')
for artist in session.query(Artist).filter(text("((length(Artist.name) - length(replace(Artist.name,'_', '')))) = 0")):
    print(artist.name)


# Запрос № 6: название треков, которые содержат слово "мой"/"my"

print('\nЗапрос № 6:')
for track in session.query(Track).filter(text("Track.name like '%%Love%%'")):
    print(track.name)

