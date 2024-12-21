import json
from django.test import TestCase, Client
from django.urls import reverse
from .models import AppUser, Hobby, AppUserHobby

class SimilarUsersTestCase(TestCase):
    def setUp(self):
        """
        Set up test data for AppUser model.
        """
        self.client = Client()

        # Create test hobbies
        reading = Hobby.objects.create(hobby_name="reading")
        cycling = Hobby.objects.create(hobby_name="cycling")
        movies = Hobby.objects.create(hobby_name="movies")
        gaming = Hobby.objects.create(hobby_name="gaming")
        cooking = Hobby.objects.create(hobby_name="cooking")
        traveling = Hobby.objects.create(hobby_name="traveling")

       # Create users
        alice = AppUser.objects.create(username="Alice", password="password", date_of_birth="2001-01-01")
        bob = AppUser.objects.create(username="Bob", password="word", date_of_birth="1990-01-01")
        charlie = AppUser.objects.create(username="Charlie", password="pa3462", date_of_birth="2003-05-23")
        david = AppUser.objects.create(username="David", password="paahherhord", date_of_birth="1998-08-02")
        eve = AppUser.objects.create(username="Eve", password="pa6gae4word", date_of_birth="2004-04-04")

        # Assign hobbies to users using the through model
        AppUserHobby.objects.create(appUser=alice, hobby=reading, date_started="2020-01-01", level_of_expertise="Intermediate")
        AppUserHobby.objects.create(appUser=alice, hobby=cycling, date_started="2019-06-15", level_of_expertise="Beginner")
        AppUserHobby.objects.create(appUser=alice, hobby=movies, date_started="2021-03-10", level_of_expertise="Advanced")

        AppUserHobby.objects.create(appUser=bob, hobby=cycling, date_started="2018-07-20", level_of_expertise="Advanced")
        AppUserHobby.objects.create(appUser=bob, hobby=gaming, date_started="2020-12-01", level_of_expertise="Intermediate")
        AppUserHobby.objects.create(appUser=bob, hobby=movies, date_started="2017-11-05", level_of_expertise="Advanced")

        AppUserHobby.objects.create(appUser=charlie, hobby=reading, date_started="2022-01-15", level_of_expertise="Beginner")
        AppUserHobby.objects.create(appUser=charlie, hobby=traveling, date_started="2021-09-10", level_of_expertise="Intermediate")

        AppUserHobby.objects.create(appUser=david, hobby=movies, date_started="2015-04-25", level_of_expertise="Advanced")
        AppUserHobby.objects.create(appUser=david, hobby=cooking, date_started="2019-10-12", level_of_expertise="Beginner")
        AppUserHobby.objects.create(appUser=david, hobby=gaming, date_started="2020-06-01", level_of_expertise="Intermediate")

        AppUserHobby.objects.create(appUser=eve, hobby=reading, date_started="2018-03-14", level_of_expertise="Advanced")
        AppUserHobby.objects.create(appUser=eve, hobby=movies, date_started="2016-08-20", level_of_expertise="Intermediate")
        AppUserHobby.objects.create(appUser=eve, hobby=cooking, date_started="2021-05-30", level_of_expertise="Beginner")

        # Store Alice for login
        self.alice = alice

    def test_similar_users_returns_correct_users_and_num_of_hobbies(self):
        """
        Test that the similar_users function returns correct frequency of common hobbies.
        """
        # Log in as Alice
        self.client.force_login(self.alice)

        # Call the view
        response = self.client.get(reverse('similar-users'))
        self.assertEqual(response.status_code, 200)

        # Load the JSON response
        response_data = json.loads(response.content)

        # Expected pairs and counts
        expected_output = {
            "2": [
                {"username": "Bob", "hobbies": ["cycling", "gaming", "movies"]},
                {"username": "Eve", "hobbies": ["reading", "movies", "cooking"]},
            ],
            "1": [
                {"username": "Charlie", "hobbies": ["reading", "traveling"]},
                {"username": "David", "hobbies": ["movies", "cooking", "gaming"]},
            ],
        }

        # Compare expected and actual output
        self.assertEqual(response_data, expected_output)

    # def test_no_duplicates_in_pairs(self):
    #     """
    #     Test that no duplicate pairs (e.g., Alice-Bob and Bob-Alice) are returned.
    #     """
    #     response = self.client.get(reverse('similar-users/'))
    #     self.assertEqual(response.status_code, 200)

    #     # Load response
    #     response_data = json.loads(json.loads(response.content))

    #     # Collect all user pairs into a set for validation
    #     seen_pairs = set()
    #     for count, pairs in response_data.items():
    #         for pair in pairs:
    #             # Create a frozenset of user names to ensure uniqueness
    #             user_pair = frozenset([pair[0]["name"], pair[1]["name"]])
    #             self.assertNotIn(user_pair, seen_pairs)  # Ensure no duplicates
    #             seen_pairs.add(user_pair)

    # def test_empty_user_list(self):
    #     """
    #     Test that the function handles an empty user list correctly.
    #     """
    #     AppUser.objects.all().delete()  # Clear all users

    #     response = self.client.get(reverse('similar-users/'))
    #     self.assertEqual(response.status_code, 200)

    #     # Load response
    #     response_data = json.loads(json.loads(response.content))
    #     self.assertEqual(response_data, {})  # Expecting empty dictionary

    # def test_single_user(self):
    #     """
    #     Test that the function handles a single user correctly (no pairs).
    #     """
    #     AppUser.objects.all().delete()
    #     AppUser.objects.create(name="Alice", hobbies=["reading", "cycling", "movies"])

    #     response = self.client.get(reverse('similar-users/'))
    #     self.assertEqual(response.status_code, 200)

    #     # Load response
    #     response_data = json.loads(json.loads(response.content))
    #     self.assertEqual(response_data, {})  # No pairs to compare
