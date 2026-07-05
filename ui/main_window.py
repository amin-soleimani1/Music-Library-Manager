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
        ctk.set_appearance_mode("Dark")
        self.title("Music Player")
        self.geometry("1266x668+40+30")
        self.resizable(False, False)

        # Core UI dependencies
        self.controller = controller

        # Total duration of the current track (seconds)
        self.track_length_var = ctk.IntVar(value=0)

        # Variable bound to the playback time slider
        self.time_slider_position_var = ctk.IntVar(value=0)

        self.repeat_mode = True

        # progressbar state
        self.status_state = True
        
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
        self.artwork_frame = ctk.CTkFrame(
            self,
            fg_color="#000009",
        )
        self.artwork_frame.grid(column=1, row=0, sticky="nsew")

        # Background lable
        self.background = ctk.CTkLabel(self.artwork_frame, text="")
        self.background.place(x=0, y=0)

        # artwork lable
        self.art_label = ctk.CTkLabel(self.artwork_frame, text="")
        self.art_label.pack()

        # track title lable
        self.track_title_label = ctk.CTkLabel(
            self.artwork_frame,
            0,
            0,
            text="",
            font=ctk.CTkFont(size=35, weight="bold"),
        )
        self.track_title_label.pack()

        # artist name lable
        self.artist_name = ctk.CTkLabel(
            self.artwork_frame,
            0,
            0,
            text="",
            font=ctk.CTkFont(size=13),
        )
        self.artist_name.pack(pady=(0, 15))

        self.default_artwork_path = str(resource_path("assets/images/artwork.png"))

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
            Image.open(resource_path("assets/icons/play.png")),
            size=(40, 40),
        )
        self.pause_icon = ctk.CTkImage(
            Image.open(resource_path("assets/icons/pause.png")),
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
            size=(15, 15),
        ),
            bg_color="#000005",
            border_width=0,
            hover_color="#000010",
            command=self.controller.on_stop_clicked,
        ).grid(column=0, row=0, padx=(10, 5))

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

        self.repeate_one_icon = ctk.CTkImage(
                Image.open(resource_path("assets/icons/repeat_one.png")),
                size=(19, 19),
            )
        
        self.repeate_all_icon = ctk.CTkImage(
                Image.open(resource_path("assets/icons/repeat_all.png")),
                size=(19, 19),
            )
        
        
        self.repeat_mode_btn = ctk.CTkButton(
            playback_buttons_frame,
            text="",
            width=0,
            height=0,
            fg_color="#000003",
            bg_color="#000003",
            image=self.repeate_one_icon,
            border_width=0,
            hover_color="#000010",
            command=self.on_repeat_mode_clicked,
        )
        self.repeat_mode_btn.grid(column=4, row=0, padx=(7, 10))

        # playback separator label
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

        # volume controls separator_label
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
        ).grid(column=1, row=0, padx=(10, 0))
        
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
        self.toggle_favorite_btn.grid(column=3, row=0, padx=(17, 5))

        self.volume_slider = ctk.CTkSlider(
            volume_controls_frame,
            fg_color="#151515",
            width=100,
            height=10,
            progress_color="#0D3F8B",
            button_color="#FFFFFF",
            button_hover_color="#dbdbdb",
            variable=ctk.IntVar(value=1),
            command=self.controller.on_volume_clicked,
        )
        self.volume_slider.grid(column=2, row=0, padx=(0, 5))

        # more options button
        ctk.CTkButton(
            volume_controls_frame,
            text="",
            fg_color="transparent",
            width=0,
            height=0,
            hover_color="#000010",
            image=ctk.CTkImage(
                Image.open(resource_path("assets/icons/more_vert.png")),
                size=(24, 24),
            ),
            command=self.show_track_actions_frame,
        ).grid(column=4, row=0, padx=(5, 0))

        self.hint_lable = ctk.CTkLabel(self, text="Please select a track first.", font=ctk.CTkFont(size=18), fg_color="#000009")

        # ==» Library Controls Frame «==---------------------------
        self.library_controls_frame = ctk.CTkFrame(self, width=200, fg_color="#030303")
        self.library_controls_frame.grid(column=0, row=0, rowspan=2, sticky="nsew")
        self.library_controls_frame.grid_columnconfigure(0, weight=1)
        self.library_controls_frame.grid_rowconfigure(([i for i in range(6)]), weight=0)
        self.library_controls_frame.grid_rowconfigure(6, weight=1)

        # --==» Search Frame «==--
        search_frame = ctk.CTkFrame(
            self.library_controls_frame,
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

        # search icon
        ctk.CTkLabel(
            search_frame,
            22,
            22,
            text="",
            image=ctk.CTkImage(
                Image.open(resource_path("assets/icons/search.png")),
                size=(22, 22)
                ),
            fg_color="#070707",
            ).place(x=8, y=15)

        # add track button
        self.add_track_btn = ctk.CTkButton(
            search_frame,
            fg_color="#030303",
            width=10,
            height=10,
            hover_color="#080808",
            text="",
            corner_radius=25,
            image=ctk.CTkImage(
                Image.open(resource_path("assets/icons/library_add.png")),
                size=(24, 24),
            ),
            command=self.on_select_tracks,
        )
        self.add_track_btn.grid(column=1, row=0)

        # --==» Library Controls Frame «==--
        # library title lable
        ctk.CTkLabel(
            self.library_controls_frame,
            text="Library ",
            anchor="w",
            text_color="#FFFFFF",
            font=ctk.CTkFont(size=25, weight="bold"),
        ).grid(column=0, row=1, sticky="w", padx=15, pady=(0, 10))

        self.show_all_tracks_btn = ctk.CTkButton(
            self.library_controls_frame,
            text="All Tracks",
            text_color="#dbdbdb",
            hover_color="#080808",
            image=ctk.CTkImage(
                Image.open(resource_path("assets/icons/music_note_2.png")),
                size=(18, 18),
            ),
            width=220,
            corner_radius=5,
            fg_color="#030303",
            anchor="w",
            font=ctk.CTkFont(size=17),
            command=self.controller.on_show_all_tracks_clicked,
        )
        self.show_all_tracks_btn.grid(column=0, row=2, pady=10, padx=5, sticky="w")

        self.show_favorites_btn = ctk.CTkButton(
            self.library_controls_frame,
            text="Favorites",
            text_color="#dbdbdb",
            hover_color="#080808",
            width=220,
            image=ctk.CTkImage(
                Image.open(resource_path("assets/icons/favorite_.png")),
                size=(18, 18),
            ),
            corner_radius=5,
            fg_color="#030303",
            font=ctk.CTkFont(size=17),
            anchor="w",
            command=self.controller.on_show_favorites_tracks_clicked,
        )
        self.show_favorites_btn.grid(column=0, row=3, padx=5, sticky="w")
        
        self.show_last_played = ctk.CTkButton(
            self.library_controls_frame,
            text="Recently Played",
            text_color="#dbdbdb",
            hover_color="#080808",
            width=220,
            image=ctk.CTkImage(
                Image.open(resource_path("assets/icons/schedule.png")),
                size=(18, 18),
            ),
            corner_radius=5,
            fg_color="#030303",
            font=ctk.CTkFont(size=17),
            anchor="w",
            command=self.controller.on_show_last_played_clicked,
        )
        self.show_last_played.grid(column=0, row=4, pady=10, padx=5, sticky="w")
        
        self.show_playlists_btn = ctk.CTkButton(
            self.library_controls_frame,
            text="Playlists",
            text_color="#dbdbdb",
            hover_color="#080808",
            width=220,
            image=ctk.CTkImage(
                Image.open(resource_path("assets/icons/queue_music.png")),
                size=(18, 20),
            ),
            corner_radius=5,
            fg_color="#030303",
            anchor="w",
            font=ctk.CTkFont(size=17),
            command=self.show_playlists_frame,
        )
        self.show_playlists_btn.grid(column=0, row=5, padx=5, sticky="w")

        ctk.CTkLabel(
            self.library_controls_frame,
            text="Tracks ",
            anchor="w",
            text_color="#FFFFFF",
            font=ctk.CTkFont(size=15, weight="bold"),
            image=ctk.CTkImage(
                Image.open(resource_path("assets/icons/chevron-down.png")),
                size=(15, 15),
            ),
            compound="right",
        ).place(x=14, y=266)
        
        self.main_listbox = CTkListbox(
            self.library_controls_frame,
            width=200,
            height=400,
            border_width=0,
            fg_color="#030303",
            hover_color="#040A29",
            bg_color="black",
            text_color="#dddddd",
            font =ctk.CTkFont(size=13),
            button_color="#040404",
            highlight_color="#0D3F8B",
            command=self.on_track_selected,
        )
        self.main_listbox.grid(column=0, row=6, pady=(50, 10))
        self.main_listbox._scrollbar.configure(
            button_color="#080808", button_hover_color="#121212"
        )

        # --==» status progressbar frame «==--
        self.status_frame = ctk.CTkFrame(
            self.library_controls_frame,
            width=235,
            height=420,
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
            self.library_controls_frame,
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
            fg_color="#0D3F8B",
            hover_color="#0D1F8B",
            border_width=1,
            border_color="#101010",
            corner_radius=15,
            text="created",
            command=self.creat_created_playlist_frame,
        )
        self.created_playlist_btn.pack(pady=10)

        self.listbox_list_playlist = CTkListbox(
            self.playlist_management_frame,
            height=310,
            width=250,
            fg_color="#030303",
            hover_color="#121212",
            bg_color="black",
            font =ctk.CTkFont(size=14),
            button_color="#080808",
            highlight_color="#151515",
            border_width=0,
        )
        self.listbox_list_playlist.pack()
        self.listbox_list_playlist._scrollbar.configure(
            button_color="#080808", button_hover_color="#121212"
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
            hover_color="#8B0D0D",
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
            hover_color="#151515",
            text="",
            image=ctk.CTkImage(
                Image.open(resource_path("assets/icons/playlist_remove.png")),
                size=(24, 24),
            ),
            
            command=self.show_playlist_deleted_frame,
        )
        self.deleted_playlist_btn.pack(side="left", padx=(0, 15))
        
        self.rename_playlist_btn = ctk.CTkButton(
            self.playlist_controls_btn_frame,
            fg_color="#070707",
            width=10,
            height=10,
            hover_color="#151515",
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
            hover_color="#151515",
            text="",
            image=ctk.CTkImage(
                Image.open(resource_path("assets/icons/playlist_play.png")),
                size=(24, 24),
            ),
            command=self.on_show_tracks_clicked,
        )
        self.run_playlist_btn.pack(side="left", padx=(0, 2))

        # » playlist_alert «
        self.playlist_alert_message = ctk.CTkLabel(self.playlist_management_frame, text="Please select a playlist !")
        
        # » playlist_deleted_alert_frame «
        self.playlist_deleted_frame = ctk.CTkFrame(self.playlist_management_frame, fg_color="transparent")
        self.playlist_deleted_frame.grid_columnconfigure((0, 1), weight=1)
        self.playlist_deleted_frame.grid_rowconfigure((0, 1), weight=1)
        # deleted_playlist_alert_message
        ctk.CTkLabel(
            self.playlist_deleted_frame,
            text="Delete this playlist ?",
            ).grid(column=0, row=0, columnspan=2)

        # deleted_playlist_btn
        ctk.CTkButton(
            self.playlist_deleted_frame,
            fg_color="#EE0000",
            width=60,
            height=10,
            hover_color="#9E0000",
            text="yes",
            command=self.controller.on_delete_playlist_clicked,
        ).grid(column=0, row=1, padx=(15, 10))
        
        # cancle_deleted_playlist_btn
        ctk.CTkButton(
            self.playlist_deleted_frame,
            fg_color="#080808",
            width=60,
            height=10,
            hover_color="#121212",
            text="cancel",
            command=self.hide_playlist_deleted_frame,
        ).grid(column=1, row=1, padx=(0, 10))
        
        # » rename playlist frame «
        self.rename_playlist_frame = ctk.CTkFrame(self.playlist_management_frame, fg_color="transparent")
        self.rename_playlist_frame.grid_columnconfigure((0, 1), weight=1)
        self.rename_playlist_frame.grid_rowconfigure((0, 1), weight=1)

        self.rename_entry = ctk.CTkEntry(
            self.rename_playlist_frame, 
            fg_color="#050505",
            border_width=1,
            border_color="#101010",
            placeholder_text="Entry New Name",
        )
        self.rename_entry.grid(column=0, row=0, columnspan=2, pady=5)

        # rename_btn
        ctk.CTkButton(
            self.rename_playlist_frame,
            fg_color="#080808",
            width=60,
            height=10,
            hover_color="#121212",
            text="",
            image=ctk.CTkImage(
                Image.open(resource_path("assets/icons/check.png")),
                size=(10, 15),
            ),
            command=self.on_rename_playlist_clicked,
        ).grid(column=0, row=1)
        
        # cancle_rename_btn
        ctk.CTkButton(
            self.rename_playlist_frame,
            fg_color="#080808",
            width=60,
            height=10,
            hover_color="#121212",
            text="",
            image=ctk.CTkImage(
                Image.open(resource_path("assets/icons/close.png")),
                size=(10, 15),
            ),
            command=self.hide_rename_frame,
        ).grid(column=1, row=1)
    
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
            corner_radius=5,
            hover_color="#000015",
            text="Add to Playlist",
            image=ctk.CTkImage(
                Image.open(resource_path("assets/icons/playlist_add.png")), size=(24, 24)
            ),
            font=ctk.CTkFont(size=13),
            command=self.show_add_to_playlist_frame,
            anchor="w",
        )

        self.remove_track_btn = ctk.CTkButton(
            self.track_actions_frame,
            height=25,
            fg_color="#000009",
            corner_radius=5,
            hover_color="#000015",
            image=ctk.CTkImage(Image.open(resource_path("assets/icons/remove.png")), size=(20, 20)),
            text="Removed Track",
            font=ctk.CTkFont(size=13),
            command=self.show_remove_track_frame,
            anchor="w",
        )
        
        # » track_deleted_alert_frame «
        self.track_deleted_frame = ctk.CTkFrame(self, 100, 100, fg_color="#000009")
        self.track_deleted_frame.grid_columnconfigure((0, 1), weight=1)
        self.track_deleted_frame.grid_rowconfigure((0, 1), weight=1)
        self.playlist_controls_btn_frame.grid_propagate(False)
        
        # deleted_playlist_alert_message
        ctk.CTkLabel(
            self.track_deleted_frame,
            text="Delete this track ?",
            font=ctk.CTkFont(size=15)
            ).grid(column=0, row=0, columnspan=2, padx=5, pady=(30, 0))

        # deleted_track_btn
        ctk.CTkButton(
            self.track_deleted_frame,
            fg_color="#EE0000",
            width=70,
            height=20,
            hover_color="#9E0000",
            text="yes",
            command=self.on_remove_track_clicked,
        ).grid(column=0, row=1, padx=(10, 5), pady=10)
        
        # cancle_deleted_track_btn
        ctk.CTkButton(
            self.track_deleted_frame,
            fg_color="#080808",
            width=70,
            height=20,
            hover_color="#121212",
            text="cancel",
            command=self.hide_remove_track_frame,
        ).grid(column=1, row=1, padx=(0, 10), pady=10)

        self.closed_track_action_frame_btn = ctk.CTkButton(
            self,
            1,
            1,
            fg_color="#000009",
            corner_radius=5,
            hover_color="#000015",
            text="Cancel",
            image=ctk.CTkImage(
                Image.open(resource_path("assets/icons/close.png")),
                size=(12, 12),
            ),
            anchor="w",
        )
        
        self.remove_track_btn.pack(side="bottom", pady=5)
        self.add_to_playlist_btn.pack(side="bottom")

        # » add to playlist Frame «
        self.add_to_playlist_frame = ctk.CTkFrame(
            self,
            width=150,
            height=95,
            border_width=0,
            fg_color="#000009",
            bg_color="black",
        )
        self.add_to_playlist_frame.pack_propagate(False)

        self.list_playlist = CTkListbox(
            self.add_to_playlist_frame,
            105,
            190,
            fg_color="#000009",
            corner_radius=0,
            hover_color="#000015",
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

        # separator_lables
        self.separator_on_img = ctk.CTkImage(Image.open(resource_path("assets/icons/minus_on.png")), size=(290, 1))

        self.separator_off_img = ctk.CTkImage(Image.open(resource_path("assets/icons/minus_off.png")), size=(290, 1))

        self.separator_all_tracks = ctk.CTkLabel(
            self.library_controls_frame,
            0,
            1,
            text="",
            anchor="w",
            image=self.separator_off_img,
            )
        self.separator_all_tracks.place(x=-35, y=132)
        
        self.separator_favorites = ctk.CTkLabel(
            self.library_controls_frame,
            0,
            1,
            text="",
            anchor="w",
            image=self.separator_off_img,
            )
        self.separator_favorites.place(x=-35, y=171)
        
        self.separator_last_played = ctk.CTkLabel(
            self.library_controls_frame,
            0,
            1,
            text="",
            anchor="w",
            image=self.separator_off_img,
            )
        self.separator_last_played.place(x=-35, y=209)
        
        self.separator_playlists = ctk.CTkLabel(
            self.library_controls_frame,
            0,
            1,
            text="",
            anchor="w",
            image=self.separator_off_img,
            )
        self.separator_playlists.place(x=-35, y=248)
        
        self.separator_tracks_lable = ctk.CTkLabel(
            self.library_controls_frame,
            0,
            1,
            text="",
            anchor="w",
            image=self.separator_on_img,
            )
        self.separator_tracks_lable.place(x=-35, y=295)

        # empty track list lable
        self.empty_track_list_lable = ctk.CTkLabel(
            self.library_controls_frame,
            1,
            1,
            text="""
                Your music list is empty.

                Tap the + button
                in the top-right corner
                to add a track.
            """,
            text_color="#303030",
            font=ctk.CTkFont(size=15),
            )
        
        # empty favorite track list lable
        self.empty_favorite_track_list_lable = ctk.CTkLabel(
            self.library_controls_frame,
            1,
            1,
            text="""
                No favorite tracks yet.

                Tap the ♡ button 
                next to the volume slider 
                to add your favorite tracks.
            """,
            text_color="#303030",
            font=ctk.CTkFont(size=15),
            )

        # empty list playlists lable
        self.empty_list_playlists_lable = ctk.CTkLabel(
            self.playlist_management_frame,
            1,
            1,
            text="""
                No playlists yet.

                Tap the "created" button
                to create your first playlist.
            """,
            text_color="#303030",
            font=ctk.CTkFont(size=15),
            )
        
        self.no_found_lable = ctk.CTkLabel(
            self.library_controls_frame,
            1,
            1,
            text="No track found 🎵",
            text_color="#303030",
            font=ctk.CTkFont(size=15),
            )
        
        self.empty_playlists_run_lable = ctk.CTkLabel(
            self.library_controls_frame,
            1,
            1,
            text="This playlist is currently empty.",
            text_color="#303030",
            
            font=ctk.CTkFont(size=14),
            )
        
    # ==» UI Update Methods «==---------------------------
    def update_track_title(self, title, name):
        self.track_title_label.configure(text=title)
        self.artist_name.configure(text=name)

    def update_toggle_favorite_btn(self, select: bool):
        self.toggle_favorite_btn.configure(
            image=self.favorite_icon_select if select else self.favorite_icon_deselect
        )

    def update_pause_unpause_btn(self, playing: bool):
        self.pause_unpause_btn.configure(
            image=self.unpause_icon if playing else self.pause_icon
        )

    def on_repeat_mode_clicked(self):
        self.repeat_mode = not self.repeat_mode
        state = self.repeat_mode
        self.repeat_mode_btn.configure(
            image=self.repeate_one_icon if state else self.repeate_all_icon
        )
    
    def update_slider_to(self, intger):
        self.time_slider.configure(to=intger)

    def update_lab_current(self, new_text):
        self.current_position_lable.configure(text=new_text)

    def update_lab_time_len(self, new_text):
        self.track_length_lable.configure(text=new_text)

    def reset_ui(self):
        self.update_track_title("", "")
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
        if self.status_state:
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

            if playlist.strip() == "":
                continue

            self.listbox_list_playlist.insert("end", str(playlist))

    def get_playlist_selected_index(self):
        return self.listbox_list_playlist.curselection()

    def on_show_tracks_clicked(self):
        self.hide_rename_frame()
        index = self.get_playlist_selected_index()
        if index is not None:
            self.controller.on_playlist_selected(index)
            self.playlist_management_frame.place_forget()
        else:
            self.playlist_alert()

    def show_playlists_frame(self):
        self.set_separator("playlists")
        self.playlist_management_frame.place(y=247)
        self.refresh_listbox_playlists_frame(self.controller.get_playlist_name())
        self.update_empty_state(self.controller.get_playlist_name(), "playlists")
    
    def hide_playlists_frame(self):
        self.hide_rename_frame()
        self.set_separator(self.controller.separator_state)
        self.playlist_management_frame.place_forget()

    # » Playlist Rename Methods «
    def on_rename_playlist_clicked(self):
        if self.rename_entry.get():
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
            self.rename_playlist_frame.place(x=43, y=300)
        else:
            self.playlist_alert()
    
    def hide_rename_frame(self):
        self.rename_playlist_frame.place_forget()

    # » Playlist Deleted Alert  «
    def show_playlist_deleted_frame(self):
        if self.get_playlist_selected_index() is not None:
            self.hide_rename_frame()
            self.playlist_deleted_frame.place(x=35, y=310)
        else:
            self.playlist_alert()

    def hide_playlist_deleted_frame(self):
        self.playlist_deleted_frame.place_forget()

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
    
    def on_created_playlist_clicked(self):
        if self.get_name_playlist() and self.get_tracks_selected_index():
            self.controller.create_playlist_with_tracks(
                self.get_name_playlist(),
                self.get_tracks_selected_index(),
            )
            self.hide_created_playlist_frame()
        else:
            if self.get_name_playlist():
                self.select_track_from_playlist_alert.place(x=24, y=360)
                self.after(2000, lambda: self.select_track_from_playlist_alert.place_forget())
                
            else:
                self.choose_a_nameplaylist_alert.place(x=23, y=360)
                self.after(2000, lambda: self.choose_a_nameplaylist_alert.place_forget())

    def creat_created_playlist_frame(self):
        if self.controller.all_tracks_info:
            self.create_playlist_frame = ctk.CTkFrame(
                self.library_controls_frame,
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
                border_color="#151515",
                fg_color="#070707",
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

            self.create_playlist_control_frame = ctk.CTkFrame(self.create_playlist_frame, 220, 50, fg_color="#030303")
            self.create_playlist_control_frame.pack()

            self.create_playlist_btn = ctk.CTkButton(
                self.create_playlist_control_frame,
                200,
                fg_color="#0D3F8B",
                hover_color="#0D1F8B",
                border_width=0,
                # corner_radius=1,
                text="created",
                command=self.on_created_playlist_clicked,
            )
            self.create_playlist_btn.pack(side="right")

            self.closed_playlist_frame_btn = ctk.CTkButton(
            self.create_playlist_control_frame,
            width=10,
            height=10,
            fg_color="#0D3F8B",
            hover_color="#0D1F8B",
            text="",
            image=ctk.CTkImage(
                Image.open(resource_path("assets/icons/close.png")),
                size=(20, 20),
            ),
            command=self.hide_created_playlist_frame,
            )
            self.closed_playlist_frame_btn.pack(side="right", padx=2, pady=10)

            self.choose_a_nameplaylist_alert = ctk.CTkLabel(self.create_playlist_frame, 1, 1, text="Choose a name for the playlist.")
            self.select_track_from_playlist_alert = ctk.CTkLabel(
                self.create_playlist_frame,
                1,
                1,
                text="Select tracks from the playlist.",
                )
            
            self.create_playlist_frame.place(y=247)
            self.create_playlist_frame.focus()
            self.refresh_listbox_list_track(self.controller.get_all_track_title())
        else:
            self.empty_list_playlists_lable.place_forget()
            self.update_empty_state(self.controller.all_tracks_info, "all_tracks")
            
    def hide_created_playlist_frame(self):
        self.create_playlist_frame.destroy()
        
    # --==» track actions Frame Methods«==--
    def on_remove_track_clicked(self):
        self.controller.remove_track()
        self.hide_track_actions_frame()
    
    def show_remove_track_frame(self):
        self.track_deleted_frame.place(x=1100, y=510)
        self.track_deleted_frame.lift()

    def hide_remove_track_frame(self):
        self.track_deleted_frame.place_forget()
    
    def show_track_actions_frame(self):
        if self.controller.current_index is not None:
            self.track_actions_frame.place(x=1115, y=510)
            self.closed_track_action_frame_btn.configure(command=self.hide_track_actions_frame)
            self.closed_track_action_frame_btn.place(x=1125, y=520)
        else:
            self.show_hint()
            self.hide_hint()
        
    def hide_track_actions_frame(self):
        self.track_actions_frame.place_forget()
        self.closed_track_action_frame_btn.place_forget()
        self.track_deleted_frame.place_forget()
    
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
        self.closed_track_action_frame_btn.place_forget()

    def _hide_destry(self):
        self.track_actions_frame.after(5000, self.hide_empty_playlist_frame)

    def show_add_to_playlist_frame(self):
        if self.controller.all_playlists_info:
            self.add_to_playlist_frame.place(x=1115, y=515)
            self.refresh_listbox_list_playlist(self.controller.get_playlist_name())
            self.closed_track_action_frame_btn.configure(command=self.hide_add_to_playlist_frame)
            self.closed_track_action_frame_btn.place(x=1115, y=500)
        else:
            self.empty_playlist_frame.place(x=1065, y=515)
            self.closed_track_action_frame_btn.place_forget()
            self._hide_destry()

    def hide_add_to_playlist_frame(self):
        self.closed_track_action_frame_btn.configure(command=self.hide_track_actions_frame)
        self.closed_track_action_frame_btn.place(x=1125, y=520)
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
            draw.rectangle((2, 2, w - 2, h - bottom_cut), fill=300)
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
                img_art, (580, 550), blur_radius=30, bottom_cut=70
            )

            art_ctk = ctk.CTkImage(result_art, size=(580, 550))


            # --- Background (1045x500) ---
            # Resize سریع
            bg = original_img.resize((1045, 500), Image.Resampling.LANCZOS)

            # افکت‌های بک‌گراند
            bg = bg.filter(ImageFilter.GaussianBlur(6))
            bg = ImageEnhance.Brightness(bg).enhance(0.90)

            # اعمال ماسک روی نسخه کوچک
            result_bg = self._apply_dark_mask(
                bg, (1045, 500), blur_radius=30, bottom_cut=60
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
    
    def set_separator(self, selected) -> str:
        sections = {
            "all_tracks": self.show_all_tracks_btn,
            "favorites": self.show_favorites_btn,
            "recently_played": self.show_last_played,
            "playlists": self.show_playlists_btn,

        }

        for name, button in sections.items():
            
            active = name == selected
        
            button.configure(
                font=ctk.CTkFont(
                    size=18,
                    weight="bold" if active else "normal"
                )
            )

    def update_empty_state(self, state, selected):
        labels = {
            "all_tracks": self.empty_track_list_lable,
            "favorites": self.empty_favorite_track_list_lable,
            "playlists": self.empty_list_playlists_lable,
            "searching": self.no_found_lable,
            "playlist_run": self.empty_playlists_run_lable,
        }

        for label in labels.values():
            label.place_forget()

        if state:
            return

        positions = {
            "all_tracks": (-40, 410),
            "favorites": (-45, 410),
            "playlists": (-40, 170),
            "searching": (50, 470),
            "playlist_run": (15, 470),
        }

        if selected in labels:
            x, y = positions[selected]
            labels[selected].place(x=x, y=y)
            
    def state_library_btn(self, state):
        sections = [
            self.show_all_tracks_btn,
            self.show_favorites_btn,
            self.show_last_played,
            self.show_playlists_btn,
        ]

        for button in sections:
            button.configure(
                state = "normal" if state else "disabled",
                text_color_disabled="#dbdbdb",
                cursor = "" if state else "watch",
                )
            
    def playlist_alert(self):
        self.playlist_alert_message.place(x=45, y=330)
        self.playlist_alert_message.after(5000, lambda: self.playlist_alert_message.place_forget())

    def show_hint(self):
        self.hint_lable.place(x=650, y=590)
    
    def hide_hint(self):
        self.hint_lable.after(
        2000,
        lambda: self.hint_lable.place_forget()
    )
    # ==» progressbar Methods «==--
    def show_loading(self):
        self.status_state = False
        self.status_frame.place(y=247)
        self.status_frame.lift()
        self.status_label.configure(text="Loading...")
        self.status_progressbar.configure(mode="indeterminate")
        self.status_progressbar.start()
        self.state_library_btn(False)
        self.configure(cursor="watch")

    def show_progress(self):
        self.status_state = False
        self.status_frame.place(y=247)
        self.status_label.configure(text="Importing tracks...")
        self.status_progressbar.configure(mode="determinate")
        self.status_progressbar.set(0)
        self.state_library_btn(False)
        self.configure(cursor="watch")
    
    def update_progress(self, value):
        self.status_progressbar.set(value)

    def hide_status(self):
        self.status_state = True
        self.status_progressbar.stop()
        self.status_frame.place_forget()
        self.state_library_btn(True)
        self.configure(cursor="")
    
    # ==» Messagebox «==--
    def show_messagebox(self, added=0, skipped=0, errors=0):

        import winsound
        winsound.MessageBeep(winsound.MB_ICONASTERISK)

        dialog = ctk.CTkToplevel(self, fg_color="#151515")

        dialog.title("Success")
        dialog.resizable(False, False)
        # dialog.overrideredirect(True)

        added_message_label = f"{added} tracks added successfully." if added > 1 else f"{added} track added successfully."
        skipped_message_label = f"{skipped} duplicate tracks skipped." if skipped > 1 else f"{skipped} duplicate track skipped."
        errors_message_label = f"Failed to add {errors} tracks." if errors > 1 else f"Failed to add {errors} track."
        
        if added:
            added_label = ctk.CTkLabel(
                dialog,
                text=added_message_label,
                font=("Arial", 17),
                text_color="#dbdbdb",
                wraplength=300,
            )
            added_label.pack(padx=30, pady=(10, 0))

        if skipped:
            skipped_label = ctk.CTkLabel(
                dialog,
                text=skipped_message_label,
                font=("Arial", 17),
                text_color="#dbdbdb",
                wraplength=300,
            )
            skipped_label.pack(padx=30, pady=10)

        if errors:
            error_label = ctk.CTkLabel(
                dialog,
                text=errors_message_label,
                font=("Arial", 17),
                text_color="#dbdbdb",
                wraplength=300,
            )
            error_label.pack(padx=30)

        ok_button = ctk.CTkButton(
            dialog,
            corner_radius=5,
            text="OK",
            fg_color="#0D3F8B",
            hover_color="#0D1F8B",
            width=150,
            command=dialog.destroy
        )
        ok_button.pack(side="bottom", pady=10)

        dialog.transient(self)
        dialog.grab_set()
        
        dialog.update_idletasks()
        width = dialog.winfo_reqwidth()
        height = dialog.winfo_reqheight()
        dialog.geometry(f"{width}x{height}")

        x = self.winfo_x() + (self.winfo_width() // 2) - 10
        y = self.winfo_y() + (self.winfo_height() // 2) - 30
        dialog.geometry(f"+{x}+{y}")

        dialog.wait_window()
