import customtkinter as ctk
from CTkListbox import CTkListbox


class CreatePlaylistWindow(ctk.CTkToplevel):
    def __init__(self, master, controller):
        super().__init__(
            master,
            fg_color="#030303",
        )  # دریافت والد از پنجره اصلی
        self.controller = controller
        self.geometry("220x368+49+360")
        self.overrideredirect(True)

        self.name_playlist_entry = ctk.CTkEntry(
            self,
            170,
            corner_radius=15,
            placeholder_text="playlist name :",
            justify="center",
            border_width=1,
            border_color="#101010",
            fg_color="#030303",
        )
        self.name_playlist_entry.pack(pady=10)

        self.tracks_list = CTkListbox(
            self,
            270,
            200,
            border_width=0,
            fg_color="#030303",
            hover_color="#080808",
            bg_color="black",
            button_color="#050505",
            highlight_color="#101010",
            multiple_selection=True,
        )
        self.tracks_list.pack(padx=(10, 0))
        self.tracks_list._scrollbar.configure(
            button_color="#030303", button_hover_color="#080808"
        )

        self.created_btn = ctk.CTkButton(
            self,
            240,
            fg_color="#001F63",
            hover_color="#001F50",
            border_width=0,
            corner_radius=0,
            text="created",
            command=self.on_created_playlist_clicked,
        )
        self.created_btn.pack()

    def get_name_playlist(self):
        return self.name_playlist_entry.get()

    def des(self):
        self.after(10, lambda: self.destroy())

    def refresh(self, list_pl):
        # pass
        try:
            self.tracks_list.delete(0, "end")
            self.insert(list_pl)
        except AttributeError:
            pass

    def insert(self, pls):
        for pl in pls:
            self.tracks_list.insert("end", pl)

    def get_tracks_selected_index(self):
        tracks_selected_index = self.tracks_list.curselection()
        if tracks_selected_index is not None:
            return tracks_selected_index

    def on_created_playlist_clicked(self):
        if self.get_name_playlist():
            self.controller.create_playlist_with_tracks(
                self.get_name_playlist(),
                self.get_tracks_selected_index(),
            )
            self.after(10, lambda: self.destroy())
        else:
            self.destroy()
