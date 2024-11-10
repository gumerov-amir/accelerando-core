import json

from accelerando_core.errors import NotFoundError
from accelerando_core.models import Article, DB, Genre, Links, Person, Track


class AccelerandoCore:
    """Accelerando core"""

    def __init__(self, file_name: str):
        self.file_name = file_name
        self._load_db()

    def _load_db(self) -> None:
        with open(self.file_name, "r", encoding="utf-8") as f:
            self.db = DB(**(json.load(f)))

    def _save_db(self) -> None:
        with open(self.file_name, "w", encoding="utf-8") as f:
            f.write(self.db.model_dump_json(indent=4))

    def add_article(
        self,
        name: str,
        text: str = "",
        url: str = "",
    ) -> tuple[int, Article]:
        """adds new article to database"""
        article_id = len(self.db.articles) + 1
        article = Article(
            id=article_id,
            name=name,
            text=text,
            url=url,
        )
        self.db.articles.append(article)
        return article_id, article

    def add_artist(
        self,
        name: str,
        birth_date: str = "",
        country: str = "",
        articles: list[int] = [],
    ) -> tuple[int, Person]:
        """adds new artist to database"""
        artist_id = len(self.db.composers) + 1
        artist = Person(
            id=artist_id,
            name=name,
            birthdate=birth_date,
            country=country,
            articles=articles.copy(),
        )
        self.db.artists.append(artist)
        return artist_id, artist

    def add_composer(
        self,
        name: str,
        birth_date: str = "",
        country: str = "",
        articles: list[int] = [],
    ) -> tuple[int, Person]:
        composer_id = len(self.db.composers) + 1
        composer = Person(
            id=composer_id,
            name=name,
            birthdate=birth_date,
            country=country,
            articles=articles.copy(),
        )
        self.db.composers.append(composer)
        return composer_id, composer

    def add_genre(
        self,
        name: str,
        parent_genre: int = 0,
        articles: list[int] = [],
    ) -> tuple[int, Genre]:
        genre_id = len(self.db.genres) + 1
        genre = Genre(
            id=genre_id,
            name=name,
            parent_genre=parent_genre,
            articles=articles.copy(),
        )
        self.db.genres.append(genre)
        return genre_id, genre

    def add_track(
        self,
        name: str,
        composers: list[int] = [],
        artists: list[int] = [],
        genres: list[int] = [],
        creation_date: str = "",
        links: Links = Links(),
        articles: list[int] = [],
    ) -> tuple[int, Track]:
        track_id = len(self.db.tracks) + 1
        track = Track(
            id=track_id,
            name=name,
            composers=composers.copy(),
            artists=artists.copy(),
            genres=genres.copy(),
            creation_date=creation_date,
            links=links.model_copy(),
            articles=articles.copy(),
        )
        self.db.tracks.append(track)
        return track_id, track

    def get_article_by_id(self, article_id: int) -> Article:
        for article in self.db.articles:
            if article.id == article_id:
                return article
        raise NotFoundError

    def get_artist_by_id(self, artist_id: int) -> Person:
        for artist in self.db.artists:
            if artist.id == artist_id:
                return artist
        raise NotFoundError

    def get_composer_by_id(self, composer_id: int) -> Person:
        for composer in self.db.composers:
            if composer.id == composer_id:
                return composer
        raise NotFoundError

    def get_genre_by_id(self, genre_id: int) -> Genre:
        for genre in self.db.genres:
            if genre.id == genre_id:
                return genre
        raise NotFoundError

    def get_track_by_id(self, track_id: int) -> Track:
        for track in self.db.tracks:
            if track.id == track_id:
                return track
        raise NotFoundError

    def get_parent_genres(self, genre_id: int) -> list[int]:
        result: list[int] = []
        genre = self.get_genre_by_id(genre_id)
        while genre.parent_genre > 0:
            genre = self.get_genre_by_id(genre.parent_genre)
            result.append(genre.id)
        return result

    def get_tracks(
        self,
        composers: list[int] = [],
        artists: list[int] = [],
        genres: list[int] = [],
    ) -> list[Track]:
        result: list[Track] = []
        for track in self.db.tracks:
            track_genres = track.genres.copy()
            for track_genre in track_genres:
                track_genres.extend(self.get_parent_genres(track_genre))
            if (
                any(composer in composers for composer in track.composers)
                or any(artist in artists for artist in track.artists)
                or any(genre in genres for genre in track_genres)
            ):
                result.append(track)
        return result

    def save(self) -> None:
        self._save_db()
