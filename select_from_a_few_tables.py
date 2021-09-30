from sqlalchemy import text
from main import Session, Artist, Genre, artist_to_genre, Album, Track, artist_to_album, Collection, track_to_collection

session = Session()


# Запрос № 1  "Количество исполнителей в каждом жанре"

print('\nЗапрос № 1: ')
for genre in session.query(Genre):
    print(genre.name, len(genre.artist))


# Запрос № 2 "Количество треков, вошедших в альбомы 2019-2020 годов"

print('\nЗапрос № 2:')
print(session.query(Track).join(Album).filter(text("Album.release_year = 2019 or Album.release_year = 2020")).count())


# Запрос № 3 "Средняя продолжительность треков по каждому альбому"

print('\nЗапрос № 3:')
for album in session.query(Album).join(Track):
    len_count = 0
    count = 0
    for track in album.track:
        len_count += track.length
        count += 1
    avg_len = len_count/count
    print(album.name, round(avg_len, 0))


# Запрос № 4 "Все исполнители, которые не выпустили альбомы в 2021 году"

print('\nЗапрос № 4:')

for album in session.query(Album).join(artist_to_album).join(Artist).filter(Album.release_year != 2021):
    for artist in album.artist:
        print(artist.name)


# Запрос № 5 "Названия сборников, в которых присутствует конкретный исполнитель (выберите сами)"

print('\nЗапрос № 5:')

for collection in session.query(Collection).join(track_to_collection).join(Track).join(Album).join(artist_to_album).\
        join(Artist).filter(Artist.name == 'FKJ'):
    print(collection.name)


# Запрос № 6 "Название альбомов, в которых присутствуют исполнители более 1 жанра"

print('\nЗапрос № 6')

for album in session.query(Album).join(artist_to_album).join(Artist).join(artist_to_genre).join(Genre):
    for artist in album.artist:
        if len(artist.genre) > 1:
            print(album.name)
        else:
            pass

# Запрос № 7 "Наименование треков, которые не входят в сборники"

print('\nЗапрос № 7:')

for track in session.query(Track).join(track_to_collection).join(Collection):
    if len(track.collection) == 0:
        print(track.name)
    else:
        pass


# Запрос № 8 "исполнителя(-ей), написавшего самый короткий по продолжительности трек
#             (теоретически таких треков может быть несколько)"

print('\nЗапрос №8')

for track in session.query(Track).join(Album).join(artist_to_album).join(Artist).order_by(Track.length)[0:1]:
    for artist in track.album.artist:
        print(artist.name)

# Запрос № 9 "Название альбомов, содержащих наименьшее количество треков."

print('\nЗапрос №9')
number_of_tracks_list = {}
for album in session.query(Album).join(Track):
    number_of_tracks_list[album.name] = len(album.track)

min_count_of_tracks = min(number_of_tracks_list.values())

for album in number_of_tracks_list.items():
    if album[1] == min_count_of_tracks:
        print(album[0])
