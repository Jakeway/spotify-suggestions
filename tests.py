import unittest
import os
from app import app, db


class SpotifyTestCase(unittest.TestCase):

    def setUp(self):
        app.config.from_object(os.environ['APP_SETTINGS'])
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    unittest.main()
