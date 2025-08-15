import subprocess
import sys

games = {
    '1': ('Pong', 'pong.py'),
    '2': ('Tetris', 'tetris.py'),
    '3': ('Snake', 'snake.py'),
    '4': ('Minesweeper', 'minesweeper.py'),
    'q': ('Quit', None)
}

def main():
    while True:
        print("=== Game Launcher ===")
        for key, (name, _) in games.items():
            print(f"{key}: {name}")
        choice = input("Select a game to play: ").strip()
        if choice == 'q':
            print("Goodbye!")
            sys.exit(0)
        elif choice in games:
            _, script = games[choice]
            if script:
                subprocess.run([sys.executable, script])
        else:
            print("Invalid choice, try again.\n")

if __name__ == "__main__":
    main()
