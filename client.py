import sys
from danisen import add_player, record_match, get_leaderboard, get_top_historical_streaks

def main_menu():
    while True:
        print("\n🏆 Danisen Tournament Bot 🏆")
        print("1. Add Entrant (Player + Character)")
        print("2. Record Match")
        print("3. Show Leaderboard")
        print("4. Show Longest Historical Streaks")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            player_name = input("Enter player name: ").strip()
            character_name = input("Enter character name: ").strip()
            add_player(player_name, character_name)
            print(f"✅ {player_name} ({character_name}) added to the tournament!")

        elif choice == "2":
            try:
                entrant1 = int(input("Enter Entrant 1 ID: ").strip())
                entrant2 = int(input("Enter Entrant 2 ID: ").strip())
                winner = int(input("Enter Winner ID: ").strip())

                if winner not in [entrant1, entrant2]:
                    print("❌ Invalid winner ID. Must be one of the entrants.")
                    continue

                record_match(entrant1, entrant2, winner)
                print(f"✅ Match recorded! Entrant {winner} won!")

            except ValueError:
                print("❌ Invalid input. Please enter numbers for entrant IDs.")

        elif choice == "3":
            print("\n" + get_leaderboard())

        elif choice == "4":
            print("\n" + get_top_historical_streaks())

        elif choice == "5":
            print("👋 Exiting Danisen Bot. See you next time!")
            sys.exit()

        else:
            print("❌ Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main_menu()
