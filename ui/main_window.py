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

        # Current playback position (seconds)
        self.current_position_var = ctk.IntVar(value=0)

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
            text="Music Name",
            font=ctk.CTkFont(family="Baskerville Old Face", size=35, weight="bold"),
        )
        self.track_title_label.pack(pady=10)

        self.default_artwork_path = "assets/images/artwork.png"

        # ==» Playback Controls Frame «==---------------------------
        playback_controls_frame = ctk.CTkFrame(self, height=100, fg_color="#000005")
        playback_controls_frame.grid(column=1, row=1, sticky="nsew")
        playback_controls_frame.columnconfigure((0, 2), weight=0)
        playback_controls_frame.columnconfigure(1, weight=1)
        playback_controls_frame.rowconfigure(0, weight=1)

        # --==» Playback Buttons Frame «==--
        playback_buttons_frame = ctk.CTkFrame(playback_controls_frame, height=50, fg_color="#000005")
        playback_buttons_frame.grid(column=0, row=0, sticky="nsew")
        playback_buttons_frame.grid_columnconfigure(([i for i in range(0, 7)]), weight=0)
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
        self.next_icon = ctk.CTkImage(
            Image.open(resource_path("assets/icons/right_light.png")),
            size=(20, 20),
        )
        self.prev_icon = ctk.CTkImage(
            Image.open(resource_path("assets/icons/left_light.png")),
            size=(20, 20),
        )
        self.stop_icon = ctk.CTkImage(
            Image.open(resource_path("assets/icons/stop.png")),
            size=(12, 12),
        )
        self.favorite_icon_deselect = ctk.CTkImage(
            Image.open(resource_path("assets/icons/like.png")),
            size=(15, 15),
        )
        self.favorite_icon_select = ctk.CTkImage(
            Image.open(resource_path("assets/icons/likedo.png")),
            size=(15, 15),
        )

        # stop button
        ctk.CTkButton(
            playback_buttons_frame,
            text="",
            width=0,
            height=0,
            fg_color="transparent",
            image=self.stop_icon,
            bg_color="black",
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
            image=self.prev_icon,
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
        self.pause_unpause_btn.grid(column=2, row=0, padx=7, pady=5)

        # next button
        ctk.CTkButton(
            playback_buttons_frame,
            width=0,
            height=0,
            text="",
            bg_color="transparent",
            fg_color="transparent",
            image=self.next_icon,
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
                Image.open(resource_path("assets/icons/agine.png")),
                size=(13, 13),
            ),
            bg_color="black",
            border_width=0,
            state="disabled",
            # command=
        )
        self.repeat_mode_btn.grid(column=4, row=0, padx=7)

        self.toggle_favorite_btn = ctk.CTkButton(
            playback_buttons_frame,
            text="",
            image=self.favorite_icon_deselect,
            width=0,
            height=0,
            hover_color="#000010",
            fg_color="transparent",
            border_width=0,
            command=self.controller.on_toggle_favorite_clicked,
        )
        self.toggle_favorite_btn.grid(column=5, row=0, padx=(0, 7))

        # separator_label
        ctk.CTkLabel(
            playback_buttons_frame,
            text="",
            image=ctk.CTkImage(
                Image.open(resource_path("assets/icons/PicsArt_05-14-12.28.21.png")),
                size=(1, 35),
            ),
        ).grid(column=6, row=0, padx=10)

        # --==» Time Slider Frame «==--
        time_slider_frame = ctk.CTkFrame(playback_controls_frame, height=50, fg_color="#000005")
        time_slider_frame.grid(column=1, row=0, sticky="nsew")
        time_slider_frame.grid_columnconfigure(1, weight=1)
        time_slider_frame.grid_columnconfigure((0, 2), weight=0)
        time_slider_frame.grid_rowconfigure(0, weight=1)

        # current position lable
        self.current_position_lable = ctk.CTkLabel(time_slider_frame, text="00:00")
        self.current_position_lable.grid(column=0, row=0, padx=5, sticky="nsew")

        self.time_slider = ctk.CTkSlider(
            time_slider_frame,
            progress_color="#001F63",
            button_color="#001F63",
            fg_color="#151515",
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
                Image.open(resource_path("assets/icons/PicsArt_05-14-12.28.21.png")),
                size=(1, 35),
            ),
        ).grid(column=0, row=0, padx=10)

        # اینارو اصلاح کن...
        ctk.CTkLabel(
            volume_controls_frame,
            text="",
            image=ctk.CTkImage(
                Image.open(resource_path("assets/icons/addvol.png")),
                size=(12, 12),
            ),
        ).grid(column=3, row=0, padx=(5, 10))
        ctk.CTkLabel(
            volume_controls_frame,
            text="",
            image=ctk.CTkImage(
                Image.open(resource_path("assets/icons/rewol.png")),
                size=(12, 12),
            ),
        ).grid(column=1, row=0, padx=(30, 0))

        # Volume Slider
        self.volume_slider = ctk.CTkSlider(
            volume_controls_frame,
            fg_color="#151515",
            width=90,
            height=10,
            progress_color="#001F63",
            button_color="#001F63",
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
                Image.open(resource_path("assets/icons/senoghte.png")),
                size=(40, 50),
            ),
            command=self.controller.open_track_actions_window,
        ).grid(column=4, row=0, padx=(5, 0))

        # ==» Library Controls Frame «==---------------------------
        library_controls_frame = ctk.CTkFrame(self, width=200, fg_color="#030303")
        library_controls_frame.grid(column=0, row=0, rowspan=2, sticky="nsew")
        library_controls_frame.grid_columnconfigure(0, weight=1)
        library_controls_frame.grid_rowconfigure(([i for i in range(7)]), weight=0)
        library_controls_frame.grid_rowconfigure(7, weight=1)

        # --==» Search Frame Frame «==--
        search_frame = ctk.CTkFrame(
            library_controls_frame,
            height=30,
            fg_color="#030303",
        )
        search_frame.grid(column=0, row=0, pady=10)
        search_frame.grid_columnconfigure(0, weight=0)
        search_frame.grid_columnconfigure(1, weight=1)
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
        self.search_entry.grid(column=1, row=0)
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
                Image.open(resource_path("assets/icons/PicsArt_05-14-01.58.55.png")),
                size=(25, 20),
            ),
            command=self.on_select_tracks,
        ).grid(column=0, row=0)

        # ==» Library Controls Frame «==--
        # library title lable
        ctk.CTkLabel(
            library_controls_frame,
            width=170,
            text="Library",
            text_color="#dbdbdb",
            font=ctk.CTkFont(family="Baskerville Old Face", size=45, weight="bold"),
        ).grid(column=0, row=1, pady=5, sticky="w")

        self.show_all_tracks_btn = ctk.CTkButton(
            library_controls_frame,
            text="All song",
            text_color="#dbdbdb",
            hover_color="#080808",
            image=ctk.CTkImage(
                Image.open(resource_path("assets/icons/all_song.png")),
                size=(20, 20),
            ),
            width=200,
            corner_radius=0,
            fg_color="#030303",
            anchor="w",
            font=ctk.CTkFont(size=17),
            command=self.controller.on_show_all_tracks_clicked,
        )
        self.show_all_tracks_btn.grid(column=0, row=2, pady=10)

        self.show_playlists_btn = ctk.CTkButton(
            library_controls_frame,
            text="Playlists",
            text_color="#dbdbdb",
            hover_color="#080808",
            width=200,
            image=ctk.CTkImage(
                Image.open(resource_path("assets/icons/play_list.png")),
                size=(20, 20),
            ),
            corner_radius=0,
            fg_color="#030303",
            anchor="w",
            font=ctk.CTkFont(size=17),
            command=self.controller.open_playlists_window,
        )
        self.show_playlists_btn.grid(column=0, row=5, pady=10)

        self.show_favorites_btn = ctk.CTkButton(
            library_controls_frame,
            text="Favorites",
            text_color="#dbdbdb",
            hover_color="#080808",
            width=200,
            image=ctk.CTkImage(
                Image.open(resource_path("assets/icons/like.png")),
                size=(20, 20),
            ),
            corner_radius=0,
            fg_color="#030303",
            font=ctk.CTkFont(size=17),
            anchor="w",
            command=self.controller.on_show_favorites_tracks_clicked,
        )
        self.show_favorites_btn.grid(column=0, row=3, pady=10)

        self.show_last_played = ctk.CTkButton(
            library_controls_frame,
            text="Recently played",
            text_color="#dbdbdb",
            hover_color="#080808",
            width=200,
            image=ctk.CTkImage(
                Image.open(resource_path("assets/icons/recom.png")),
                size=(20, 17),
            ),
            corner_radius=0,
            fg_color="#030303",
            font=ctk.CTkFont(size=17),
            anchor="w",
            command=self.controller.on_show_last_played_clicked,
        )
        self.show_last_played.grid(column=0, row=4, pady=10)

        self.main_listbox = CTkListbox(
            library_controls_frame,
            width=200,
            height=335,
            border_width=0,
            fg_color="#030303",
            hover_color="#080808",
            bg_color="black",
            button_color="#050505",
            highlight_color="#101010",
            command=self.controller.on_track_selected,
        )
        self.main_listbox.grid(column=0, row=7)
        self.main_listbox._scrollbar.configure(
            button_color="#080808", button_hover_color="#121212"
        )

        # --==» status progressbar frame «==--
        self.status_frame = ctk.CTkFrame(
            library_controls_frame,
            width=200,
            height=335,
            border_width=0,
            fg_color="#030303",
            bg_color="black",
        )

        self.status_label = ctk.CTkLabel(self.status_frame, text="")
        self.status_progressbar = ctk.CTkProgressBar(
            self.status_frame,
            height=3,
            width=180,
            fg_color="#151515",
            progress_color="#404040",
        )

        self.status_label.pack(pady=(20, 0))
        self.status_progressbar.pack(padx=21)
    
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
        self.current_position_var.set(0)
        self.time_slider_position_var.set(0)
        self.update_toggle_favorite_btn(False)

    # ==» Search Methods «==---------------------------
    def on_text_change(self, event):
        text = self.search_entry.get()

        if len(text) >= 3:
            self.controller.search_tracks(text)

    def search_entry_get(self):
        return self.search_entry.get()

    def reset_search_entry(self):
        self.search_entry.delete(0, "end")
        self.search_entry.focus()
        self.focus()

    # ==» progressbar Methods «==---------------------------
    def show_loading(self):
        self.main_listbox.grid_remove()

        self.status_frame.grid(
            column=0,
            row=7,
            sticky="nsew",
        )
        self.status_label.configure(text="Loading...")
        self.status_progressbar.configure(mode="indeterminate")
        self.status_progressbar.start()

    def show_progress(self):
        self.main_listbox.grid_remove()

        self.status_frame.grid(
            column=0,
            row=7,
            sticky="nsew",
        )
        self.status_label.configure(text="Importing tracks...")
        self.status_progressbar.configure(mode="determinate")
        self.status_progressbar.set(0)
    
    def update_progress(self, value):
        self.status_progressbar.set(value)

    def hide_status(self):
        self.status_progressbar.stop()
        self.status_frame.grid_remove()
        self.main_listbox.grid()

    # ==» Playlist Helpers «==---------------------------
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