import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from profiles.api.serializers import ProfileSerializer, ProfileStatusSerializer
from profiles.models import Profile, ProfileStatus


class RegistrationTestCase(APITestCase):

    def test_registration(self):
        data = {"username": "test", "email": "test@test.com",
                "password1": "a_lot _of21", "password2": "a_lot _of21"}
        response = self.client.post("/api/rest-auth/registration/", data)
        # print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ProfileViewSetTestcase(APITestCase):

    list_url = reverse("profile-list")

    def setUp(self):
        self.user = User.objects.create_user(
            username="sample", password="aa_lot _of2133")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        # print("###################################")
        # print(str(self.token))
        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # print(self.token.key)

    def test_profile_list_authenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_list_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_profile_detail_retrieve(self):
        response = self.client.get(reverse("profile-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"], "sample")

    def test_profile_update(self):
        response = self.client.put(
            reverse("profile-detail",
                    kwargs={"pk": 1}), {"city": "korean", "bio": "ann"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content),
                         {"id": 1, "user": "sample", "bio": "ann", "city": "korean", "avatar": None})


def test_profile_update_random(self):
    random_user = User.objects.create_user(
        username="tttttt", password="aa_lot_eesdfa")
    self.client.force_authenticate(user=random_user)
    response = self.client.put(
        reverse("profile-detail", kwargs={"pk": 1})), {"city": "korean", "bio": "ann!"}
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ProfileStatusViewSetTestcase(APITestCase):

    url = reverse("status-list")

    def setUp(self):
        self.user = User.objects.create_user(
            username="sample", password="aa_lot _of2133")
        self.status = ProfileStatus.objects.create(
            user_profile=self.user.profile, status_contant="status code")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_status_list_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_status_list_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_status_create(self):
        data = {"status_contant": "a new status!"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["user_profile"], "sample")
        self.assertEqual(response.data["status_contant"], "a new status!")

    def test_single_status_create(self):
        serializer_data = ProfileSerializer(instance=self.status).data
        response = self.client.get(reverse("status-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_status_update_owner(self):
        data = {"status_contant": "content updated"}
        response = self.client.put(
            reverse("status-detail", kwargs={"pk": 1}), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status_contant"], "content updated")

    def test_status_update_by_random_user(self):
        random_user = User.objects.create_user(
            username="random", password="psw123123123")
        self.client.force_authenticate(user=random_user)
        response = self.client.put(
            reverse("status-detail", kwargs={"pk": 1}), {"bio": "hacked!!!"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
