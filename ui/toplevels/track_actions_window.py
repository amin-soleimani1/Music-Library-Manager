import customtkinter as ctk
from PIL import Image


class TrackActionsWindow(ctk.CTkToplevel):
    def __init__(self, master, controller):
        super().__init__(master, fg_color="#000009")  # دریافت والد از پنجره اصلی
        self.geometry("130x80+1180+590")
        self.overrideredirect(True)
        self.controller = controller

        self.close_btn = ctk.CTkButton(
            self,
            height=25,
            fg_color="#000009",
            corner_radius=0,
            hover_color="#000003",
            text="Add to Playlist",
            image=ctk.CTkImage(
                Image.open("assets/icons/add_to_playl.png"), size=(20, 20)
            ),
            font=ctk.CTkFont(size=13),
            command=self.controller.open_add_to_playlist_window,
            anchor="w",
        )
        self.close_btn.place(x=5, y=20)

        self.remove_btn = ctk.CTkButton(
            self,
            height=25,
            fg_color="#000009",
            corner_radius=0,
            hover_color="#000003",
            image=ctk.CTkImage(Image.open("assets/icons/remove.png"), size=(20, 20)),
            text="Removed Track",
            font=ctk.CTkFont(size=13),
            command=self.re_des,
            anchor="w",
        )
        self.remove_btn.place(x=5, y=50)

    def re_des(self):
        self.controller.remove_track()
        self.destroy()
