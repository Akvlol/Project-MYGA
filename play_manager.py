#------------------------------------------------------------------------------
# Node
#------------------------------------------------------------------------------
class Node:
    def __init__(self, song_index):
        self.data = song_index
        self.next = None
        self.prev = None

#------------------------------------------------------------------------------
# PlaybackList
#------------------------------------------------------------------------------
class PlaybackList:
    def __init__(self):
        self.head = None
        self.current = None
        self.size = 0

    def append(self, song_index):

        new_node = Node(song_index)

        if not self.head:
            self.head = new_node

            self.head.next = new_node
            self.head.prev = new_node

            self.current = new_node

        else:
            tail = self.head.prev

            tail.next = new_node

            new_node.prev = tail
            new_node.next = self.head

            self.head.prev = new_node

        self.size += 1

    def next(self):
        if self.current:
            self.current = self.current.next
            return self.current
        return None

    def prev(self):
        if self.current:
            self.current = self.current.prev
            return self.current
        return None

    def jump_to(self, song_index):
        node = self.head
        for _ in range(self.size):
            if node.data == song_index:
                self.current = node
                return node
            node = node.next
        return None

    def clear(self):
        self.head = self.current = None
        self.size = 0


#------------------------------------------------------------------------------
# PlaybackManager
#------------------------------------------------------------------------------
from tool.input_tool import InputTool
from cdp import ChromiumDevTools
from browser_manager import Browser
import threading
import time

class PlaybackManager:
    
    def __init__(self, playlist=None):
        self.playlist = playlist
        self.playback_list = PlaybackList()
        self.player = ChromiumDevTools()
        self.browser = Browser()

        self.running = False
        self.monitor_thread = None

    # --------------------------------------------------
    # Shuffle playlist
    # --------------------------------------------------
    def shuffle(self):
        import random

        self.playback_list.clear()

        indices = list(range(len(self.playlist.songs)))
        random.shuffle(indices)

        for index in indices:
            self.playback_list.append(index)

    # --------------------------------------------------
    # Monitor video, NEXT song if ENDED
    # --------------------------------------------------
    def _monitor_video(self):
        while self.running:

            if self.player.is_ended():
                self.next()
                print()
                current_song_name = self.get_current_song().title.split(" - ")[0]
                print(f"<playing: {current_song_name} ># " if len(current_song_name) < 36 
                      else f"<playing: {current_song_name[:33]}... ># ", end="", flush=True)

            time.sleep(0.5)
    
    # --------------------------------------------------
    # Start playback
    # --------------------------------------------------
    def start(self):
        self.browser.start()
        self.player.connect()
        self.shuffle()

        if InputTool.yes_or_no("Play a random song?"):
            self.get_current_song()
            self.play()
        else:
            self.jump_to()

        self.running = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_video,
            daemon=True
        )

        self.monitor_thread.start()

    # --------------------------------------------------
    # Stop playback    
    # --------------------------------------------------
    def stop(self):
        self.running = False
        self.player.disconnect()
        self.browser.stop()
    
    # --------------------------------------------------
    # Get current song    
    # --------------------------------------------------
    def get_current_song(self):
        if self.playback_list.current is None:
            return None
        index = self.playback_list.current.data
        return self.playlist.songs[index]

    # --------------------------------------------------
    # Get next song    
    # --------------------------------------------------
    def next(self):
        node = self.playback_list.next()

        if node is None:
            return None

        self.play()

    # --------------------------------------------------
    # Get previous song    
    # --------------------------------------------------
    def previous(self):
        node = self.playback_list.prev()

        if node is None:
            return None

        self.play()     

    # --------------------------------------------------
    # Jump to a specific song
    # --------------------------------------------------
    def jump_to(self):
        self.playlist.display_songs()
        if InputTool.yes_or_no("Find song?"):
            while True:
                self.playlist.find_song()
                if InputTool.yes_or_no("Satisfied?"):
                    break

        song_index = InputTool.valid_int("Song (index)?",0 , len(self.playlist.songs) - 1)

        node = self.playback_list.jump_to(song_index)

        if node is None:
            return None

        self.play()

    # --------------------------------------------------
    # Play the song
    # --------------------------------------------------
    def play(self):
        self.player.load(
            f"https://www.youtube.com/watch?v={self.get_current_song().id}"
        )

    # --------------------------------------------------
    # Play/Pause
    # --------------------------------------------------
    def play_pause(self):
        if self.player.is_playing():
            self.player.pause()
        else:
            self.player.play()

    # --------------------------------------------------
    # Get current song info
    # --------------------------------------------------
    def get_current_song_info(self):
        self.playlist.display_song_info(self.get_current_song().id)