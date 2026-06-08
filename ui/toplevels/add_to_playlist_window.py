import customtkinter as ctk
from CTkListbox import CTkListbox


class AddToPlaylistWindow(ctk.CTkToplevel):
    def __init__(self, master, controller):
        super().__init__(master, fg_color="#000009")  # دریافت والد از پنجره اصلی
        self.controller = controller
        self.geometry("200x105+1110+565")
        self.overrideredirect(True)
        self.build_ui()

    def build_ui(self):

        self.listbox_for_playlist_top = CTkListbox(
            self,
            105,
            190,
            border_width=0,
            command=self.controller.on_add_to_playlist_clicked,
        )
        self.listbox_for_playlist_top.pack()

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
        self.empty_playlist_label.pack(padx=(0, 10))

    def refresh(self, list_pl):
        try:
            self.listbox_for_playlist_top.delete(0, "end")
            self.listbox_insert(list_pl)
        except AttributeError:
            pass

    def listbox_insert(self, pls):
        for pl in pls:
            self.listbox_for_playlist_top.insert("end", pl)

    def get_idx_listbox(self):
        return self.listbox_for_playlist_top.curselection()

    # def p(self, name):
    #     self.controller.insert_track_to_pl_db_B()
    #     self.after(10, lambda: self.destroy())

    def show_empty_playlist_frame(self):
        self.listbox_for_playlist_top.pack_forget()
        self.empty_playlist_frame.pack(pady=(20, 0))

    def hide_empty_playlist_frame(self):
        self.empty_playlist_frame.pack_forget()
        self.listbox_for_playlist_top.pack()
        self.destroy()

    def _hide_destry(self):
        self.after(5000, self.hide_empty_playlist_frame)
