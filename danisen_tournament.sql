CREATE TABLE IF NOT EXISTS entrants (
    id INT AUTO_INCREMENT PRIMARY KEY,
    player_name VARCHAR(255) NOT NULL,
    character_name VARCHAR(255) NOT NULL,
    rank INT DEFAULT 1,
    points INT DEFAULT 0,
    wins INT DEFAULT 0,
    losses INT DEFAULT 0,
    win_streak INT DEFAULT 0,
    loss_streak INT DEFAULT 0,
    max_win_streak INT DEFAULT 0,
    max_loss_streak INT DEFAULT 0,
    UNIQUE (player_name, character_name)  -- Prevent duplicate entries for the same character
);

CREATE TABLE IF NOT EXISTS matches (
    id INT AUTO_INCREMENT PRIMARY KEY,
    entrant1_id INT,
    entrant2_id INT,
    winner_id INT,
    loser_id INT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (entrant1_id) REFERENCES entrants(id),
    FOREIGN KEY (entrant2_id) REFERENCES entrants(id),
    FOREIGN KEY (winner_id) REFERENCES entrants(id),
    FOREIGN KEY (loser_id) REFERENCES entrants(id)
);
