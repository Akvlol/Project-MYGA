from play_list import Playlist
from play_manager import PlaybackManager
from tool.input_tool import InputTool
import subprocess
import platform

#------------------------------------------------------------------------------
# Edit mode
#------------------------------------------------------------------------------
def print_menu_edit():
    print("""
Edit mode:
[h] - Display this help menu
[d] - Display all songs
 |-[D] - Display all songs with URL
[f] - Find song by substring
[a] - Add a new song
[u] - Update an existing song
[x] - Delete a song
[s] - Save the playlist to a file
[clear] - Clear the screen
[exit] - Back to the main menu
""")
def edit_playlist(playlist):
    print_menu_edit()
    changes_made = False
    while True:
        choice = InputTool.valid_value("<edit># ", ['h','f', 'a', 'd', 'D', 'u', 'x', 's', 'clear', 'exit'], "Invalid choice. Press 'h' for help.\n")
        match choice:
            case 'h':
                print_menu_edit()
            case 'a':
                changes_made = playlist.add_song() or changes_made
            case 'f':
                playlist.find_song()
            case 'd':
                playlist.display_songs()
            case 'D':
                playlist.display_songs(with_url=True)
            case 'u':
                changes_made = playlist.update_song() or changes_made
            case 'x':
                changes_made = playlist.delete_song() or changes_made
            case 's':
                playlist.save_playlist_to_json()
                changes_made = False
            case 'clear':
                subprocess.run('cls' if platform.system() == 'Windows' else 'clear', shell=True)
            case 'exit':
                if changes_made:
                    if InputTool.yes_or_no("Save before quitting?"):
                        playlist.save_playlist_to_json()
                        print("Changes saved.\n")
                    else:
                        print("\nChanges NOT saved.\n")
                else:
                    print()
                break

#------------------------------------------------------------------------------
# Play mode
#------------------------------------------------------------------------------
def print_menu_play():
    print("""
Play mode:
[h] - Display this help menu
[s] - Shuffle the playlist and Start playing
[z] - Jump to a specific song by index
[x] - Play/Pause
[n] - Play the next song
[p] - Play the previous song
[g] - Get current song info
[clear] - Clear the screen
[exit] - Stop & back to the main menu
""")
def play_playlist(manager):
    manager.start()
    while True:
        song_name = manager.get_current_song().title.split(" - ")[0]
        choice = InputTool.valid_value(f"<playing: {song_name} ># " if len(song_name) < 36 else f"<playing: {song_name[:33]}... ># ",
                                       ['h', 's', 'z', 'n', 'p', 'x', 'g', 'exit', 'clear'],
                                       "Invalid choice. Press 'h' for help.\n",
                                       continue_if_empty=False)
        if choice == "":
            continue

        match choice:
            case 'h':
                print_menu_play()
            case 's':
                manager.shuffle()
            case 'z':
                manager.jump_to()
            case 'x':
                manager.play_pause()
            case 'n':
                manager.next()
            case 'p':
                manager.previous()
            case 'g':
                manager.get_current_song_info()
            case 'clear':
                subprocess.run('cls' if platform.system() == 'Windows' else 'clear', shell=True)
            case 'exit':
                manager.stop()
                print()
                break

#------------------------------------------------------------------------------
# Main
#------------------------------------------------------------------------------
def main():
    playlist = Playlist()
    playlist.load_playlist_from_json()
    manager = PlaybackManager(playlist)
    while True:    
        print("""Main menu:
[e] - Edit the playlist
[p] - Play the playlist
[clear] - Clear the screen
[quit] - Quit the program
""")
        choice = InputTool.valid_value("<main># ", ['e', 'p', 'clear', 'quit'], "Invalid choice. Please enter 'e', 'p', or 'quit'.\n")
        match choice:
            case 'e':
                edit_playlist(playlist)
            case 'p':
                play_playlist(manager)
            case 'clear':
                subprocess.run('cls' if platform.system() == 'Windows' else 'clear', shell=True)
            case 'quit':
                if InputTool.yes_or_no("Quit?"):
                    print("Exiting the program.")
                    break

#------------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        manager = PlaybackManager()
        manager.stop()
        print("\nForcefully exiting the program.")