import mysql.connector


# Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="your-un",
    password="your-pw"
)
cursor = db.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS danisen_tournament;")
cursor.close()
db.close()

# Now connect again with the correct DB
db = mysql.connector.connect(
    host="localhost",
    user="your-un",
    password="your-pw",
    database="danisen_tournament"
)
cursor = db.cursor()
# 🏆 Add a New Player
def add_player(player_name, character_name):
    # Assuming you already have a table with columns like: id, player_name, character_name, etc.
    cursor = db.cursor()
    query = "INSERT INTO entrants (player_name, character_name) VALUES (%s, %s)"
    cursor.execute(query, (player_name, character_name))
    db.commit()
    cursor.close()


# 🎮 Record a Match
def record_match(winner_name, winner_character, loser_name, loser_character):
    cursor = db.cursor()

    # Update winner
    update_winner = """
    UPDATE entrants
    SET wins = wins + 1,
        current_streak = CASE
            WHEN current_streak >= 0 THEN current_streak + 1
            ELSE 1
        END,
        longest_streak = GREATEST(longest_streak, 
            CASE
                WHEN current_streak >= 0 THEN current_streak + 1
                ELSE 1
            END)
    WHERE player_name = %s AND character_name = %s
    """
    cursor.execute(update_winner, (winner_name, winner_character))

    # Update loser
    update_loser = """
    UPDATE entrants
    SET losses = losses + 1,
        current_streak = CASE
            WHEN current_streak <= 0 THEN current_streak - 1
            ELSE -1
        END
    WHERE player_name = %s AND character_name = %s
    """
    cursor.execute(update_loser, (loser_name, loser_character))

    db.commit()
    cursor.close()


def update_points(winner, loser):
    cursor.execute("UPDATE players SET points = points + 2 WHERE id = %s", (winner,))
    cursor.execute("UPDATE players SET points = points - 1 WHERE id = %s", (loser,))
    
    # Check for rank-ups
    check_rank(winner)
    check_rank(loser)

def check_rank(player_id):
    cursor.execute("SELECT points, rank FROM players WHERE id = %s", (player_id,))
    points, rank = cursor.fetchone()

    if points >= 5:
        cursor.execute("UPDATE players SET rank = rank + 1, points = 0 WHERE id = %s", (player_id,))
    elif points <= -5 and rank > 1:
        cursor.execute("UPDATE players SET rank = rank - 1, points = 0 WHERE id = %s", (player_id,))
    
    db.commit()
# 📈 Update Streaks (Active & Historical)
def update_streaks(winner, loser):
    cursor.execute("SELECT win_streak, max_win_streak FROM players WHERE id = %s", (winner,))
    win_streak, max_win_streak = cursor.fetchone()

    cursor.execute("SELECT loss_streak, max_loss_streak FROM players WHERE id = %s", (loser,))
    loss_streak, max_loss_streak = cursor.fetchone()

    # Update streaks
    win_streak += 1
    loss_streak += 1

    # Update max streaks
    max_win_streak = max(win_streak, max_win_streak)
    max_loss_streak = max(loss_streak, max_loss_streak)

    # Commit streak updates
    cursor.execute("UPDATE players SET win_streak = %s, max_win_streak = %s WHERE id = %s", (win_streak, max_win_streak, winner))
    cursor.execute("UPDATE players SET loss_streak = %s, max_loss_streak = %s WHERE id = %s", (loss_streak, max_loss_streak, loser))

    db.commit()

# 🔝 Leaderboard Display
def get_leaderboard():
    cursor = db.cursor()
    query = """
    SELECT player_name, character_name, wins, losses, 
           ROUND((wins / NULLIF((wins + losses), 0)) * 100, 2) AS win_rate
    FROM entrants
    ORDER BY win_rate DESC, wins DESC
    """
    cursor.execute(query)
    leaderboard = cursor.fetchall()
    cursor.close()

    return leaderboard


# 🔥 Longest Historical Streaks
def get_top_historical_streaks():
    query = "SELECT name, max_win_streak FROM players ORDER BY max_win_streak DESC LIMIT 5"
    cursor.execute(query)
    results = cursor.fetchall()

    streaks = "🔥 **All-Time Longest Win Streaks** 🔥\n"
    for i, (name, streak) in enumerate(results, 1):
        streaks += f"{i}. {name} - {streak} Wins\n"

    return streaks

def get_all_players():
    cursor = db.cursor()
    query = "SELECT player_name, character_name FROM entrants ORDER BY player_name, character_name"
    cursor.execute(query)
    players = cursor.fetchall()
    cursor.close()
    
    return players
def clear_players():
    cursor = db.cursor()
    query = "DELETE FROM entrants"
    cursor.execute(query)
    db.commit()
    cursor.close()
    print("✅ All players have been cleared from the list.")
