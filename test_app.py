import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie

# assistant_token = "Bearer {}".format(os.environ.get('ASSISTANT_JWT'))
# director_token = "Bearer {}".format(os.environ.get('DIRECTOR_JWT'))
# producer_token = "Bearer {}".format(os.environ.get('PRODUCER_JWT'))
assistant_token = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJiQVg5clc2WXl2ckVoTzJpdmZBNyJ9.eyJpc3MiOiJodHRwczovL2NocmlzLWZzbmQuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmMzU0ZGY2OTU4MGRkMDA2ZDBhMjNiMyIsImF1ZCI6Ikhlcm9rdSIsImlhdCI6MTU5NzMyOTU5OSwiZXhwIjoxNTk3NDAxNTk5LCJhenAiOiJHMlJnNVlDSzJLUXVFbVpoQmVxWHF1czgzbzdyWlFYcCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.hweKh43FCITzylP5uwqjUKgzEmRAiDaMz20DiyTYP2y37xcjUeiRaKWWDGsv36-PsCBJr2wbLzg8I-MzS6YQkINCnmNODUctkKd-ZAaFpS5BRvUs9Mwv1T0u45WlklAKxQqX6PQ8lsmRVSi2BYbe-ghlK0WaVewTMQGaGhXaG56Aidv6aMQq9WHTBZTvcG2zzJksP5OGv4tUlB5-qGvePk6w1ujooMYOxyzd1joJuphZtUSLkuz4hAVf9_64X4spCWjqtk5HW0f05fQKGws3rSVX55HiPCBf7oEFVqP6KeMihl3yvFpp9YK6LY7GF1JVTXjoAWm_k9zwupfxht-4cQ"
director_token = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJiQVg5clc2WXl2ckVoTzJpdmZBNyJ9.eyJpc3MiOiJodHRwczovL2NocmlzLWZzbmQuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmMTljMGJmYzVhNTg1MDAxOWIyZGI0NiIsImF1ZCI6Ikhlcm9rdSIsImlhdCI6MTU5NzMzMjcwOSwiZXhwIjoxNTk3NDA0NzA5LCJhenAiOiJHMlJnNVlDSzJLUXVFbVpoQmVxWHF1czgzbzdyWlFYcCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.j5CgJXiead7K8p7-VUmoGD6RBAAmqSf5eEAtZVzyXO7y4zz8_Cd3y293n6wsju-p6_oUSTjL8VfEuc5eHR5AvENHPUXabKcMJ-LY8VL-TLNqYyJDMwYxSIIEqI0cQ3wqLEQmxKfAPw2KDbUiRU8tWUR718GI0ov08lgp7hyo5b-M_-eoGUxpXkDk6cQnNwNRpzPxm2d1VqcVDTUJ25VVj8EciaNq9JyLK6ffEbXfuS9Vp_kdbvqVc7SJFSxvSq8nr0vZBHZ8Qh80uJIp0jqnzLFGR57bnXhy3Fd6ABpuyRO-O5l2WvpBs7yib2fYm4Kan8bl1CU4mN_4PsHS-7FmYQ"
producer_token = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJiQVg5clc2WXl2ckVoTzJpdmZBNyJ9.eyJpc3MiOiJodHRwczovL2NocmlzLWZzbmQuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmMTE2ZGY2MWJhOGYzMDAxOWIzYjI5ZCIsImF1ZCI6Ikhlcm9rdSIsImlhdCI6MTU5NzMzMjc1MywiZXhwIjoxNTk3NDA0NzUzLCJhenAiOiJHMlJnNVlDSzJLUXVFbVpoQmVxWHF1czgzbzdyWlFYcCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.A2YKLw4PbLEN3-XlaHXlDVoS3vR5omWj6IsaO612G11kJAZRWFfy8urifxW14eZE3_UbpceQhwSaz69QfVmSxeGobJT2dVn6vB8C39KXdJE-EXPV11vlCksgzrP4ueTpScbJnDEx3MuvjftYVa3hmn3ChcOrMT0XkFtGhOY0D7dsc0TX1yCavfCAiShnjTaW2UyrdhAj2fmTBRoFyjg1g_hNpRfVklZ3AkYq_awiwQNei4PURGatYnUttbG6kaKLcY3wPIuEoFYYnOFt_uV9W0VSXTh9xC0sZEK3Boa9PwmHJ6B3QiHEp-h4h-xfDKBeD5uIQ3x6E2AJdPHdTT6UCg"

