import customtkinter as ctk
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
from io import BytesIO
import os
from CTkListbox import CTkListbox
from tkinter.filedialog import askopenfilenames
from utils.file_utils import resource_path

class MusicPlayerUI(ctk.CTk):

    def __init__(self, controller):
        super().__init__(fg_color="black")
        self.title("Music Player")
        self.geometry("1266x668+40+30")
        self.resizable(False, False)

        # Core UI dependencies
        self.controller = controller

        # Total duration of the current track (seconds)
        self.track_length_var = ctk.IntVar(value=0)

        # Variable bound to the playback time slider
        self.time_slider_position_var = ctk.IntVar(value=0)
        
        self.build_ui()
        self.set_artwork(self.default_artwork_path)
        self.bind("<Key>", self.controller.on_key_pressed)

    # ==» UI Construction «==---------------------------
    def build_ui(self):

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # ==» Artwork Frame «==---------------------------
        artwork_frame = ctk.CTkFrame(
            self,
            fg_color="#000009",
        )
        artwork_frame.grid(column=1, row=0, sticky="nsew")

        # Background lable
        self.background = ctk.CTkLabel(artwork_frame, text="")
        self.background.place(x=0, y=0)

        # artwork lable
        self.art_label = ctk.CTkLabel(artwork_frame, text="")
        self.art_label.pack()

        # track title lable
        self.track_title_label = ctk.CTkLabel(
            artwork_frame,
            text="",
            font=ctk.CTkFont(size=35, weight="bold"),
        )
        self.track_title_label.pack(pady=10)

        self.default_artwork_path = "assets/images/artwork.png"

        # ==» Playback Controls Frame «==---------------------------
        playback_controls_frame = ctk.CTkFrame(self, height=90, fg_color="#000005")
        playback_controls_frame.grid(column=1, row=1, sticky="nsew")
        playback_controls_frame.columnconfigure((0, 2), weight=0)
        playback_controls_frame.columnconfigure(1, weight=1)
        playback_controls_frame.rowconfigure(0, weight=1)

        # --==» Playback Buttons Frame «==--
        playback_buttons_frame = ctk.CTkFrame(playback_controls_frame, height=50, fg_color="#000005")
        playback_buttons_frame.grid(column=0, row=0, sticky="nsew")
        playback_buttons_frame.grid_columnconfigure(([i for i in range(0, 6)]), weight=0)
        playback_buttons_frame.grid_rowconfigure(0, weight=1)

        # icon buttons
        self.unpause_icon = ctk.CTkImage(
            Image.open(
                resource_path("assets/icons/start_dark_new.png")
            ),
            size=(40, 40),
        )
        self.pause_icon = ctk.CTkImage(
            Image.open(resource_path("assets/icons/stop_dark_new.png")),
            size=(40, 40),
        )

        self.favorite_icon_deselect = ctk.CTkImage(
            Image.open(resource_path("assets/icons/favorite_.png")),
            size=(17, 17),
        )
        self.favorite_icon_select = ctk.CTkImage(
            Image.open(resource_path("assets/icons/likedo.png")),
            size=(17, 17),
        )

        # stop button
        ctk.CTkButton(
            playback_buttons_frame,
            text="",
            width=0,
            height=0,
            fg_color="transparent",
            image=ctk.CTkImage(
            Image.open(resource_path("assets/icons/stop.png")),
            size=(22, 22),
        ),
            bg_color="#000005",
            border_width=0,
            hover_color="#000010",
            command=self.controller.on_stop_clicked,
        ).grid(column=0, row=0, padx=7)

        # previous button
        ctk.CTkButton(
            playback_buttons_frame,
            width=0,
            height=0,
            text="",
            bg_color="transparent",
            fg_color="transparent",
            image=ctk.CTkImage(
            Image.open(resource_path("assets/icons/skip_previous.png")),
            size=(30, 30),
        ),
            hover_color="#000010",
            command=self.controller.on_previous_track_clicked,
        ).grid(column=1, row=0)

        self.pause_unpause_btn = ctk.CTkButton(
            playback_buttons_frame,
            width=0,
            height=0,
            text="",
            bg_color="transparent",
            fg_color="transparent",
            image=self.pause_icon,
            hover_color="#000010",
            command=self.controller.on_pause_unpause_clicked,
        )
        self.pause_unpause_btn.grid(column=2, row=0, padx=5)

        # next button
        ctk.CTkButton(
            playback_buttons_frame,
            width=0,
            height=0,
            text="",
            bg_color="transparent",
            fg_color="transparent",
            image=ctk.CTkImage(
            Image.open(resource_path("assets/icons/skip_next.png")),
            size=(30, 30),
        ),
            hover_color="#000010",
            command=self.controller.on_next_track_clicked,
        ).grid(column=3, row=0)

        self.repeat_mode_btn = ctk.CTkButton(
            playback_buttons_frame,
            text="",
            width=0,
            height=0,
            fg_color="transparent",
            image=ctk.CTkImage(
                Image.open(resource_path("assets/icons/repeat_one.png")),
                size=(20, 20),
            ),
            bg_color="#000003",
            border_width=0,
            state="disabled",
            # command=
        )
        self.repeat_mode_btn.grid(column=4, row=0, padx=(7, 12))

        # separator_label
        ctk.CTkLabel(
            playback_buttons_frame,
            text="",
            image=ctk.CTkImage(
                Image.open(resource_path("assets/icons/texture.png")),
                size=(1, 35),
            ),
        ).grid(column=5, row=0, padx=(5, 10))

        # --==» Time Slider Frame «==--
        time_slider_frame = ctk.CTkFrame(playback_controls_frame, height=50, fg_color="#000005")
        time_slider_frame.grid(column=1, row=0, sticky="ew")
        time_slider_frame.pack_propagate(False)
        time_slider_frame.grid_columnconfigure(1, weight=1)
        time_slider_frame.grid_columnconfigure((0, 2), weight=0)
        time_slider_frame.grid_rowconfigure(0, weight=1)

        # current position lable
        self.current_position_lable = ctk.CTkLabel(time_slider_frame, text="00:00")
        self.current_position_lable.grid(column=0, row=0, padx=5, sticky="nsew")

        self.time_slider = ctk.CTkSlider(
            time_slider_frame,
            progress_color="#0D3F8B",
            button_color="#FFFFFF",
            fg_color="#151515",
            button_hover_color="#dbdbdb",
            from_=0,
            to=100,
            variable=self.time_slider_position_var,
            command=self.controller.on_time_slider_clicked,
        )
        self.time_slider.grid(column=1, row=0, sticky="ew")

        # track length lable
        self.track_length_lable = ctk.CTkLabel(time_slider_frame, text="00:00")
        self.track_length_lable.grid(column=2, row=0, padx=5, sticky="nsew")

        # --==» Volume Controls Frame «==--
        volume_controls_frame = ctk.CTkFrame(playback_controls_frame, height=50, fg_color="#000005")
        volume_controls_frame.grid(column=2, row=0, sticky="nsew")
        volume_controls_frame.columnconfigure((0, 1, 3, 4), weight=0)
        volume_controls_frame.columnconfigure(2, weight=1)
        volume_controls_frame.rowconfigure(0, weight=1)

        # separator_label
        ctk.CTkLabel(
            volume_controls_frame,
            text="",
            image=ctk.CTkImage(
                Image.open(resource_path("assets/icons/texture.png")),
                size=(1, 35),
            ),
        ).grid(column=0, row=0, padx=10)

        # volume icon
        ctk.CTkLabel(
            volume_controls_frame,
            text="",
            image=ctk.CTkImage(
                Image.open(resource_path("assets/icons/volume.png")),
                size=(20, 20),
            ),
        ).grid(column=1, row=0, padx=(12, 0))
        
        self.toggle_favorite_btn = ctk.CTkButton(
            volume_controls_frame,
            text="",
            image=self.favorite_icon_deselect,
            width=0,
            height=0,
            hover_color="#000010",
            fg_color="transparent",
            border_width=0,
            command=self.controller.on_toggle_favorite_clicked,
        )
        self.toggle_favorite_btn.grid(column=3, row=0, padx=(13, 0))

        self.volume_slider = ctk.CTkSlider(
            volume_controls_frame,
            fg_color="#151515",
            width=110,
            height=10,
            progress_color="#0D3F8B",
            button_color="#FFFFFF",
            button_hover_color="#dbdbdb",
            variable=ctk.IntVar(value=1),
            command=self.controller.on_volume_clicked,
        )
        self.volume_slider.grid(column=2, row=0, padx=5)

        # more options button
        ctk.CTkButton(
            volume_controls_frame,
            text="",
            fg_color="transparent",
            width=0,
            height=0,
            hover_color="#000010",
            image=ctk.CTkImage(
                Image.open(resource_path("assets\icons\more_vert.png")),
                size=(24, 24),
            ),
            command=self.show_track_actions_frame,
        ).grid(column=4, row=0, padx=(5, 0))

        # ==» Library Controls Frame «==---------------------------
        library_controls_frame = ctk.CTkFrame(self, width=200, fg_color="#030303")
        library_controls_frame.grid(column=0, row=0, rowspan=2, sticky="nsew")
        library_controls_frame.grid_columnconfigure(0, weight=1)
        library_controls_frame.grid_rowconfigure(([i for i in range(6)]), weight=0)
        library_controls_frame.grid_rowconfigure(6, weight=1)

        # --==» Search Frame «==--
        search_frame = ctk.CTkFrame(
            library_controls_frame,
            height=30,
            fg_color="#030303",
        )
        search_frame.grid(column=0, row=0)
        search_frame.grid_columnconfigure(0, weight=1)
        search_frame.grid_columnconfigure(1, weight=0)
        search_frame.rowconfigure(0, weight=1)
    
        self.search_entry = ctk.CTkEntry(
            search_frame,
            height=30,
            corner_radius=25,
            border_width=1,
            border_color="#151515",
            placeholder_text="Search Music",
            width=170,
            fg_color="#070707",
            justify="center",
            font=ctk.CTkFont(size=12),
        )
        self.search_entry.grid(column=0, row=0, pady=10)
        self.search_entry.bind("<KeyRelease>", self.on_text_change)

        # add track button
        ctk.CTkButton(
            search_frame,
            fg_color="#030303",
            width=10,
            height=10,
            hover_color="#080808",
            text="",
            image=ctk.CTkImage(
                Image.open(resource_path("assets/icons/library_add.png")),
                size=(24, 24),
            ),
            command=self.on_select_tracks,
        ).grid(column=1, row=0)

        # --==» Library Controls Frame «==--
        # library title lable
        ctk.CTkLabel(
            library_controls_frame,
            text="Library ",
            image=ctk.CTkImage(
                Image.open(resource_path("assets/icons/library_music_.png")),
                size=(15, 15),
            ),
            anchor="w",
            text_color="#dbdbdb",
            compound="right",
            font=ctk.CTkFont(size=15),
        ).grid(column=0, row=1, sticky="w", padx=15)

        self.show_all_tracks_btn = ctk.CTkButton(
            library_controls_frame,
            text="All Song",
            text_color="#dbdbdb",
            hover_color="#080808",
            image=ctk.CTkImage(
                Image.open(resource_path("assets/icons/music_note_2.png")),
                size=(20, 22),
            ),
            width=220,
            corner_radius=5,
            fg_color="#030303",
            anchor="w",
            font=ctk.CTkFont(size=20),
            command=self.controller.on_show_all_tracks_clicked,
        )
        self.show_all_tracks_btn.grid(column=0, row=2, pady=10, padx=5, sticky="w")

        self.show_favorites_btn = ctk.CTkButton(
            library_controls_frame,
            text="Favorites",
            text_color="#dbdbdb",
            hover_color="#080808",
            width=220,
            image=ctk.CTkImage(
                Image.open(resource_path("assets/icons/favorite_.png")),
                size=(20, 22),
            ),
            corner_radius=5,
            fg_color="#030303",
            font=ctk.CTkFont(size=20),
            anchor="w",
            command=self.controller.on_show_favorites_tracks_clicked,
        )
        self.show_favorites_btn.grid(column=0, row=3, padx=5, sticky="w")
        
        self.show_last_played = ctk.CTkButton(
            library_controls_frame,
            text="Recently Played",
            text_color="#dbdbdb",
            hover_color="#080808",
            width=220,
            image=ctk.CTkImage(
                Image.open(resource_path("assets/icons/schedule.png")),
                size=(20, 20),
            ),
            corner_radius=5,
            fg_color="#030303",
            font=ctk.CTkFont(size=20),
            anchor="w",
            command=self.controller.on_show_last_played_clicked,
        )
        self.show_last_played.grid(column=0, row=4, pady=10, padx=5, sticky="w")
        
        self.show_playlists_btn = ctk.CTkButton(
            library_controls_frame,
            text="Playlists",
            text_color="#dbdbdb",
            hover_color="#080808",
            width=220,
            image=ctk.CTkImage(
                Image.open(resource_path("assets/icons/queue_music.png")),
                size=(20, 22),
            ),
            corner_radius=5,
            fg_color="#030303",
            anchor="w",
            font=ctk.CTkFont(size=20),
            command=self.show_playlists_frame,
        )
        self.show_playlists_btn.grid(column=0, row=5, padx=5, sticky="w")

        self.main_listbox = CTkListbox(
            library_controls_frame,
            width=200,
            height=400,
            border_width=0,
            fg_color="#030303",
            hover_color="#080808",
            bg_color="black",
            button_color="#050505",
            highlight_color="#101010",
            command=self.on_track_selected,
        )
        self.main_listbox.grid(column=0, row=6, pady=10)
        self.main_listbox._scrollbar.configure(
            button_color="#080808", button_hover_color="#121212"
        )

        # --==» status progressbar frame «==--
        self.status_frame = ctk.CTkFrame(
            library_controls_frame,
            width=225,
            height=410,
            border_width=0,
            fg_color="#030303",
            bg_color="black",
        )
        self.status_frame.pack_propagate(False)

        self.status_label = ctk.CTkLabel(self.status_frame, text="")
        self.status_progressbar = ctk.CTkProgressBar(
            self.status_frame,
            height=3,
            width=180,
            fg_color="#151515",
            progress_color="#404040",
        )

        self.status_label.pack(pady=(20, 0))
        self.status_progressbar.pack(padx=20)

        # --==» Playlist Management Frame «==--
        self.playlist_management_frame = ctk.CTkFrame(
            library_controls_frame,
            width=225,
            height=410,
            border_width=0,
            fg_color="#030303",
            bg_color="black",
        )
        self.playlist_management_frame.pack_propagate(False)

        self.created_playlist_btn = ctk.CTkButton(
            self.playlist_management_frame,
            150,
            fg_color="#050505",
            hover_color="#030303",
            border_width=1,
            border_color="#101010",
            corner_radius=15,
            text="+ created",
            command=self.show_created_playlist_frame,
        )
        self.created_playlist_btn.pack(pady=10)

        self.listbox_list_playlist = CTkListbox(
            self.playlist_management_frame,
            height=310,
            width=200,
            fg_color="#030303",
            hover_color="#080808",
            bg_color="black",
            button_color="#050505",
            highlight_color="#101010",
            border_width=0,
        )
        self.listbox_list_playlist.pack()
        self.listbox_list_playlist._scrollbar.configure(
            button_color="#030303", button_hover_color="#080808"
        )

        # » playlist controls button frame «
        self.playlist_controls_btn_frame = ctk.CTkFrame(self.playlist_management_frame, width=200, height=50, fg_color="transparent")
        self.playlist_controls_btn_frame.pack()
        self.playlist_controls_btn_frame.pack_propagate(False)
        
        self.closed_window_btn = ctk.CTkButton(
            self.playlist_controls_btn_frame,
            fg_color="#070707",
            width=10,
            height=10,
            hover_color="#121212",
            text="",
            image=ctk.CTkImage(
                Image.open(resource_path("assets/icons/close.png")),
                size=(24, 24),
            ),
            command=self.hide_playlists_frame,
        )
        self.closed_window_btn.pack(side="left", padx=(2, 15))
        
        self.deleted_playlist_btn = ctk.CTkButton(
            self.playlist_controls_btn_frame,
            fg_color="#070707",
            width=10,
            height=10,
            hover_color="#121212",
            text="",
            image=ctk.CTkImage(
                Image.open(resource_path("assets/icons/playlist_remove.png")),
                size=(24, 24),
            ),
            command=self.controller.on_delete_playlist_clicked,
        )
        self.deleted_playlist_btn.pack(side="left", padx=(0, 15))
        
        self.rename_playlist_btn = ctk.CTkButton(
            self.playlist_controls_btn_frame,
            fg_color="#070707",
            width=10,
            height=10,
            hover_color="#121212",
            text="",
            image=ctk.CTkImage(
                Image.open(resource_path("assets/icons/edit_note.png")),
                size=(24, 24),
            ),
            command=self.show_rename_frame,
        )
        self.rename_playlist_btn.pack(side="left", padx=(0, 15))
        
        self.run_playlist_btn = ctk.CTkButton(
            self.playlist_controls_btn_frame,
            fg_color="#070707",
            width=10,
            height=10,
            hover_color="#121212",
            text="",
            image=ctk.CTkImage(
                Image.open(resource_path("assets/icons/playlist_play.png")),
                size=(24, 24),
            ),
            command=self.on_show_tracks_clicked,
        )
        self.run_playlist_btn.pack(side="left", padx=(0, 2))

        # » rename playlist frame «
        self.rename_playlist_frame = ctk.CTkFrame(self.playlist_management_frame, fg_color="transparent")

        self.rename_entry = ctk.CTkEntry(
            self.rename_playlist_frame, 
            fg_color="#050505",
            border_width=1,
            border_color="#101010",
            placeholder_text="Entry New Name",
        )
        self.rename_entry.pack(side="left")

        self.rename_btn = ctk.CTkButton(
            self.rename_playlist_frame,
            fg_color="#030303",
            width=10,
            height=10,
            hover_color="#080808",
            text="",
            image=ctk.CTkImage(
                Image.open(resource_path("assets/icons/check.png")),
                size=(10, 15),
            ),
            command=self.on_rename_playlist_clicked,
        )
        self.rename_btn.pack(side="left")
        
        self.close_frame_btn = ctk.CTkButton(
            self.rename_playlist_frame,
            fg_color="#030303",
            width=10,
            height=10,
            hover_color="#080808",
            text="",
            image=ctk.CTkImage(
                Image.open(resource_path("assets/icons/close.png")),
                size=(10, 15),
            ),
            command=self.hide_rename_frame,
        )
        self.close_frame_btn.pack(side="left")
    
        # --==» create playlist Frame «==--
        self.create_playlist_frame = ctk.CTkFrame(
            library_controls_frame,
            width=225,
            height=410,
            border_width=0,
            fg_color="#030303",
            bg_color="black",
        )

        self.playlist_name_entry = ctk.CTkEntry(
            self.create_playlist_frame,
            170,
            corner_radius=15,
            placeholder_text="playlist name :",
            justify="center",
            border_width=1,
            border_color="#101010",
            fg_color="#030303",
        )
        self.playlist_name_entry.pack(pady=10)

        self.listbox_list_track = CTkListbox(
            self.create_playlist_frame,
            315,
            200,
            border_width=0,
            fg_color="#030303",
            hover_color="#080808",
            bg_color="black",
            button_color="#050505",
            highlight_color="#101010",
            multiple_selection=True,
        )
        self.listbox_list_track.pack()
        self.listbox_list_track._scrollbar.configure(
            button_color="#030303", button_hover_color="#080808"
        )

        self.create_playlist_btn = ctk.CTkButton(
            self.create_playlist_frame,
            220,
            fg_color="#070707",
            hover_color="#121212",
            border_width=0,
            corner_radius=0,
            text="created",
            command=self.on_created_playlist_clicked,
        )
        self.create_playlist_btn.pack(pady=(5, 0))

        # --==» track actions Frame «==--
        self.track_actions_frame = ctk.CTkFrame(
            self,
            width=150,
            height=100,
            border_width=0,
            fg_color="#000009",
            bg_color="black",
        )
        self.track_actions_frame.pack_propagate(False)

        self.add_to_playlist_btn = ctk.CTkButton(
            self.track_actions_frame,
            height=25,
            fg_color="#000009",
            corner_radius=0,
            hover_color="#000003",
            text="Add to Playlist",
            image=ctk.CTkImage(
                Image.open("assets/icons/playlist_add.png"), size=(24, 24)
            ),
            font=ctk.CTkFont(size=13),
            command=self.show_add_to_playlist_frame,
            anchor="w",
        )

        self.remove_track_btn = ctk.CTkButton(
            self.track_actions_frame,
            height=25,
            fg_color="#000009",
            corner_radius=0,
            hover_color="#000003",
            image=ctk.CTkImage(Image.open("assets/icons/remove.png"), size=(20, 20)),
            text="Removed Track",
            font=ctk.CTkFont(size=13),
            command=self.on_remove_track_clicked,
            anchor="w",
        )
        
        self.remove_track_btn.pack(side="bottom", pady=5)
        self.add_to_playlist_btn.pack(side="bottom")

        # » add to playlist Frame «
        self.add_to_playlist_frame = ctk.CTkFrame(
            self,
            width=150,
            height=100,
            border_width=0,
            fg_color="#000009",
            bg_color="black",
        )
        self.add_to_playlist_frame.pack_propagate(False)

        self.list_playlist = CTkListbox(
            self.add_to_playlist_frame,
            105,
            190,
            border_width=0,
            command=self.controller.on_add_to_playlist_clicked,
        )
        self.list_playlist.pack()

        # » empty playlist Frame «
        self.empty_playlist_frame = ctk.CTkFrame(
            self,
            border_width=0,
            fg_color="#000009",
        )

        self.empty_playlist_label = ctk.CTkLabel(
            self.empty_playlist_frame,
            text="""
                No playlists found.

                To create a new playlist,
                go to the Playlists section.
            """,
        )
        self.empty_playlist_label.pack()

    # ==» UI Update Methods «==---------------------------
    def update_track_title(self, name):
        self.track_title_label.configure(text=name)

    def update_toggle_favorite_btn(self, select: bool):
        self.toggle_favorite_btn.configure(
            image=self.favorite_icon_select if select else self.favorite_icon_deselect
        )

    def update_pause_unpause_btn(self, playing: bool):
        self.pause_unpause_btn.configure(
            image=self.unpause_icon if playing else self.pause_icon
        )

    def update_slider_to(self, intger):
        self.time_slider.configure(to=intger)

    def update_lab_current(self, new_text):
        self.current_position_lable.configure(text=new_text)

    def update_lab_time_len(self, new_text):
        self.track_length_lable.configure(text=new_text)

    def reset_ui(self):
        self.update_track_title("Music Name")
        self.set_artwork(self.default_artwork_path)
        self.update_pause_unpause_btn(False)
        self.update_lab_current("00:00")
        self.update_lab_time_len("00:00")
        self.controller.seek_offset = 0
        self.time_slider_position_var.set(0)
        self.update_toggle_favorite_btn(False)

    # ==» Search Methods «==---------------------------
    def on_text_change(self, event):
        text = self.search_entry.get()

        if len(text) >= 3:
            self.controller.search_tracks(text)

    def reset_search_entry(self):
    
        if self.search_entry.get():
            self.search_entry.delete(0, "end")
            self.search_entry.focus()
            self.focus()
        elif self.search_entry.get() is not None:
            self.focus()

    # ==» Playlist Helpers «==---------------------------
    def on_track_selected(self, file_name):
        self.controller.track_selected()
    
    def main_listbox_del(self):
        self.main_listbox.delete(0, "end")

    def main_listbox_insert(self, tracks_title):
        for title in tracks_title:
            self.main_listbox.insert("end", title)

    def main_listbox_on_track_insert(self, title):
        self.main_listbox.insert("end", title)

    def on_select_tracks(self):

        paths = askopenfilenames(
            title="Import Music Files", filetypes=[("MP3 Files", "*.mp3")]
        )
        
        if paths:
            self.controller.add_tracks_to_library(paths)

    def get_selected_index_main_listbox(self):
        return self.main_listbox.curselection()

    def select_main_listbox(self, idx):

        if idx is None:
            return

        if 0 <= idx < self.main_listbox.size():
            self.main_listbox.activate(idx)
    
    def unselect_main_listbox(self, idx):
        self.main_listbox.deactivate(idx)

    # --==» Playlist Management Frame Methods «==--
    def refresh_listbox_playlists_frame(self, list_playlists):
            self.listbox_list_playlist.delete(0, "end")
            self.listbox_insert(list_playlists)

    def listbox_insert(self, playlists):
        for playlist in playlists:
            self.listbox_list_playlist.insert("end", playlist)

    def get_playlist_selected_index(self):
        return self.listbox_list_playlist.curselection()

    def on_show_tracks_clicked(self):
        self.hide_rename_frame()
        index = self.get_playlist_selected_index()
        if index is not None:
            self.controller.on_playlist_selected(index)
            self.playlist_management_frame.place_forget()
        else:
            self.playlist_management_frame.place_forget()

    def on_rename_playlist_clicked(self):
        self.controller.rename_playlist(self.rename_entry.get())
        self.hide_rename_frame()
    
    def reset_rename_playlist_frame(self):
        if self.rename_entry.get():
            self.rename_entry.delete(0, "end")
            self.rename_entry.focus()
            self.rename_playlist_frame.focus()
        elif self.rename_entry.get() is not None:
            self.rename_playlist_frame.focus()
    
    def show_rename_frame(self):
        if self.get_playlist_selected_index() is not None:
            self.reset_rename_playlist_frame()
            self.rename_playlist_frame.place(x=20, y=330)
    
    def hide_rename_frame(self):
        self.rename_playlist_frame.place_forget()

    def show_playlists_frame(self):
        self.playlist_management_frame.place(y=247)
        self.refresh_listbox_playlists_frame(self.controller.get_playlist_name())
    
    def hide_playlists_frame(self):
        self.hide_rename_frame()
        self.playlist_management_frame.place_forget()
    
    # » create playlist Frame Methods «
    def get_name_playlist(self):
        return self.playlist_name_entry.get()

    def refresh_listbox_list_track(self, tracks):
        if tracks is None:
            return
        
        self.show_loading()
        self.listbox_list_track.delete(0, "end")
        self.insert_to_listbox_list_track(tracks)
        self.hide_status()

    def insert_to_listbox_list_track(self, tracks):
        for track in tracks:
            self.listbox_list_track.insert("end", track)

    def get_tracks_selected_index(self):
        tracks_selected_index = self.listbox_list_track.curselection()
        if tracks_selected_index is not None:
            return tracks_selected_index

    def reset_playlist_name_entry(self):
        if self.playlist_name_entry.get():
            self.playlist_name_entry.delete(0, "end")
            self.playlist_name_entry.focus()
            self.create_playlist_frame.focus()
        elif self.search_entry.get() is not None:
            self.create_playlist_frame.focus()
    
    def on_created_playlist_clicked(self):
        if self.get_name_playlist():
            self.controller.create_playlist_with_tracks(
                self.get_name_playlist(),
                self.get_tracks_selected_index(),
            )
            self.hide_created_playlist_frame()
        else:
            self.hide_created_playlist_frame()
    
    def show_created_playlist_frame(self):
        self.reset_playlist_name_entry()
        self.create_playlist_frame.place(y=247)
        self.refresh_listbox_list_track(self.controller.get_all_track_title())
    
    def hide_created_playlist_frame(self):
        self.create_playlist_frame.place_forget()
        
    # --==» track actions Frame Methods«==--
    def on_remove_track_clicked(self):
        self.controller.remove_track()
        self.hide_track_actions_frame()
    
    def show_track_actions_frame(self):
        self.track_actions_frame.place(x=1110, y=510)
        
    def hide_track_actions_frame(self):
        self.track_actions_frame.place_forget()
    
    # » add to playlist Frame «
    def refresh_listbox_list_playlist(self, list_playlist):
        self.list_playlist.delete(0, "end")
        self.listbox_playlist_insert(list_playlist)

    def listbox_playlist_insert(self, playlists):
        for playlist in playlists:
            self.list_playlist.insert("end", playlist)

    def get_index_listbox(self):
        return self.list_playlist.curselection()

    def hide_empty_playlist_frame(self):
        self.empty_playlist_frame.place_forget()
        self.track_actions_frame.place_forget()

    def _hide_destry(self):
        self.track_actions_frame.after(5000, self.hide_empty_playlist_frame)

    def show_add_to_playlist_frame(self):
        if self.controller.all_playlists_info:
            self.add_to_playlist_frame.place(x=1110, y=510)
            self.refresh_listbox_list_playlist(self.controller.get_playlist_name())
        else:
            self.empty_playlist_frame.place(x=1065, y=515)
            self._hide_destry()

    def hide_add_to_playlist_frame(self):
        self.add_to_playlist_frame.place_forget()

    # ==» Shared UI Helpers «==-----------------------------
    def _load_image(self, obj):
            if not obj:
                return None
            try:
                if isinstance(obj, str):
                    if not os.path.exists(obj):
                        return None
                    img = Image.open(obj)
                else:  # bytes
                    img = Image.open(BytesIO(obj))
                return img.convert("RGB")
            except Exception:
                return None
    
    def _apply_dark_mask(self, img, size, blur_radius, bottom_cut):
            """اعمال ماسک تاریک و محو روی عکس کوچک شده"""
            w, h = size
            # ایجاد ماسک گرادینت ساده برای پایین تصویر
            mask = Image.new("L", size, 0)
            draw = ImageDraw.Draw(mask)
            # مستطیل سفید در بالا
            draw.rectangle((20, 20, w - 20, h - bottom_cut), fill=255)
            mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))

            dark_layer = Image.new("RGB", size, "#000009")
            return Image.composite(img, dark_layer, mask)
    
    def _prepare_artwork_images(self, artwork):

        original_img = self._load_image(artwork)
        if not original_img:
            return None

        try:
            # --- Foreground (art_label: 580x550) ---
            # ابتدا Resize می‌کنیم (بسیار سریع‌تر از بلور کردن عکس بزرگ)
            img_art = original_img.resize((580, 550), Image.Resampling.LANCZOS)

            # اعمال افکت روی نسخه کوچک
            result_art = self._apply_dark_mask(
                img_art, (580, 550), blur_radius=30, bottom_cut=100
            )

            art_ctk = ctk.CTkImage(result_art, size=(580, 550))


            # --- Background (1045x500) ---
            # Resize سریع
            bg = original_img.resize((1045, 500), Image.Resampling.LANCZOS)

            # افکت‌های بک‌گراند
            bg = bg.filter(ImageFilter.GaussianBlur(5))
            bg = ImageEnhance.Brightness(bg).enhance(0.90)

            # اعمال ماسک روی نسخه کوچک
            result_bg = self._apply_dark_mask(
                bg, (1045, 500), blur_radius=50, bottom_cut=100
            )

            bg_ctk = ctk.CTkImage(result_bg, size=(1045, 500))

            return art_ctk, bg_ctk
        
        except Exception as e:
            print(f"Error processing image: {e}")
            self.set_artwork(self.default_artwork_path)
        
    def set_artwork(self, artwork):

        if not artwork:
            artwork = self.default_artwork_path

        processed = self._prepare_artwork_images(artwork)

        if not processed:
            return
        
        art_ctk, bg_ctk = processed

        self.art_label.configure(image=art_ctk)
        self.art_label.image = art_ctk

        self.background.configure(image=bg_ctk)
        self.background.image = bg_ctk
    
    # ==» progressbar Methods «==--
    def show_loading(self):
        self.status_frame.place(y=247)
        self.status_frame.lift()
        self.status_label.configure(text="Loading...")
        self.status_progressbar.configure(mode="indeterminate")
        self.status_progressbar.start()

    def show_progress(self):
        self.status_frame.place(y=247)
        self.status_label.configure(text="Importing tracks...")
        self.status_progressbar.configure(mode="determinate")
        self.status_progressbar.set(0)
    
    def update_progress(self, value):
        self.status_progressbar.set(value)

    def hide_status(self):
        self.status_progressbar.stop()
        self.status_frame.place_forget()
