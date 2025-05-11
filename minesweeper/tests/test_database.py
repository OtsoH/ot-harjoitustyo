import unittest
from database import GameDatabase

class TestGameDatabase(unittest.TestCase):

    def setUp(self):
        self.db = GameDatabase(":memory:")

    def tearDown(self):
        self.db.close()

    def test_initialization(self):
        # Checking that highscores-table is created
        self.db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='high_scores'")
        result = self.db.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "high_scores")

        self.db.cursor.execute("PRAGMA table_info(high_scores)")
        columns = self.db.cursor.fetchall()
        self.assertEqual(len(columns), 3)

        column_names = [column[1] for column in columns]
        self.assertIn("id", column_names)
        self.assertIn("difficulty", column_names)
        self.assertIn("time", column_names)

    def test_save_score_new_record(self):
        # Testing that a new score is saved correctly
        self.db.save_score("Easy", 100)
        self.db.cursor.execute("SELECT difficulty, time FROM high_scores WHERE difficulty = 'Easy'")
        result = self.db.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "Easy")
        self.assertEqual(result[1], 100)

    def test_save_score_better_time(self):
        #Testing that a better score replaces the old one
        self.db.save_score("Medium", 101.0)
        self.db.save_score("Medium", 100.0)

        self.db.cursor.execute("SELECT COUNT(*), MIN(time) FROM high_scores WHERE difficulty = 'Medium'")
        result = self.db.cursor.fetchone()
        self.assertEqual(result[0], 1)
        self.assertEqual(result[1], 100.0)

    def test_save_score_worse_time(self):
        #Testing that a worse score does not replace the old one
        self.db.save_score("Hard", 100.0)
        self.db.save_score("Hard", 101.0)

        self.db.cursor.execute("SELECT COUNT(*), MIN(time) FROM high_scores WHERE difficulty = 'Hard'")
        result = self.db.cursor.fetchone()
        self.assertEqual(result[0], 1)
        self.assertEqual(result[1], 100.0)


