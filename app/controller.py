import os
import shutil
from core.track import Track
from core.playlist import PlayLists
from utils.file_utils import get_media_path, extract_metadata, delete_file, format_time, save_artwork_cache
import threading
from pathlib import Path




class Controller:

    def __init__(self, player, db):

        # Core controller dependencies
        self.player = player
        self.db = db
        self.ui = None

        # Currently visible UI state
        # File path of the currently selected track
        self.current_file_path = None

        # Index of the item currently selected in the main listbox
        self.current_index = None

        self.current_playlist_id = None

        # Current playback position (seconds)
        self.seek_offset = 0

        # Currently selected tracks
        self.visible_tracks: list[Track] = []

        # Static information for tracks, playlists, and top-levels
        # Information about all tracks in the database
        self.all_tracks_info: list[Track] = []

        # Information about all playlists in the database
        self.all_playlists_info: list[PlayLists] = self.db.get_all_playlist()

        # Threading: database lock (heavy operations) and progress bar updates
        self.db_lock = threading.Lock()

        self.separator_state = None

    # ==» UI → Controller «==-----------------------------
    def set_ui(self, ui):
        self.ui = ui
        self.on_show_all_tracks_clicked()

    # ==» User Events «==-----------------------------
    def track_selected(self, file_path=None):
        
        # Controller attributes initialization
        if file_path == None:
            self.current_index = self.ui.get_selected_index_main_listbox()
            track = self.visible_tracks[self.current_index]
            self.current_file_path = track.file_path
        else:
            list_track, index = self._find_track_location_by_file_path(self.current_file_path)
            track = list_track[index]

        # Send the track file path to the player engine
        self.player.play(track.file_path)

        # Update the recently played track record in the database
        self.db.update_last_played(track.track_id)

        # See line 76 for details.
        self._get_current_time()
        self._get_music_time_len()

        # Update the UI
        self.seek_offset = 0
        self.ui.update_track_title(track.title, track.artist)

        try:
            self.ui.set_artwork(track.artwork)
        except Exception as e:
            print("ARTWORK ERROR:", e)

        self.ui.update_pause_unpause_btn(True)
        if track.is_favorite == 1:
            self.ui.update_toggle_favorite_btn(True)
        else:
            self.ui.update_toggle_favorite_btn(False)
        self.ui.reset_search_entry()

    # Update playback time, refresh UI labels, and handle track completion :
    def _get_current_time(self):
        current_time = self.seek_offset + self.player.get_pg_postion()
        self.ui.update_lab_current(format_time(int(current_time)))
        self.ui.time_slider_position_var.set(int(current_time))
        if int(current_time) == self.ui.track_length_var.get() - 2:
            if self.ui.repeat_mode:
                self.seek_offset = 0
                self.track_selected(self.current_file_path)
            else:
                self.on_next_track_clicked()

        self.ui.after(1000, self._get_current_time)

    def _get_music_time_len(self):
        list_track, index = self._find_track_location_by_file_path(self.current_file_path)
        track = list_track[index]
        self.ui.track_length_var.set(track.length)
        self.ui.update_lab_time_len(format_time(track.length))
        self.ui.update_slider_to(track.length)
    
    def on_playlist_selected(self, index):
        playlist = self.all_playlists_info[index]
        self.current_playlist_id = playlist.id
        self.visible_tracks = self.db.get_music_by_playlist(playlist.id)
        self._refresh_visible_tracks()
        self.ui.reset_search_entry()
        self.ui.update_empty_state(self.visible_tracks, "playlist_run")
    
    def on_key_pressed(self, event):
        if event.keysym == "space":
            self.on_pause_unpause_clicked()
        elif event.keysym == "Right":
            self.on_next_track_clicked()
        elif event.keysym == "Left":
            self.on_previous_track_clicked()
        elif event.keysym == "Delete":
            self.remove_track()
        elif event.keysym == "Escape":
            self.ui.destroy()

    # ==» Playback «==-----------------------------
    def on_pause_unpause_clicked(self):
        if self.current_index is not None:
            paused = self.player.pause_unpause()
            self.ui.update_pause_unpause_btn(not paused)
        else:
            self.ui.show_hint()
            self.ui.hide_hint()
    
    def on_next_track_clicked(self):
        if not self.current_index is None:
            current = self.current_index
            if current is None:
                return
            next_index = self.player.next_index(current, len(self.visible_tracks) - 1)
            self.ui.select_main_listbox(next_index)
        else:
            self.ui.show_hint()
            self.ui.hide_hint()

    def on_previous_track_clicked(self):
        if not self.current_index is None:
            current = self.current_index
            if current is None:
                return

            prev_index = self.player.previous_index(current)
            self.ui.select_main_listbox(prev_index)
        else:
            self.ui.show_hint()
            self.ui.hide_hint()

    def on_stop_clicked(self):
        if self.current_index is not None:
            self.player.stop()
            self.ui.after(10, self.ui.reset_ui)
            if self.ui.get_selected_index_main_listbox():
                self.ui.unselect_main_listbox(self.current_index)
            self.current_index = None
            self.current_file_path = None
            self.ui.reset_search_entry()
        else:
            self.ui.show_hint() 
            self.ui.hide_hint()
    
    def on_time_slider_clicked(self, state):
        if self.current_index is not None:
            self.seek_offset = state
            self.player.play(self.current_file_path, state)
            self.ui.update_pause_unpause_btn(True)
    
    def on_volume_clicked(self, vol):
        self.player.set_volume(vol)
    
    # ==» Playlist «==-----------------------------
    def add_tracks_to_library(self, file_paths):

        if not file_paths:
            return

        self.ui.show_progress()

        threading.Thread(
            target=self._add_tracks_worker, args=(file_paths,), daemon=True
        ).start()

    def _add_tracks_worker(self, file_paths):

        added = 0
        skipped = 0
        errors = 0

        total = len(file_paths)

        try:

            for current, src_path in enumerate(file_paths, start=1):

                try:

                    file_name = Path(src_path).name

                    dest_path = get_media_path() / file_name

                    if dest_path.exists():
                        skipped += 1

                    else:

                        shutil.copy2(src_path, dest_path)

                        meta = extract_metadata(dest_path)

                        if not meta:
                            errors += 1
                            continue

                        meta["file_path"] = str(dest_path)

                        artwork_bytes = meta.get("artwork")
                        meta["artwork"] = None

                        with self.db_lock:

                            track_id = self.db.insert_track(meta)

                            if not track_id:
                                skipped += 1
                                continue

                            if artwork_bytes:

                                artwork_path = save_artwork_cache(
                                    artwork_bytes, track_id
                                )

                                if artwork_path:
                                    self.db.update_track_artwork_path(
                                        track_id, artwork_path
                                    )

                        added += 1

                except Exception as e:

                    errors += 1
                    print("Import error:", e)

                progress = current / total

                self.ui.after(0, lambda p=progress: self.ui.update_progress(p))

        finally:

            self.ui.after(0, lambda: self._add_tracks_finished(added, skipped, errors))

    def _add_tracks_finished(self, added, skipped, errors):

        self.ui.hide_status()

        self.on_show_all_tracks_clicked()
        self.ui.show_messagebox(added, skipped, errors)

    def remove_track(self):

        track_list, index = self._find_track_location_by_file_path(
            self.current_file_path
        )

        if index is None:
            self.ui.hide_track_actions_frame()
            return

        track = track_list[index]
        track_id = track.track_id
        file_path = track.file_path

        if index == 0:
            new_track = index + 1
        else:
            new_track = index - 1

        self.player.stop()

        threading.Thread(
            target=self._remove_music_worker,
            args=(track_list, index, track_id, file_path, new_track),
            daemon=True,
        ).start()

    def _remove_music_worker(self, track_list, index, track_id, file_path, new_track):

        try:
            delete_file(file_path)
            self.db.deleted_track(track_id)
            del track_list[index]

        finally:
            self.ui.after(0, lambda: self._remove_music_finished(new_track))

    def _remove_music_finished(self, new_track):

        if self.visible_tracks:
            if new_track >= len(self.visible_tracks):
                new_track = len(self.visible_tracks) - 1
            self.ui.select_main_listbox(new_track)
            self._refresh_visible_tracks()

        else:
            self.ui.reset_ui()
            self.current_index = None
            self.on_show_all_tracks_clicked()

    def create_playlist_with_tracks(self, name, tracks):
        playlist_id = self.db.insert_to_Playlists(name) # این تابع ایدی پلی لیست مد نظر را برمیگرداند
        for t in tracks:
            track = self.all_tracks_info[t]
            self.db.insert_playlist_track(playlist_id, track.track_id)
        playlist_name = self.get_playlist_name()
        self.ui.refresh_listbox_playlists_frame(playlist_name)
        self.ui.update_empty_state(True, "playlists")

    
    def on_add_to_playlist_clicked(self, none):
        if self.current_index is not None:
            index = self.ui.get_index_listbox()
            playlist_info = self.all_playlists_info[index]
            list_track, index = self._find_track_location_by_file_path(self.current_file_path)
            track_id = list_track[index]
            self.db.insert_playlist_track(
                playlist_info.id,
                track_id.track_id,
            )
            self.ui.hide_add_to_playlist_frame()
            self.ui.hide_track_actions_frame()
        else:
            self.ui.hide_add_to_playlist_frame()
            self.ui.hide_track_actions_frame()

    def on_delete_playlist_clicked(self):
        if self.ui.get_playlist_selected_index() is not None:
            self.ui.hide_playlist_deleted_frame()
            index = self.ui.get_playlist_selected_index()
            playlist = self.all_playlists_info[index]
            self.db.deleted_playlist(playlist.id)
            playlist_name = self.get_playlist_name()
            self.ui.refresh_listbox_playlists_frame(playlist_name)
            self.ui.update_empty_state(self.all_playlists_info, "playlists")
            if playlist.id == self.current_playlist_id:
                self.on_show_all_tracks_clicked()
        else:
            self.ui.playlist_alert()
 
    def rename_playlist(self, new_playlist_name):
        index = self.ui.get_playlist_selected_index()
        playlist = self.all_playlists_info[index]
        self.db.update_playlist_name(playlist.id, new_playlist_name)
        playlist_name = self.get_playlist_name()
        self.ui.refresh_listbox_playlists_frame(playlist_name)
        
    # ==» Track Library «==-----------------------------
    def on_show_all_tracks_clicked(self):
        
        self.ui.set_separator("all_tracks")
        self.separator_state = "all_tracks"
        self.ui.hide_playlists_frame()

        if hasattr(self.ui, 'create_playlist_frame') and self.ui.create_playlist_frame.winfo_exists():
            self.ui.hide_created_playlist_frame()

        self.ui.show_loading()

        self.all_tracks_info = self.db.get_all_tracks()
        self.visible_tracks = self.all_tracks_info
        tracks = [song.title for song in self.visible_tracks]

        def load():
            self.ui.main_listbox_del()
            self.ui.main_listbox_insert(tracks)
            self.ui.hide_status()

        self.ui.after(10, load)
        self.ui.reset_search_entry()

        self.ui.update_empty_state(self.visible_tracks, "all_tracks")
    
    def on_show_favorites_tracks_clicked(self):

        self.ui.set_separator("favorites")
        self.separator_state = "favorites"
        self.ui.hide_playlists_frame()

        if hasattr(self.ui, 'create_playlist_frame') and self.ui.create_playlist_frame.winfo_exists():
            self.ui.hide_created_playlist_frame()

        self.ui.show_loading()

        self.visible_tracks = self.db.get_favourite_tracks()
        tracks = [song.title for song in self.visible_tracks]

        def load():
            self.ui.main_listbox_del()
            self.ui.main_listbox_insert(tracks)
            self.ui.hide_status()

        self.ui.after(10, load)
        self.ui.reset_search_entry()
        
        self.ui.update_empty_state(self.visible_tracks, "favorites")

    def on_show_last_played_clicked(self):

        self.ui.set_separator("recently_played")
        self.separator_state = "recently_played"
        self.ui.hide_playlists_frame()

        if hasattr(self.ui, 'create_playlist_frame') and self.ui.create_playlist_frame.winfo_exists():
            self.ui.hide_created_playlist_frame()

        self.ui.show_loading()

        self.visible_tracks = self.db.get_last_played()
        tracks = [song.title for song in self.visible_tracks]

        def load():
            self.ui.main_listbox_del()
            self.ui.main_listbox_insert(tracks)
            self.ui.hide_status()

        self.ui.after(10, load)
        self.ui.reset_search_entry()

        self.ui.update_empty_state(self.visible_tracks, "all_tracks")

    def on_toggle_favorite_clicked(self):
        if self.current_index is not None:
            list_track, index = self._find_track_location_by_file_path(self.current_file_path)
            track = list_track[index]
            new_state = self.db.toggle_favorite(track.track_id)

            track.is_favorite = new_state

            if new_state == 1:
                self.ui.update_toggle_favorite_btn(True)
            else:
                self.ui.update_toggle_favorite_btn(False)
            self.ui.reset_search_entry()
        else:
            self.ui.show_hint()
            self.ui.hide_hint()
            
    # ==» Search «==-----------------------------
    def search_tracks(self, query: str):

        self.ui.set_separator(None)
        query = query.lower().strip()

        # Search tracks by title.
        results = [
            track for track in self.all_tracks_info if query in track.title.lower()
        ]

        # Results with titles closer in length to the query are ranked higher.
        results.sort(
            key=lambda track: (
                abs(len(track.title) - len(query)),
                track.title.lower(),
            )
        )

        # Ties are resolved alphabetically.

        self.visible_tracks = results
        self._refresh_visible_tracks()
        self.ui.update_empty_state(self.visible_tracks, "searching")

    # ==» Shared Controller Helpers «==-----------------------------
    def _refresh_visible_tracks(self):

        self.ui.show_loading()

        def load():

            self.ui.main_listbox_del()

            tracks = [song.title for song in self.visible_tracks]

            self.ui.main_listbox_insert(tracks)

            self.ui.hide_status()

        self.ui.after(10, load)
    
    def _find_track_location_by_file_path(self, file_path):

        for index, track in enumerate(self.visible_tracks):
            if track.file_path == file_path:
                return self.visible_tracks, index

        for index, track in enumerate(self.all_tracks_info):
            if track.file_path == file_path:
                return self.all_tracks_info, index

        return None, None
    
    def get_playlist_name(self):
        self.all_playlists_info = self.db.get_all_playlist()
        playlist_name = []
        for playlist in self.all_playlists_info:
            if self.db.get_music_by_playlist(playlist.id):
                playlist_name.append(playlist.name)
            else:
                self.db.deleted_playlist(playlist.id)
        return playlist_name
    
    def get_all_track_title(self):
        self.all_tracks_info = self.db.get_all_tracks()
        tracks = [track.title for track in self.all_tracks_info]
        return tracks