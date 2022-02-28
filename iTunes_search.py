from lib2to3.pgen2.pgen import generate_grammar
import json
import requests
import webbrowser

class Media():
    def __init__(self, title="No Title", author="No Author",
            release_year='No Release Year', url='No URL', json=None):
        if json:
            try:
                self.title = json['trackName']
            except:
                try:
                    self.title = json['collectionName']
                except:
                    self.title = "N/A"
            try:
                self.url = json['trackViewUrl']
            except:
                try:
                    self.url = json['collectionViewUrl']
                except:
                    self.url = 'N/A'
            self.author = json['artistName']
            try:
                self.release_year = json['releaseDate'][:4]
            except:
                self.release_year = 'N/A'

        else:
            self.title = title
            self.author = author
            self.release_year = release_year
            self.url = url

    def info(self):
        return f"{self.title} by {self.author} ({self.release_year})"

    def length(self):
        return 0

class Song(Media):
    def __init__(self, title="No Title", author="No Author", release_year='No Release Year', 
            url='No URL', album='No Album', genre='No Genre', track_length=0, json=None):
        super().__init__(title, author, release_year, url, json)
        if json:
            self.album = json['collectionName']
            self.genre = json['primaryGenreName']
            self.track_length = json['trackTimeMillis']
        else:
            self.album = album
            self.genre = genre
            self.track_length = track_length

    def info(self):
        return f"{self.title} by {self.author} ({self.release_year}) [{self.genre}]"

    def length(self):
        return round((self.track_length/1000))

class Movie(Media):
    def __init__(self, title="No Title", author="No Author", release_year='No Release Year',
             url='No URL', rating='No Rating', movie_length=0, json=None):
        super().__init__(title, author, release_year, url, json)
        if json:
            self.rating = json['contentAdvisoryRating']
            self.movie_length = json['trackTimeMillis']
        else:
            self.rating = rating
            self.movie_length = movie_length

    def info(self):
        return f"{self.title} by {self.author} ({self.release_year}) [{self.rating}]"

    def length(self):
        return round((self.movie_length/60000))

def get_itunes(url):
    foo = {'media': []}
    results = requests.get(url).json()['results']
    for track in results:
        if 'wrapperType' in track.keys():
            if track['wrapperType'] == 'track':
                if track['kind'] == 'song':
                    if 'songs' in foo.keys():
                        foo['songs'].append(Song(json=track))
                    else:
                        foo['songs'] = [Song(json=track)]
                if track['kind'] == 'feature-movie':
                    if 'movies' in foo.keys():
                        foo['movies'].append(Movie(json=track))
                    else:
                        foo['movies'] = [Movie(json=track)]
                if track['kind'] == 'podcast':
                    foo['media'].append(Media(json=track))
        else:
            foo['media'].append(Media(json=track))
    return foo

def search_itunes(x):
    itune_url = 'https://itunes.apple.com/search?term='
    audiobook = 'media=podcast&media=musicVideo&media=audiobook&media=shortFilm&media=tvShow&media=software&media=ebook'
    song = 'entity=song'
    movie = 'entity=movie'

    term = x.replace(' ', '+')

    if x.lower().strip() == 'exit':
        print('Goodbye')
    else:
        results_list = []
        # searching songs, movies, and media
        try:
            songs = get_itunes(f'{itune_url}{term}&{song}')['songs']
        except:
            songs = []
        try:
            movies = get_itunes(f'{itune_url}{term}&{movie}')['movies']
        except:
            movies = []
        media = get_itunes(f'{itune_url}{term}&{audiobook}')['media']

        results_list.extend(songs[:20])
        results_list.extend(movies[:20])
        results_list.extend(media[:20])

        # printing results preview
        print(f'\nThe results for "{x}" are: ')
        print('\nSongs')
        if len(songs) < 1:
            print('No Song results')
        else:
            for son in songs[:20]:
                print(results_list.index(son)+1, son.info())
        print('\nMovies')
        if len(movies) < 1:
            print('No movie results')
        else:
            for mov in movies[:20]:
                print(results_list.index(mov)+1, mov.info())
        print('\nOther Media:')
        if len(media) < 1:
            print('No media results')
        else:
            for item in media[:20]:
                if item.url != 'N/A':
                    print(results_list.index(item)+1, item.info())

        # User input after preview
        y = input("\nPlease enter the number of the item you'd like to see, enter another search term, or 'Exit' to quit. ")
        term = y.replace(' ', '+')

        # if input out of results_list range, input treated as query
        if y.isnumeric():
            if int(y) <= len(results_list):
                y = int(y)
                print(f'Launching "{results_list[y-1].info()}" in browser')
                webbrowser.open(results_list[y-1].url)
                z = input('\nPlease enter a search term or enter "Exit" to quit. ')
                if z.lower().strip() == 'exit':
                    print('Goodbye')
                else:
                    term2 = z.replace(' ', '+')
                    search_itunes(term2)
            else:
                search_itunes(y)
        elif y.lower().strip() == 'exit':
            print('Goodbye')
        else:
            search_itunes(y)

def main():
    x = input('Please enter a search term or enter "Exit" to quit. ')
    search_itunes(x)


if __name__ == "__main__":
    main()
