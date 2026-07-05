import pygame
import os


class MusicPlayer:
    
    def __init__(self):
        pygame.mixer.init()
        self._paused = False

    def play(self, file_path, start=None):

        if file_path and os.path.exists(file_path):
            try:
                pygame.mixer.music.load(file_path)
                
                if start is not None:
                    pygame.mixer.music.play(start=start)
                    self.set_volume(1)
                else:
                    pygame.mixer.music.play()
                    self.set_volume(1)
            except pygame.error as e:
                print("Error loading music:", e)
        else:
            print("File not found")

    def stop(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

    def pause_unpause(self):
        if self._paused:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()

        self._paused = not self._paused
        return self._paused

    def set_volume(self, vol):
        pygame.mixer.music.set_volume(vol)

    def next_index(self, idx, max_idx):
        if idx >= max_idx:
            return 0
        return idx + 1

    def previous_index(self, idx):
        if idx <= 0:
            return 0
        return idx - 1

    def get_pg_postion(self):
        return int(pygame.mixer.music.get_pos() / 1000)

