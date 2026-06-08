import os
import shutil
from core.track import Track
from core.playlist import PlayLists
from utils.file_utils import get_media_path, extract_metadata, delete_file, format_time
from utils.image_utils import save_artwork_cache
import threading


class Controller:
    def __init__(self, player, db):

        # Core controller dependencies :
        self.player = player
        self.db = db
        self.ui = None

        # Currently visible UI state :
        # File path of the currently selected track
        self.current_file_path = None

        # Index of the item currently selected in the main listbox
        self.current_index = None

        # Currently selected tracks
        self.visible_tracks: list[Track] = []

        # Static information for tracks, playlists, and top-levels :
        # Information about all tracks in the database
        self.all_tracks_info: list[Track] = []

        # Information about all playlists in the database
        self.all_playlists_info: list[PlayLists] = []

        # Dictionary for storing top-level windows
        self.top_windows = {}

        # Threading: database lock (heavy operations) and progress bar updates :
        self.db_lock = threading.Lock()

    # ==»» UI → Controller ««==-----------------------------
    def set_ui(self, ui):
        self.ui = ui
        self.on_show_all_tracks_clicked()

    # ==»» Toplevels → Contriller → Toplevels ««==-----------------------------
    def open_playlists_window(self):
        from ui.toplevels.playlists_window import PlaylistsWindow

        self.all_playlists_info = self.db.get_all_playlist()
        playlists_name = [playlist.name for playlist in self.all_playlists_info]
        playlists_window = PlaylistsWindow(master=self.ui, controller=self)
        playlists_window.refresh_listbox_playlists_window(playlists_name)
        self.top_windows["playlists_window"] = playlists_window
        playlists_window.grab_set()

    def open_create_playlist_window(self):
        from ui.toplevels.create_playlist_window import CreatePlaylistWindow

        self.all_tracks_info = self.db.get_all_tracks()
        tracks = [track.title for track in self.all_tracks_info]
        create_playlist_window = CreatePlaylistWindow(
            master=self.top_windows["playlists_window"], controller=self
        )
        create_playlist_window.refresh(tracks)
        self.top_windows["create_playlist_window"] = create_playlist_window
        create_playlist_window.grab_set()

    def open_track_actions_window(self):
        from ui.toplevels.track_actions_window import TrackActionsWindow

        track_actions_window = TrackActionsWindow(master=self.ui, controller=self)
        self.top_windows["track_actions_window"] = track_actions_window
        track_actions_window.grab_set()

    def open_add_to_playlist_window(self):
        from ui.toplevels.add_to_playlist_window import AddToPlaylistWindow

        self.all_playlists_info = self.db.get_all_playlist()
        add_to_playlist_window = AddToPlaylistWindow(
            master=self.top_windows["track_actions_window"], controller=self
        )
        self.top_windows["add_to_playlist_window"] = add_to_playlist_window
        self._load_playlists_to_add_playlist_listbox()
        add_to_playlist_window.grab_set()
        if not self.all_playlists_info:
            self.top_windows["add_to_playlist_window"]._hide_destry()

    # ==»» User Events ««==-----------------------------
    def on_track_selected(self, filename):

        # Controller attributes initialization
        self.current_index = self.ui.get_selected_index_main_listbox()
        track = self.visible_tracks[self.current_index]
        self.current_file_path = track.file_path

        # Send the track file path to the player engine
        self.player.play(track.file_path)

        # Update the recently played track record in the database
        self.db.update_last_played(track.track_id)

        # See line 357 for details.
        self._get_current_time()
        self._get_music_time_len()

        # Update the UI
        self.ui.real_time.set(0)
        self.ui.update_title(filename)
        self.ui.update_artwork(track.artwork)
        self.ui.update_pause_unpause_btn(True)
        if track.is_favorite == 1:
            self.ui.update_toggle_favorite_btn(True)
        else:
            self.ui.update_toggle_favorite_btn(False)
        self.ui.reset_search_entry()
    
    # Update playback time, refresh UI labels, and handle track completion :
    def _get_current_time(self):
        current_time = self.ui.real_time.get() + self.player.get_pg_postion()
        self.ui.update_lab_current(format_time(current_time))
        self.ui.state_var.set(current_time)
        if current_time + 1 == self.ui.music_len.get():
            self.ui.select_main_listbox(self.current_index)
        self.ui.after(1000, self._get_current_time)

    def _get_music_time_len(self):
        track = self.visible_tracks[self.current_index]
        self.ui.music_len.set(track.length)
        self.ui.update_lab_time_len(format_time(track.length))
        self.ui.update_slider_to(track.length)
    
    def on_playlist_selected(self, index):
        playlist = self.all_playlists_info[index]
        self.visible_tracks = self.db.get_music_by_playlist(playlist.id)
        self._refresh_visible_tracks()
        self.ui.reset_search_entry()
    
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

    # ==»» Playback ««==-----------------------------
    def on_pause_unpause_clicked(self):
        if not self.current_index is None:
            paused = self.player.pause_unpause()
            self.ui.update_pause_unpause_btn(not paused)
        else:
            pass
    
    def on_next_track_clicked(self):
        if not self.current_index is None:
            current = self.current_index
            if current is None:
                return
            next_index = self.player.next_index(current, len(self.visible_tracks) - 1)
            self.ui.select_main_listbox(next_index)
        else:
            pass

    def on_previous_track_clicked(self):
        if not self.current_index is None:
            current = self.current_index
            if current is None:
                return

            prev_index = self.player.previous_index(current)
            self.ui.select_main_listbox(prev_index)
        else:
            pass

    def on_stop_clicked(self):
        if not self.current_index is None:
            self.player.stop()
            self.ui.reset_ui()
            self.ui.unselect_main_listbox(self.current_index)
            self.current_index = None
            self.ui.reset_search_entry()
    
    def on_time_slider_clicked(self, state):
        if self.current_index or self.current_index == 0:
            self.ui.real_time.set(state)
            self.player.play(self.current_file_path, state)
            self.ui.update_pause_unpause_btn(True)
        else:
            pass
    
    def on_volume_clicked(self, vol):
        self.player.set_volume(vol)
    
    # ==»» Playlist ««==-----------------------------
    def add_tracks_to_library(self, file_paths):

        if not file_paths:
            return

        self.ui.show_Adding_overlay()

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

                    file_name = os.path.basename(src_path)

                    dest_path = os.path.join(get_media_path(), file_name)

                    if os.path.exists(dest_path):
                        skipped += 1

                    else:

                        shutil.copy2(src_path, dest_path)

                        meta = extract_metadata(dest_path)

                        if not meta:
                            errors += 1
                            continue

                        meta["file_path"] = dest_path

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

        self.ui.hide_loading_overlay()

        self.on_show_all_tracks_clicked()

        print(f"Added: {added}, " f"Skipped: {skipped}, " f"Errors: {errors}")

    def remove_track(self):

        track_list, index = self._find_track_location_by_file_path(
            self.current_file_path
        )

        if index is None:
            self.top_windows["track_actions_window"].after(
                10, lambda: self.top_windows["track_actions_window"].destroy()
            )
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

        if "track_actions_window" in self.top_windows:
            try:
                self.top_windows["track_actions_window"].destroy()
            except Exception:
                pass

    def create_playlist_with_tracks(
        self, name, tracks
    ):

        playlist_id = self.db.insert_to_Playlists(name) # این تابع ایدی پلی لیست مد نظر را برمیگرداند
        for t in tracks:
            track = self.all_tracks_info[t]
            self.db.insert_playlist_track(playlist_id, track.track_id)
        self.all_playlists_info = self.db.get_all_playlist()
        playlist_name = [playlist.name for playlist in self.all_playlists_info]
        self.top_windows["playlists_window"].refresh_listbox_playlists_window(playlist_name)
    
    def on_add_to_playlist_clicked(self, name):
        if self.current_index is not None:
            index = self.top_windows["add_to_playlist_window"].get_idx_listbox()
            playlist_info = self.all_playlists_info[index]
            track_id = self.visible_tracks[self.current_index]
            self.db.insert_playlist_track(
                playlist_info.id,
                track_id.track_id,
            )
            self.top_windows["add_to_playlist_window"].after(
                10, lambda: self.top_windows["add_to_playlist_window"].destroy()
            )
        else:
            self.top_windows["add_to_playlist_window"].after(
                10, lambda: self.top_windows["add_to_playlist_window"].destroy()
            )

    def _load_playlists_to_add_playlist_listbox(self):
        if self.all_playlists_info:
            playlist_name = [playlist.name for playlist in self.all_playlists_info]
            self.top_windows["add_to_playlist_window"].refresh(playlist_name)
        else:
            self.top_windows["add_to_playlist_window"].show_empty_playlist_frame()

    # ==»» Track Library ««==-----------------------------
    def on_show_all_tracks_clicked(self):
        
        self.ui.show_loading_overlay()

        def load():

            self.ui.main_listbox_del()

            self.all_tracks_info = self.db.get_all_tracks()
            self.visible_tracks = self.all_tracks_info
            tracks = [song.title for song in self.visible_tracks]

            self.ui.main_listbox_insert(tracks)

            self.ui.hide_loading_overlay()

        self.ui.after(10, load)
        self.ui.reset_search_entry()
    
    def on_show_favorites_tracks_clicked(self):

        self.ui.show_loading_overlay()

        def load():

            self.ui.main_listbox_del()

            self.visible_tracks = self.db.get_favourite_tracks()

            tracks = [song.title for song in self.visible_tracks]

            self.ui.main_listbox_insert(tracks)

            self.ui.hide_loading_overlay()

        self.ui.after(10, load)
        self.ui.reset_search_entry()

    def on_show_last_played_clicked(self):

        self.ui.show_loading_overlay()

        def load():

            self.ui.main_listbox_del()

            self.visible_tracks = self.db.get_last_played()

            tracks = [song.title for song in self.visible_tracks]

            self.ui.main_listbox_insert(tracks)

            self.ui.hide_loading_overlay()

        self.ui.after(10, load)
        self.ui.reset_search_entry()

    def on_toggle_favorite_clicked(self):
        if self.current_index is not None:
            track = self.visible_tracks[self.current_index]
            new_state = self.db.toggle_favorite(track.track_id)

            track.is_favorite = new_state

            if new_state == 1:
                self.ui.update_toggle_favorite_btn(True)
            else:
                self.ui.update_toggle_favorite_btn(False)
            self.ui.reset_search_entry()
        else:
            pass
            
    # ==»» Search ««==-----------------------------
    def search_tracks(self, query: str):

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

    # ==»» Shared Controller Helpers ««==-----------------------------
    def _refresh_visible_tracks(self):

        self.ui.show_loading_overlay()

        def load():

            self.ui.main_listbox_del()

            tracks = [song.title for song in self.visible_tracks]

            self.ui.main_listbox_insert(tracks)

            self.ui.hide_loading_overlay()

        self.ui.after(10, load)
    
    def _find_track_location_by_file_path(self, file_path):

        for index, track in enumerate(self.visible_tracks):
            if track.file_path == file_path:
                return self.visible_tracks, index

        for index, track in enumerate(self.all_tracks_info):
            if track.file_path == file_path:
                return self.all_tracks_info, index

        return None, None