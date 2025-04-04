import mysql.connector


# Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="your_user",
    password="your_password",
    database="danisen_tournament"
)
cursor = db.cursor()

# 🏆 Add a New Player
def add_player(name):
    try:
        query = "INSERT INTO players (name) VALUES (%s)"
        cursor.execute(query, (name,))
        db.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# 🎮 Record a Match
def record_match(player1, player2, winner):
    loser = player2 if winner == player1 else player1

    # Insert match record
    query = "INSERT INTO matches (player1_id, player2_id, winner_id, loser_id) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (player1, player2, winner, loser))

    # Update win/loss records
    cursor.execute("UPDATE players SET wins = wins + 1 WHERE id = %s", (winner,))
    cursor.execute("UPDATE players SET losses = losses + 1 WHERE id = %s", (loser,))

    # Update points and ranks
    update_points(winner, loser)
    
    # Update win/loss streaks
    update_streaks(winner, loser)
    
    db.commit()

def update_points(winner, loser):
    cursor.execute("UPDATE players SET points = points + 2 WHERE id = %s", (winner,))
    cursor.execute("UPDATE players SET points = points - 1 WHERE id = %s", (loser,))
    
    # Check for rank-ups
    check_rank(winner)
    check_rank(loser)

def check_rank(player_id):
    cursor.execute("SELECT points, rank FROM players WHERE id = %s", (player_id,))
    points, rank = cursor.fetchone()

    if points >= 10:
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
    query = """
    SELECT name, rank, points, wins, losses, win_streak, 
           ROUND((wins / NULLIF((wins + losses), 0)) * 100, 2) AS win_rate
    FROM players
    ORDER BY rank DESC, points DESC, win_rate DESC, wins DESC
    LIMIT 10;
    """
    cursor.execute(query)
    results = cursor.fetchall()

    leaderboard = "🏆 **Danisen Leaderboard** 🏆\n"
    for i, (name, rank, points, wins, losses, win_streak, win_rate) in enumerate(results, 1):
        leaderboard += f"{i}. {name} - Rank {rank}, {points} pts, {wins}W-{losses}L, {win_streak} WS ({win_rate}% WR)\n"

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
