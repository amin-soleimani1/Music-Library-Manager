import customtkinter
from customtkinter import *
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
from io import BytesIO
import os
from CTkListbox import CTkListbox
import tkinter
from utils.file_utils import resource_path

class MusicPlayerUI(customtkinter.CTk):
    def __init__(self, controller):
        super().__init__(fg_color="black")
        self.controller = controller
        self.real_time = tkinter.IntVar(value=0)
        self.state_var = tkinter.IntVar(value=0)
        self.music_len = tkinter.IntVar(value=0)

        self.title("Music Player")
        self.geometry("1266x668+40+30")
        self.resizable(False, False)

        self.build_ui()
        self.bind("<Key>", self.controller.on_key_pressed)

    # ---------------- UI Construction ----------------
    def build_ui(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # ===
        # ----------------------- ( ARTWORK ) -----------------------------
        # ===
        artwork_frame = CTkFrame(
            self,
            fg_color="#000009",
            bg_color="black",
        )
        artwork_frame.grid(column=1, row=0, sticky="nsew")
        artwork_frame.grid_columnconfigure(0, weight=1)
        artwork_frame.grid_rowconfigure(0, weight=1)
        artwork_frame.grid_rowconfigure(1, weight=0)

        # Background
        # فیلتر
        img = Image.open("assets/images/artwork.png").convert("RGB")
        img_blurred = img.filter(ImageFilter.GaussianBlur(5))
        brightness_enhancer = ImageEnhance.Brightness(img_blurred)
        img_darkened = brightness_enhancer.enhance(0.90)
        mask = Image.new("L", img_darkened.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rectangle(
            (20, 20, img_darkened.width - 20, img_darkened.height - 400), fill=255
        )
        mask = mask.filter(ImageFilter.GaussianBlur(180))
        shadow = Image.new("RGB", img_darkened.size, "#000009")
        self.result_background = Image.composite(img_darkened, shadow, mask)
        # فیلتر
        self.default_background = CTkImage(
            self.result_background,
            size=(1045, 500),
        )

        self.background = CTkLabel(
            artwork_frame,
            image=self.default_background,
        )
        self.background.place(x=0, y=0)

        # Artwork
        # فیلتر --
        img_default_art = Image.open("assets/images/artwork.png").convert("RGB")
        mask_img_default_art = Image.new("L", img_default_art.size, 0)
        draw_img_default_art = ImageDraw.Draw(mask_img_default_art)
        draw_img_default_art.rectangle(
            (20, 20, img_default_art.width - 20, img_default_art.height - 450),
            fill=255,
        )
        mask_img_default_art = mask_img_default_art.filter(
            ImageFilter.GaussianBlur(150)
        )
        dark_img_default_art = Image.new("RGB", img_default_art.size, "#000009")
        result_default_art = Image.composite(
            img_default_art, dark_img_default_art, mask_img_default_art
        )
        # فیلتر --
        self.default_art = CTkImage(
            result_default_art,
            size=(580, 550),
        )
        self.art_label = CTkLabel(
            artwork_frame,
            text="",
            image=self.default_art,
        )
        self.art_label.grid(column=0, row=0)

        # Title
        self.title_label = CTkLabel(
            artwork_frame,
            text="Music Name",
            font=CTkFont(family="Baskerville Old Face", size=35, weight="bold"),
        )
        self.title_label.grid(column=0, row=1, pady=(10, 15), sticky="ew")

        # ===
        # ------------------------ ( CONTROLLS ) -------------------------
        # ===
        controll_frame = CTkFrame(self, height=100, fg_color="#000005")
        controll_frame.grid(column=1, row=1, sticky="nsew")
        controll_frame.columnconfigure((0, 2), weight=0)
        controll_frame.columnconfigure(1, weight=1)
        controll_frame.rowconfigure(0, weight=1)

        # فریم دکمه های پلی نکست ...
        buttons_frame = CTkFrame(controll_frame, height=50, fg_color="#000005")
        buttons_frame.grid(column=0, row=0, sticky="nsew")
        buttons_frame.grid_columnconfigure(([i for i in range(0, 7)]), weight=0)
        buttons_frame.grid_rowconfigure(0, weight=1)

        self.play_icon = CTkImage(
            Image.open(
                resource_path("assets/icons/start_dark_new.png")
            ),
            size=(40, 40),
        )
        self.pause_icon = CTkImage(
            Image.open(resource_path("assets/icons/stop_dark_new.png")),
            size=(40, 40),
        )
        self.next_icon = CTkImage(
            Image.open(resource_path("assets/icons/right_light.png")),
            size=(20, 20),
        )
        self.prev_icon = CTkImage(
            Image.open(resource_path("assets/icons/left_light.png")),
            size=(20, 20),
        )

        self.stop_icon = CTkImage(
            Image.open(resource_path("assets/icons/stop.png")),
            size=(12, 12),
        )

        self.favorite_icon_deselect = CTkImage(
            Image.open(resource_path("assets/icons/like.png")),
            size=(15, 15),
        )

        self.favorite_icon_select = CTkImage(
            Image.open(resource_path("assets/icons/likedo.png")),
            size=(15, 15),
        )

        self.pause_unpause_btn = CTkButton(
            buttons_frame,
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

        CTkButton(
            buttons_frame,
            width=0,
            height=0,
            text="",
            bg_color="transparent",
            fg_color="transparent",
            image=self.prev_icon,
            hover_color="#000010",
            command=self.controller.on_previous_track_clicked,
        ).grid(column=1, row=0)

        CTkButton(
            buttons_frame,
            width=0,
            height=0,
            text="",
            bg_color="transparent",
            fg_color="transparent",
            image=self.next_icon,
            hover_color="#000010",
            command=self.controller.on_next_track_clicked,
        ).grid(column=3, row=0)

        CTkButton(
            buttons_frame,
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

        self.toggle_favorite_btn = CTkButton(
            buttons_frame,
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

        CTkButton(
            buttons_frame,
            text="",
            width=0,
            height=0,
            fg_color="transparent",
            image=CTkImage(
                Image.open(resource_path("assets/icons/agine.png")),
                size=(13, 13),
            ),
            bg_color="black",
            border_width=0,
            state="disabled",
        ).grid(column=4, row=0, padx=7)

        CTkLabel(
            buttons_frame,
            text="",
            image=CTkImage(
                Image.open(resource_path("assets/icons/PicsArt_05-14-12.28.21.png")),
                size=(1, 35),
            ),
        ).grid(column=6, row=0, padx=10)

        # ---- TIME SLAIDER ----
        slider_frame = CTkFrame(controll_frame, height=50, fg_color="#000005")
        slider_frame.grid(column=1, row=0, sticky="nsew")
        slider_frame.grid_columnconfigure(1, weight=1)
        slider_frame.grid_columnconfigure((0, 2), weight=0)
        slider_frame.grid_rowconfigure(0, weight=1)

        # slider time
        self.slider_time = CTkSlider(
            slider_frame,
            progress_color="#001F63",
            button_color="#001F63",
            fg_color="#151515",
            from_=0,
            to=100,
            variable=self.state_var,
            command=self.controller.on_time_slider_clicked,
        )
        self.slider_time.grid(column=1, row=0, sticky="ew")

        # current time lab
        self.lab_sli_current_time = CTkLabel(slider_frame, text="00:00")
        self.lab_sli_current_time.grid(column=0, row=0, padx=5, sticky="nsew")

        # time len lab
        self.lab_sli_time_len = CTkLabel(slider_frame, text="00:00")
        self.lab_sli_time_len.grid(column=2, row=0, padx=5, sticky="nsew")

        # ---- volume frame ----
        volume_frame = CTkFrame(controll_frame, height=50, fg_color="#000005")
        volume_frame.grid(column=2, row=0, sticky="nsew")
        volume_frame.columnconfigure((0, 1, 3, 4), weight=0)
        volume_frame.columnconfigure(2, weight=1)
        volume_frame.rowconfigure(0, weight=1)

        CTkLabel(
            volume_frame,
            text="",
            image=CTkImage(
                Image.open(resource_path("assets/icons/PicsArt_05-14-12.28.21.png")),
                size=(1, 35),
            ),
        ).grid(column=0, row=0, padx=10)

        CTkLabel(
            volume_frame,
            text="",
            image=CTkImage(
                Image.open(resource_path("assets/icons/addvol.png")),
                size=(12, 12),
            ),
        ).grid(column=3, row=0, padx=(5, 10))

        CTkLabel(
            volume_frame,
            text="",
            image=CTkImage(
                Image.open(resource_path("assets/icons/rewol.png")),
                size=(12, 12),
            ),
        ).grid(column=1, row=0, padx=(30, 0))

        # Volume Slider
        self.volume_slider = CTkSlider(
            volume_frame,
            fg_color="#151515",
            width=90,
            height=10,
            progress_color="#001F63",
            button_color="#001F63",
            variable=tkinter.IntVar(value=1),
            command=self.controller.on_volume_clicked,
        )
        self.volume_slider.grid(column=2, row=0, padx=5)

        self.seg_btn = CTkButton(
            volume_frame,
            text="",
            fg_color="transparent",
            width=0,
            height=0,
            hover_color="#000010",
            image=CTkImage(
                Image.open(resource_path("assets/icons/senoghte.png")),
                size=(40, 50),
            ),
            command=self.controller.open_track_actions_window,
        ).grid(column=4, row=0, padx=(5, 0))

        # ===
        # ---------------------- ( sidebar ) ------------------------
        # ===
        sidebar = CTkFrame(self, width=200, fg_color="#030303")
        sidebar.grid(column=0, row=0, rowspan=2, sticky="nsew")
        sidebar.grid_columnconfigure(0, weight=1)
        sidebar.grid_rowconfigure(([i for i in range(7)]), weight=0)
        sidebar.grid_rowconfigure(7, weight=1)
        # sidebar.grid_rowconfigure(8, weight=0)

        frame_search = CTkFrame(
            sidebar,
            height=30,
            fg_color="#030303",
        )
        frame_search.grid(column=0, row=0, pady=10)
        frame_search.grid_columnconfigure(0, weight=0)
        frame_search.grid_columnconfigure(1, weight=1)
        frame_search.rowconfigure(0, weight=1)

        self.entry_searching = CTkEntry(
            frame_search,
            height=30,
            corner_radius=25,
            border_width=1,
            border_color="#151515",
            placeholder_text="Search Music",
            width=170,
            fg_color="#070707",
            justify="center",
            font=CTkFont(size=12),
        )
        self.entry_searching.grid(column=1, row=0)
        self.entry_searching.bind("<KeyRelease>", self.on_text_change)

        CTkButton(
            frame_search,
            fg_color="#030303",
            width=10,
            height=10,
            hover_color="#080808",
            text="",
            image=CTkImage(
                Image.open(resource_path("assets/icons/PicsArt_05-14-01.58.55.png")),
                size=(25, 20),
            ),
            command=self.on_add_music,
        ).grid(column=0, row=0)

        CTkLabel(
            sidebar,
            width=170,
            text="Library",
            text_color="#dbdbdb",
            font=CTkFont(family="Baskerville Old Face", size=45, weight="bold"),
        ).grid(column=0, row=1, pady=5, sticky="w")

        self.all_song_btn = CTkButton(
            sidebar,
            text="All song",
            text_color="#dbdbdb",
            hover_color="#080808",
            image=CTkImage(
                Image.open(resource_path("assets/icons/all_song.png")),
                size=(20, 20),
            ),
            width=200,
            corner_radius=0,
            fg_color="#030303",
            anchor="w",
            font=CTkFont(size=17),
            command=self.controller.on_show_all_tracks_clicked,
        )
        self.all_song_btn.grid(column=0, row=2, pady=10)

        self.playlist_btn = CTkButton(
            sidebar,
            text="Playlists",
            text_color="#dbdbdb",
            hover_color="#080808",
            width=200,
            image=CTkImage(
                Image.open(resource_path("assets/icons/play_list.png")),
                size=(20, 20),
            ),
            corner_radius=0,
            fg_color="#030303",
            anchor="w",
            font=CTkFont(size=17),
            command=self.controller.open_playlists_window,
        )
        self.playlist_btn.grid(column=0, row=5, pady=10)

        self.show_favorite_btn = CTkButton(
            sidebar,
            text="Favorites",
            text_color="#dbdbdb",
            hover_color="#080808",
            width=200,
            image=CTkImage(
                Image.open(resource_path("assets/icons/like.png")),
                size=(20, 20),
            ),
            corner_radius=0,
            fg_color="#030303",
            font=CTkFont(size=17),
            anchor="w",
            command=self.controller.on_show_favorites_tracks_clicked,
        )
        self.show_favorite_btn.grid(column=0, row=3, pady=10)

        self.five_btn = CTkButton(
            sidebar,
            text="Recently played",
            text_color="#dbdbdb",
            hover_color="#080808",
            width=200,
            image=CTkImage(
                Image.open(resource_path("assets/icons/recom.png")),
                size=(20, 17),
            ),
            corner_radius=0,
            fg_color="#030303",
            font=CTkFont(size=17),
            anchor="w",
            command=self.controller.on_show_last_played_clicked,
        )
        self.five_btn.grid(column=0, row=4, pady=10)

        self.main_listbox = CTkListbox(
            sidebar,
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

        # progressbar
        self.loading_frame = CTkFrame(
            sidebar,
            width=200,
            height=335,
            border_width=0,
            fg_color="#030303",
            bg_color="black",
        )

        self.loading_label = CTkLabel(self.loading_frame, text="")
        self.loading_progress = CTkProgressBar(
            self.loading_frame,
            height=3,
            width=180,
            fg_color="#151515",
            progress_color="#404040",
        )

        self.loading_label.pack(pady=(20, 10))
        self.loading_progress.pack(padx=21)

    # ---------------- UI Event methods ----------------

    def on_text_change(self, event):
        text = self.entry_searching.get()

        if len(text) >= 3:
            self.controller.search_tracks(text)

    def reset_search_entry(self):
        self.entry_searching.delete(0, "end")
        self.entry_searching.focus()
        self.focus()

    def search_entry_get(self):
        return self.entry_searching.get()

    # ---------------- UI Update methods ----------------

    # Artwork and Title
    def update_title(self, name):
        self.title_label.configure(text=name)

    def update_toggle_favorite_btn(self, select: bool):
        self.toggle_favorite_btn.configure(
            image=self.favorite_icon_select if select else self.favorite_icon_deselect
        )

    def update_artwork(self, artwork):
        # 1. تعریف توابع کمکی برای تمیزی کد
        def _set_defaults():
            self.art_label.configure(image=self.default_art)
            self.art_label.image = self.default_art
            self.background.configure(image=self.default_background)
            self.background.image = self.default_background

        def _load_image(obj):
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

        def _apply_dark_mask(img, size, blur_radius, bottom_cut):
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

        # 2. لود کردن عکس
        original_img = _load_image(artwork)
        if not original_img:
            _set_defaults()
            return

        try:
            # --- Foreground (art_label: 580x550) ---
            # ابتدا Resize می‌کنیم (بسیار سریع‌تر از بلور کردن عکس بزرگ)
            img_art = original_img.resize((580, 550), Image.Resampling.LANCZOS)

            # اعمال افکت روی نسخه کوچک
            result_art = _apply_dark_mask(
                img_art, (580, 550), blur_radius=30, bottom_cut=100
            )

            art_ctk = CTkImage(result_art, size=(580, 550))
            self.art_label.configure(image=art_ctk)
            self.art_label.image = art_ctk

            # --- Background (1045x500) ---
            # Resize سریع
            bg = original_img.resize((1045, 500), Image.Resampling.LANCZOS)

            # افکت‌های بک‌گراند
            bg = bg.filter(ImageFilter.GaussianBlur(5))
            bg = ImageEnhance.Brightness(bg).enhance(0.90)

            # اعمال ماسک روی نسخه کوچک
            result_bg = _apply_dark_mask(
                bg, (1045, 500), blur_radius=50, bottom_cut=100
            )

            bg_ctk = CTkImage(result_bg, size=(1045, 500))
            self.background.configure(image=bg_ctk)
            self.background.image = bg_ctk

        except Exception as e:
            print(f"Error processing image: {e}")
            _set_defaults()

    # Button Play
    def update_pause_unpause_btn(self, playing: bool):
        self.pause_unpause_btn.configure(
            image=self.play_icon if playing else self.pause_icon
        )

    # Reset UI
    def reset_ui(self):
        self.update_title("Music Name")
        self.background.configure(image=self.default_background)
        self.update_artwork(None)
        self.update_pause_unpause_btn(False)
        self.update_lab_current("00:00")
        self.update_lab_time_len("00:00")
        self.real_time.set(0)
        self.state_var.set(0)
        self.update_toggle_favorite_btn(False)

    # Slider Time

    def update_slider_to(self, intger):
        self.slider_time.configure(to=intger)

    def update_lab_current(self, new_text):
        self.lab_sli_current_time.configure(text=new_text)

    def update_lab_time_len(self, new_text):
        self.lab_sli_time_len.configure(text=new_text)

    def set_loading_state(self, state: bool):
        print(state)

    # progressbar update
    def show_loading_overlay(self):
        self.main_listbox.grid_remove()

        self.loading_frame.grid(
            column=0,
            row=7,
            sticky="nsew",
        )
        self.loading_label.configure(text="Loading...")
        self.loading_progress.configure(mode="indeterminate")
        self.loading_progress.start()

    def hide_loading_overlay(self):

        self.loading_progress.stop()

        self.loading_frame.grid_remove()

        self.main_listbox.grid()

    def show_Adding_overlay(self):
        self.main_listbox.grid_remove()

        self.loading_frame.grid(
            column=0,
            row=7,
            sticky="nsew",
        )
        self.loading_label.configure(text="Importing tracks...")
        self.loading_progress.configure(mode="determinate")
        self.loading_progress.set(0)

    def update_progress(self, value):
        self.loading_progress.set(value)

    # ---------------- Playlist helpers ----------------

    def main_listbox_del(self):
        self.main_listbox.delete(0, "end")

    def main_listbox_insert(self, tracks_title):
        for title in tracks_title:
            self.main_listbox.insert("end", title)

    def main_listbox_on_track_insert(self, title):
        self.main_listbox.insert("end", title)

    def on_add_music(self):
        from tkinter.filedialog import askopenfilenames

        paths = askopenfilenames(
            title="انتخاب موزیک‌ها", filetypes=[("MP3 Files", "*.mp3")]
        )

        if paths:  # اگر کاربر چیزی انتخاب کرد
            # فقط لیست مسیرها را به کنترولر بده
            self.controller.add_tracks_to_library(paths)

    def get_selected_index_main_listbox(self):
        return self.main_listbox.curselection()

    def select_main_listbox(self, idx):
        try:
            if idx < self.main_listbox.size():
                self.main_listbox.activate(idx)
        except:
            pass

    def unselect_main_listbox(self, idx):
        self.main_listbox.deactivate(idx)

    # def main_list_box_del_by_on_index(self, index):
    # def get_selected_name(self):
    #     return self.main_listbox.get(self.main_listbox.curselection())

    def size(self):
        return self.main_listbox.size()

# if __name__ == "__main__":
#     view = MusicPlayerUI(DummyController())
#     view.mainloop()
