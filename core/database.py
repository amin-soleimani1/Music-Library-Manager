import sqlite3
from pathlib import Path

from core.track import Track
from core.playlist import PlayLists


class MusicDatabase:

    # ==» Tables «==-----------------------------
    CREATED_TRACKS_TABLE = """
        CREATE TABLE IF NOT EXISTS tracks (
            track_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            length INTEGER,
            file_path TEXT UNIQUE,
            artwork TEXT,
            is_favorite INTEGER DEFAULT 0,
            play_count INTEGER DEFAULT 0,
            last_played TIMESTAMP,
            added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """

    CREATED_PLAYLISTS_TABLE = """
        CREATE TABLE IF NOT EXISTS playlists (
            playlist_id INTEGER PRIMARY KEY AUTOINCREMENT,
            playlist_name TEXT UNIQUE
        )
    """

    CREATED_PLAYLIST_TRACK_TABLE = """
        CREATE TABLE IF NOT EXISTS playlist_track (
            playlist_id INTEGER,
            track_id INTEGER,
            PRIMARY KEY (playlist_id, track_id)
            FOREIGN KEY (playlist_id) REFERENCES playlists(playlist_id) ON DELETE CASCADE,
            FOREIGN KEY (track_id) REFERENCES tracks(track_id) ON DELETE CASCADE
        )
    """

    def __init__(self, db_name="music_library.db"):

        # database file path
        project_root = Path(__file__).parent.parent
        data_dir = project_root / "data"
        data_dir.mkdir(exist_ok=True)
        db_path = data_dir / db_name

        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute(self.CREATED_TRACKS_TABLE)
            self.conn.execute(self.CREATED_PLAYLISTS_TABLE)
            self.conn.execute(self.CREATED_PLAYLIST_TRACK_TABLE)

    # ==» Tracks Table Method «==-----------------------------

    # » inserted «
    def insert_track(self, meta):
        query = """
            INSERT OR IGNORE INTO tracks
            (title,file_path, length, artwork)
            VALUES (?, ?, ?, ?)
        """
        metadata = (meta["title"], meta["file_path"], meta["length"], meta["artwork"])
        with self.conn:
            cur = self.conn.execute(query, metadata)
        if cur.rowcount == 0:
            return None
        return cur.lastrowid

    # » readed «
    def get_all_tracks(self):
        cursor = self.conn.execute(
            "SELECT track_id, title, is_favorite, file_path, length, artwork FROM tracks"
        )
        return self._rows_to_tracks(cursor.fetchall())

    def get_favourite_tracks(self):
        query = """
            SELECT track_id, title, is_favorite, file_path, length, artwork FROM tracks
            WHERE is_favorite = 1
            ORDER BY last_played DESC
        """
        cursor = self.conn.execute(query)
        return self._rows_to_tracks(cursor.fetchall())

    def get_last_played(self):
        query = """
            SELECT track_id, title, is_favorite, file_path, length, artwork FROM tracks
            WHERE last_played IS NOT NULL
            ORDER BY last_played DESC LIMIT 10
        """
        cursor = self.conn.execute(query)
        return self._rows_to_tracks(cursor.fetchall())

    # » updated «
    def toggle_favorite(self, track_id):
        cursor = self.conn.execute(
            "SELECT is_favorite FROM tracks WHERE track_id = ?", (track_id,)
        )
        row = cursor.fetchone()

        if row:
            current_status = row[0]
            new_status = 1 if current_status == 0 else 0

            # حالا آپدیت کن
            query = "UPDATE tracks SET is_favorite = ? WHERE track_id = ?"
            with self.conn:
                self.conn.execute(query, (new_status, track_id))
            return new_status
        return None

    def update_last_played(self, track_id):
        query = """
            UPDATE tracks SET
                play_count = play_count + 1,
                last_played = CURRENT_TIMESTAMP
                WHERE track_id = ?
        """
        with self.conn:
            self.conn.execute(query, (track_id,))

    def update_track_artwork_path(self, track_id, artwork_path):
        with self.conn:
            self.conn.execute(
                "UPDATE tracks SET artwork = ? WHERE track_id = ?",
                (artwork_path, track_id),
            )

    # » deleted «
    def deleted_track(self, track_id):
        with self.conn:
            self.conn.execute("DELETE FROM tracks WHERE track_id = ?", (track_id,))

    # ==» Playlists Table Method «==-----------------------------

    # » inserted «
    def insert_to_Playlists(self, playlist_name):
        with self.conn:
            cur = self.conn.execute(
                "INSERT OR IGNORE INTO playlists (playlist_name) VALUES (?)", (playlist_name,)
            )
        return cur.lastrowid

    # » readed «
    def get_all_playlist(self):
        cursor = self.conn.execute("SELECT * FROM playlists")
        return [PlayLists(id=r[0], name=r[1]) for r in cursor.fetchall()]
    
    # » updated «
    def update_playlist_name(self, playlists_id, new_playlists_name):
        with self.conn:
            self.conn.execute(
                "UPDATE playlists SET playlist_name = ? WHERE playlist_id = ?",
                (new_playlists_name, playlists_id)
                )
    
    # » deleted «
    def deleted_playlist(self, playlists_id):
        with self.conn:
            self.conn.execute(
                "DELETE FROM playlists WHERE playlist_id = ?",
                (playlists_id),
                )

    # ==» Playlists_Tracks Table Method «==-----------------------------

    # » inserted «
    def insert_playlist_track(self, playlist_id, music_id):
        with self.conn:
            self.conn.execute(
                "INSERT OR IGNORE INTO playlist_track (playlist_id, track_id) VALUES (?, ?)",
                (playlist_id, music_id),
            )

    # » readed «
    def get_music_by_playlist(self, playlist_id):
        query = """
            SELECT tracks.track_id, tracks.title, tracks.is_favorite, tracks.file_path, tracks.length, tracks.artwork FROM tracks
            JOIN playlist_track ON tracks.track_id = playlist_track.track_id
            WHERE playlist_track.playlist_id = ?
        """
        cursor = self.conn.execute(query, (playlist_id,))
        return self._rows_to_tracks(cursor.fetchall())

    # ==» Shared Database Helpers «==-----------------------------
    def _rows_to_tracks(self, rows):
        return [
            Track(
                track_id=r[0],
                title=r[1],
                is_favorite=bool(r[2]),
                file_path=r[3],
                length=r[4],
                artwork=r[5],
            )
            for r in rows
        ]
    
if __name__ == "__main__":
    db = MusicDatabase()
