from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

# TODO: Figure out if these tests are "best practice"


class UserTest(APITestCase):
    def _create_post_request_and_return_response(self, url,
                                                 data=None, format=None):
        if data is None:
            data = {"username": "gopar1", "password": "skater1",
                    "email": "hello@csumb.edu", "first_name": "Joseph",
                    "last_name": "Sup"}
        if format is None:
            format = 'json'
        return self.client.post(url, data, format=format)

    def _create_user_and_setup_auth_header_client(self, url):
        user_response = self._create_post_request_and_return_response(url)
        token = user_response.data['token']
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        return client

    def test_create_user(self):
        """
        Ensure we can create a new user object.
        """
        url = reverse('user-list')
        response = self._create_post_request_and_return_response(url)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_token_received_when_create_user(self):
        """
        Make sure we receive a token when we create a user
        """
        url = reverse('user-list')
        response = self._create_post_request_and_return_response(url)
        self.assertIn('token', response.data)
        # Token is NOT empty
        self.assertNotEqual(response.data['token'], "")

    def test_can_get_list_of_products(self):
        """
        When we make a GET request, we get a list of products
        """
        client = self._create_user_and_setup_auth_header_client("/api/users/")

        url = reverse('product-list')
        response = client.get(url)
        self.assertIsInstance(response.data, list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_get_list_of_users(self):
        """
        When we make a GET request, we get a list of users
        """
        url = reverse('user-list')
        client = self._create_user_and_setup_auth_header_client(url)

        response = client.get(url)
        self.assertIsInstance(response.data, list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_info(self):
        """
        When we hit the API /user/PK we should see info about that current user.
        """
        url = reverse('user-list')
        client = self._create_user_and_setup_auth_header_client(url)
        user = User.objects.first()
        user_pk_response = client.get(url + "{}/".format(user.pk))

        for attrb in "first_name last_name pk email".split():
            self.assertIn(attrb, user_pk_response.data)

        # Should only return 4 members from API
        self.assertEqual(len(user_pk_response.data), 4)
        # No weird errors
        self.assertEqual(user_pk_response.status_code, status.HTTP_200_OK)
