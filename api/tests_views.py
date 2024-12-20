import json
from django.test import TestCase, Client
from django.urls import reverse
from .models import AppUser, Hobby

class SimilarUsersTestCase(TestCase):
    def setUp(self):
        """
        Set up test data for AppUser model.
        """
        self.client = Client()

        # Create test users with hobbies
        AppUser.objects.create(username="Alice", hobbies=["reading", "cycling", "movies"])
        AppUser.objects.create(username="Bob", hobbies=["cycling", "gaming", "movies"])
        AppUser.objects.create(username="Charlie", hobbies=["reading", "traveling"])
        AppUser.objects.create(username="David", hobbies=["movies", "cooking", "gaming"])
        AppUser.objects.create(username="Eve", hobbies=["reading", "movies", "cooking"])

        Hobby.objects.create(appUser=AppUser.objects.get(username="Alice"), hobby_name="reading")

    def test_similar_users_functionality(self):
        """
        Test that the similar_users function returns correct frequency of common hobbies.
        """
        response = self.client.get(reverse('similar-users/'))  # URL name is 'similar-users/'
        self.assertEqual(response.status_code, 200)

        # Load the JSON response
        response_data = json.loads(json.loads(response.content))
        print(response_data)

        # Check that the output contains correct frequencies
        # Expected pairs:
        # Alice & Bob -> 2 common hobbies (cycling, movies)
        # Alice & Eve -> 2 common hobbies (reading, movies)
        # Bob & David -> 2 common hobbies (movies, gaming)
        # Alice & Charlie -> 1 common hobby (reading)
        # Charlie & Eve -> 1 common hobby (reading)
        # David & Eve -> 1 common hobby (movies)
        expected_output = {
            "2": [
                [{"name": "Alice", "hobbies": ["reading", "cycling", "movies"]},
                 {"name": "Bob", "hobbies": ["cycling", "gaming", "movies"]}],
                [{"name": "Alice", "hobbies": ["reading", "cycling", "movies"]},
                 {"name": "Eve", "hobbies": ["reading", "movies", "cooking"]}],
                [{"name": "Bob", "hobbies": ["cycling", "gaming", "movies"]},
                 {"name": "David", "hobbies": ["movies", "cooking", "gaming"]}]
            ],
            "1": [
                [{"name": "Alice", "hobbies": ["reading", "cycling", "movies"]},
                 {"name": "Charlie", "hobbies": ["reading", "traveling"]}],
                [{"name": "Charlie", "hobbies": ["reading", "traveling"]},
                 {"name": "Eve", "hobbies": ["reading", "movies", "cooking"]}],
                [{"name": "David", "hobbies": ["movies", "cooking", "gaming"]},
                 {"name": "Eve", "hobbies": ["reading", "movies", "cooking"]}]
            ]
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
