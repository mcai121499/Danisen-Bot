import sys
from danisen import add_player, record_match, get_leaderboard, get_top_historical_streaks, get_all_players, clear_players

def main_menu():
    while True:
        print("\n=== Danisen Tournament Bot ===")
        print("1. Add Player")
        print("2. Record Match")
        print("3. Show Leaderboard")
        print("4. Show Full Player List")
        print("5. Clear Player List")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            player_name = input("Enter player name: ").strip()
            character_name = input("Enter character name: ").strip()
            add_player(player_name, character_name)
            print(f"> {player_name} ({character_name}) added successfully!")

        elif choice == "2":
            winner = input("Enter winner's name: ")
            winner_character = input("Enter winner's character: ")
            loser = input("Enter loser's name: ")
            loser_character = input("Enter loser's character: ")
            record_match(winner, winner_character, loser, loser_character)
            print("Match recorded successfully!")

        elif choice == "3":
            leaderboard = get_leaderboard()
            print("\nLeaderboard:")
            for player in leaderboard:
                print(f"{player[0]} ({player[1]}): {player[2]} wins, {player[3]} losses, {player[4]}% win rate")


        elif choice == "4":
            players = get_all_players()
            print("\nFull Player List:")
            for player in players:
                print(f"{player[0]} ({player[1]})")

        elif choice == "5":
            confirmation = input("Are you sure you want to clear the player list? (Y/N): ").strip().lower()
            if confirmation == "Y":
                clear_players()
            else:
                print("Clearing player list canceled.")

        elif choice == "6":
            print("Exiting...")
            break
        
        else:
            print("! Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main_menu()
