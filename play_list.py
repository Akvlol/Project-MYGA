import json
import os
from tool.input_tool import InputTool

#------------------------------------------------------------------------------
# Song
#------------------------------------------------------------------------------
class Song:
    def __init__(self, title, id):
        self.title = title
        self.id = id

#------------------------------------------------------------------------------
# Playlist
#------------------------------------------------------------------------------
class Playlist:
    def __init__(self):
        self.songs = []
    #--------------------------------------------------
    # Display songs
    #--------------------------------------------------
    def display_songs(self, with_url=False):
        if with_url == False:
            for index, song in enumerate(self.songs):
                print(f"[{index}] {song.title}")
        else:
            for index, song in enumerate(self.songs):
                print(f"\n[{index}] {song.title} - https://www.youtube.com/watch?v={song.id}\n")

    #--------------------------------------------------    
    # Display song info
    #--------------------------------------------------
    def display_song_info(self, song_id):
        for index, song in enumerate(self.songs):
            if song.id == song_id:
                print(f'''
                Index: {index}
                Title: {song.title}
                Link: https://www.youtube.com/watch?v={song.id}
''')
                return
        print("Song not found.")

    #--------------------------------------------------
    # Add song
    #--------------------------------------------------
    def add_song(self):

        is_add_many = True
        is_added_once = False
        many_add_confirm = False

        while is_add_many:

            #URL to id
            while True:
                url = InputTool.empty_is_none("URL: ")

                if url is None:
                    if InputTool.yes_or_no("Stop adding song?"):
                        print()
                        return False or is_added_once
                    else:
                        continue
                id = None
                if url.startswith("https://www.youtube.com/watch?v="):
                    id = url.split("www.youtube.com/watch?v=")[1].split("&list=")[0]
                elif url.startswith("https://youtu.be/"):
                    id = url.split("youtu.be/")[1].split("?")[0]

                #if cant get title, ask for new URL
                title = InputTool.get_youtube_title(id)
                if title is None:
                    print("Invalid URL.")
                    continue
                
                if not InputTool.is_duplicate(id, [song.id for song in self.songs]):
                    break

            #Change title if needed
            if not InputTool.yes_or_no(f'\nKeep title: "{title}" ?'):
                while True:
                    title = InputTool.empty_is_none("\nTitle: ")
                    if title is None:
                        if InputTool.yes_or_no("Stop adding song?"):
                            print()
                            return False or is_added_once
                        else:
                            continue
                    if not InputTool.is_duplicate(title, [song.title for song in self.songs]):
                        break

            #Add song to playlist
            self.songs.append(Song(title, id))
            print(f"\nAdded: {title} - https://www.youtube.com/watch?v={id}\n")
            is_added_once = True

            #Continue if adding multiple songs mode is confirmed
            if many_add_confirm:
                continue

            #If adding multiple songs mode is not confirmed, ask for confirmation
            if InputTool.yes_or_no("\nAdd more songs?"):
                many_add_confirm = True
            else:
                return True
            
    #--------------------------------------------------
    # Update song
    #--------------------------------------------------
    def update_song(self):

        #Return if no songs
        if not self.songs:
            print("No songs to update.\n")
            return False

        #Which song to update
        self.display_songs()
        index = InputTool.valid_int("Index: ", 0, len(self.songs) - 1)
        song = self.songs[index]
        print(f"\nUpdating: {song.title} https://www.youtube.com/watch?v={song.id}\n")

        new_id = song.id
        
        #New URL to new id
        while True:
            new_url = InputTool.empty_is_none("New URL: ")
            if new_url is None:
                break

            new_id = None
            if new_url.startswith("https://www.youtube.com/watch?v="):
                new_id = new_url.split("www.youtube.com/watch?v=")[1].split("&list=")[0]
            elif new_url.startswith("https://youtu.be/"):
                new_id = new_url.split("youtu.be/")[1].split("?")[0]

            new_title = InputTool.get_youtube_title(new_id)
            if new_title is None:
                print("Invalid URL.")
                continue

            if new_id == song.id:
                break
            
            if not InputTool.is_duplicate(new_id, [s.id for s in self.songs]):
                song.id = new_id
                break
        
        #New title
        while True:
            new_title = InputTool.empty_is_none("New Title: ")
            if new_title is None or (new_title == song.title):
                break
            elif not InputTool.is_duplicate(new_title, [s.title for s in self.songs]):
                song.title = new_title
                break

        #Return if no changes
        if new_id == song.id and new_title == song.title:
            return False

        #Update song
        print(f"\nUpdated: {song.title} - https://www.youtube.com/watch?v={song.id}\n")
        return True
    
    #--------------------------------------------------
    # Find song by substring
    #--------------------------------------------------
    def find_song(self):
        #Return if no songs
        if not self.songs:
            print("No songs to find.\n")
            return None

        #Find song
        substring = input("Song name: ")
        found = False
        print("\nFound: ", end="")
        for index, song in enumerate(self.songs):
            if substring.lower() in song.title.lower():
                if found == False:
                    found = True
                    print()
                print(f"\t[{index}] {song.title}")

        if found == False:
            print("None")

        print()

    #--------------------------------------------------
    # Delete song
    #--------------------------------------------------
    def delete_song(self):
        #Return if no songs
        if not self.songs:
            print("No songs to delete.\n")
            return False

        #Which song to delete
        self.display_songs()
        index = InputTool.valid_int("Index: ", 0, len(self.songs) - 1)
        song = self.songs[index]
        if InputTool.yes_or_no(f"Are you sure you want to delete '{song.title}'?"):
            if InputTool.yes_or_no("Are you really sure? This action cannot be undone."):
                del self.songs[index]
                print(f"\nDeleted: {song.title} - https://www.youtube.com/watch?v={song.id}\n")
                return True
        return False

    #--------------------------------------------------
    # Save playlist to JSON
    #--------------------------------------------------
    def save_playlist_to_json(self, file_path="data/playlist.json"):

        #Convert songs to Dict
        data = {
            "songs": [{"title": song.title, "id": song.id} for song in self.songs]
        }

        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base_dir, file_path)
        
        #Save to JSON
        with open(full_path, "w", encoding="utf-8") as f:
            # indent=4 giúp file JSON tự động xuống dòng và thụt lề đẹp mắt
            # ensure_ascii=False giữ nguyên tiếng Việt có dấu
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"Playlist saved to {file_path}\n")

    #--------------------------------------------------
    # Load playlist from JSON
    #--------------------------------------------------
    def load_playlist_from_json(self, file_path="data/playlist.json"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base_dir, file_path)

        #Return if no playlist
        if not os.path.exists(full_path):
            print(f"\nNo playlist found at {file_path}. Starting with an empty playlist.\n")
            return

        #Load from JSON
        with open(full_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.songs = [Song(song["title"], song["id"]) for song in data.get("songs", [])]

        print(f"\nPlaylist loaded from {file_path}\n")