class CastingAgencyTestCase(unittest.TestCase):
  """This class represents the Casting Agency test case"""

  def setUp(self):
    """Define test variables and initialize app."""
    self.app = create_app()
    self.client = self.app.test_client
    self.database_name = "casting_test"
    self.database_path = "postgres://{}/{}".format('chris:admin@localhost:5432', self.database_name)
    setup_db(self.app, self.database_path)

    self.new_actor = {
      'name': 'Keanu Reeves',
      'age': 55,
      'gender': 'Male'
    }

    self.new_actor_2 = {
      'name': 'Brad Pitt',
      'age': 56,
      'gender': 'Male'
    }

    self.update_actor = {
      'name': 'Natalie Portman',
      'age': 39,
      'gender': 'Female'
    }

    self.new_movie = {
      'title': 'Eternal Sunshine of the Spotless Mind',
      'release_date': '2004-04-30 00:00'
    }

    self.new_movie_2 = {
      'title': 'John Wick',
      'release_date': '2015-04-10 00:50'
    }

    self.update_movie = {
      'title': 'Spirited Away',
      'release_date': '2003-09-12 01:45'
    }

    # binds the app to the current context
    with self.app.app_context():
      self.db = SQLAlchemy()
      self.db.init_app(self.app)
      # create all tables
      self.db.create_all()

  def tearDown(self):
    """Executed after reach test"""
    pass

  #  Success behavior

  def test_get_actors (self):
    res = self.client().get('/actors', headers={ "Authorization": ( assistant_token ) })
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertTrue(data['success'])
    self.assertTrue(len(data['actors']) >= 0)

  def test_get_movies (self):
    res = self.client().get('/movies', headers={ "Authorization": ( assistant_token ) })
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertTrue(data['success'])
    self.assertTrue(len(data['movies']) >= 0)

  def test_create_actors (self):
    res = self.client().post('/actors', json=self.new_actor, headers={ "Authorization": ( director_token ) })
    data = json.loads(res.data)

    self.assertTrue(data['success'])
    self.assertTrue(len(data['actors']) == 1)

  def test_create_movies (self):
    res = self.client().post('/movies', json=self.new_movie, headers={ "Authorization": ( producer_token ) })
    data = json.loads(res.data)

    self.assertTrue(data['success'])
    self.assertTrue(len(data['movies']) == 1)

  def test_update_actors (self):
    self.client().post('/actors', json=self.new_actor, headers={ "Authorization": ( producer_token ) })
    res = self.client().patch('/actors/1', json=self.update_actor, headers={ "Authorization": ( producer_token ) })
    data = json.loads(res.data)

    self.assertTrue(data['success'])
    self.assertTrue(len(data['actors']) == 1)

  def test_update_movies (self):
    self.client().post('/movies', json=self.new_movie, headers={ "Authorization": ( director_token ) })
    res = self.client().patch('/movies/1', json=self.update_movie, headers={ "Authorization": ( director_token ) })
    data = json.loads(res.data)

    self.assertTrue(data['success'])
    self.assertTrue(len(data['movies']) == 1)

  def test_delete_actors (self):
    self.client().post('/actors', json=self.new_actor, headers={ "Authorization": ( producer_token ) })
    self.client().post('/actors', json=self.new_actor_2, headers={ "Authorization": ( producer_token ) })
    res = self.client().delete('/actors/2', headers={ "Authorization": ( producer_token ) })
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['delete'], '2')
    self.assertTrue(data['success'])

  def test_delete_movies (self):
    self.client().post('/movies', json=self.new_movie, headers={ "Authorization": ( producer_token ) })
    self.client().post('/movies', json=self.new_movie_2, headers={ "Authorization": ( producer_token ) })
    res = self.client().delete('/movies/2', headers={ "Authorization": ( producer_token ) })
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['delete'], '2')
    self.assertTrue(data['success'])

  #  Error behavior

  def test_401_get_actors (self):
    res = self.client().get('/actors')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 401)
    self.assertFalse(data['success'])

  def test_401_get_movies (self):
    res = self.client().get('/movies')
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 401)
    self.assertFalse(data['success'])
  
  def test_401_create_actors (self):
    res = self.client().post('/actors', json=self.new_actor)
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 401)
    self.assertFalse(data['success'])

  def test_401_create_movies (self):
    res = self.client().post('/movies', json=self.new_movie)
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 401)
    self.assertFalse(data['success'])

  def test_404_update_actors (self):
    res = self.client().patch('/actors/1000', json=self.update_actor, headers={ "Authorization": ( producer_token ) })
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 404)
    self.assertFalse(data['success'])

  def test_404_update_movies (self):
    res = self.client().patch('/movies/1000', json=self.update_movie, headers={ "Authorization": ( producer_token ) })
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 404)
    self.assertFalse(data['success'])
  
  def test_404_delete_actors (self):
    res = self.client().delete('/actors/1000', headers={ "Authorization": ( producer_token ) })
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 404)
    self.assertFalse(data['success'])
  
  def test_404_delete_movies (self):
    res = self.client().delete('/movies/1000', headers={ "Authorization": ( producer_token ) })
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 404)
    self.assertFalse(data['success'])

# Make the tests conveniently executable
if __name__ == "__main__":
  unittest.main()
