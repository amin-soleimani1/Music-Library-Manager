import customtkinter as ctk
from CTkListbox import CTkListbox


class PlaylistsWindow(ctk.CTkToplevel):
    def __init__(self, master, controller):
        super().__init__(
            master,
            fg_color="#030303",
        )  # دریافت والد از پنجره اصلی
        self.controller = controller
        self.geometry("220x368+49+360")
        self.overrideredirect(True)
        self.build_ui()

    def build_ui(self):

        self.created_playlist_btn = ctk.CTkButton(
            self,
            150,
            fg_color="#050505",
            hover_color="#030303",
            border_width=1,
            border_color="#101010",
            corner_radius=15,
            text="+ created",
            command=self.controller.open_create_playlist_window,
        )
        self.created_playlist_btn.pack(pady=10)

        self.listbox_list_playlist = CTkListbox(
            self,
            height=270,
            width=200,
            fg_color="#030303",
            hover_color="#080808",
            bg_color="black",
            button_color="#050505",
            highlight_color="#101010",
            border_width=0,
            command=self.s,
        )
        self.listbox_list_playlist.pack(padx=(10, 0))
        self.listbox_list_playlist._scrollbar.configure(
            button_color="#030303", button_hover_color="#080808"
        )

        self.btn_frame = ctk.CTkFrame(master=self, width=250, height=50, fg_color="transparent")
        self.btn_frame.pack(pady=(0, 12))
        self.btn_frame.pack_propagate(False)
        
        self.closed_window_btn = ctk.CTkButton(
            master=self.btn_frame,
            width=40,
            height=40,
            fg_color="#001F63",
            hover_color="#001F50",
            border_width=0,
            corner_radius=0,
            text="close",
            command=self.destroy,
        )
        self.closed_window_btn.pack(side="left", padx=10)
        
        self.deleted_playlist_btn = ctk.CTkButton(
            master=self.btn_frame,
            width=40,
            height=40,
            fg_color="#001F63",
            hover_color="#001F50",
            border_width=0,
            corner_radius=0,
            text="deleted",
            # command=self.destroy,
        )
        self.deleted_playlist_btn.pack(side="left")
        
        self.edited_playlist_btn = ctk.CTkButton(
            master=self.btn_frame,
            width=40,
            height=40,
            fg_color="#001F63",
            hover_color="#001F50",
            border_width=0,
            corner_radius=0,
            text="edited",
            # command=self.destroy,
        )
        self.edited_playlist_btn.pack(side="left", padx=10)
        
        self.run_playlist_btn = ctk.CTkButton(
            master=self.btn_frame,
            width=40,
            height=40,
            fg_color="#001F63",
            hover_color="#001F50",
            border_width=0,
            corner_radius=0,
            text="run",
            # command=self.destroy,
        )
        self.run_playlist_btn.pack(side="left", padx=(0, 10))

    def refresh_listbox_playlists_window(self, list_pl):
        # pass
        try:
            self.listbox_list_playlist.delete(0, "end")
            self.listbox_insert(list_pl)
        except AttributeError:
            pass

    def listbox_insert(self, pls):
        for pl in pls:
            self.listbox_list_playlist.insert("end", pl)

    def top_get_select(self):
        return self.listbox_list_playlist.curselection()

    def s(self, name):
        index = self.top_get_select()
        if index is not None:
            self.controller.on_playlist_selected(index)
            # self.after(10, lambda: self.destroy())
