import sqlite3

class GameDatabase:
    """Tietokantaa käsittelevä luokka."""
    def __init__(self, db_file="highscores.db"):
        """Alustaa tietokantayhteyden."""
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Luo tarvittavat taulut, jos niitä ei ole."""
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS high_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            difficulty TEXT,
            time REAL
        )
        ''')
        self.conn.commit()

    def save_score(self, difficulty, time_seconds):
        """Tallentaa uuden tuloksen, jos se on parempi kuin aiempi paras tulos.

        Args:
            difficulty: Vaikeustaso ("Easy", "Medium", "Hard")
            time_seconds: Peliaika sekunteina
        """
        self.cursor.execute(
            "SELECT time FROM high_scores WHERE difficulty = ? ORDER BY time ASC LIMIT 1",
            (difficulty,)
        )
        result = self.cursor.fetchone()

        if result is None or time_seconds < result[0]:
            self.cursor.execute("DELETE FROM high_scores WHERE difficulty = ?", (difficulty,))

            self.cursor.execute(
                "INSERT INTO high_scores (difficulty, time) VALUES (?, ?)",
                (difficulty, time_seconds)
            )
            self.conn.commit()

    def get_high_scores(self, difficulty, limit=1):
        """Hakee parhaat tulokset tietylle vaikeustasolle.

        Args:
            difficulty: Vaikeustaso ("Easy", "Medium", "Hard")
            limit: Palautettavien tulosten maksimimäärä

        Returns:
            Lista tupleja (time)
        """
        self.cursor.execute(
            "SELECT time FROM high_scores WHERE difficulty = ? ORDER BY time ASC LIMIT ?",
            (difficulty, limit)
        )
        return self.cursor.fetchall()

    def close(self):
        """Sulkee tietokantayhteyden."""
        if self.conn:
            self.conn.close()