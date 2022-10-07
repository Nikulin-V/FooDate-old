from django.contrib.auth import get_user_model
from django.test import TestCase

from core.backends import EmailAuthBackend

User = get_user_model()


class EmailAuthBackendTest(TestCase):
    def setUp(self):
        user = User.objects.create(
            username='test',
            email='test@mail.ru',
            first_name='test_first_name',
            last_name='test_last_name'
        )
        user.set_password('test_password')
        user.save()

        user_verified = User.objects.create(
            username='verified_user',
            email='user@mail.ru',
            first_name='verified_user_first_name',
            last_name='verified_user_last_name',
            is_email_verified=True
        )
        user_verified.set_password('verified_user_password')
        user_verified.save()

        user_unverified = User.objects.create(
            username='unverified_user',
            email='user@mail.ru',
            first_name='unverified_user_first_name',
            last_name='unverified_user_last_name',
            is_email_verified=False
        )
        user_unverified.set_password('unverified_user_password')
        user_unverified.save()

        bad_username_user = User.objects.create(
            username='bad@user',
            email='bad_username_user@mail.ru',
            first_name='bad_username_user_first_name',
            last_name='bad_username_user_last_name'
        )
        bad_username_user.set_password('bad_username_user_password')
        bad_username_user.save()

    def test_authenticate_throw_login(self):
        user = User.objects.get(username='test')
        request = 'WSGIRequest_plug'
        backend = EmailAuthBackend()
        self.assertEqual(
            user,
            backend.authenticate(request, user.username, 'test_password'),
            "Can't authenticate throw login with good password"
        )
        self.assertEqual(
            None,
            backend.authenticate(request, user.username, 'bad_password'),
            "Authenticates throw login with bad password"
        )

    def test_authenticate_throw_email(self):
        user = User.objects.get(email='test@mail.ru')
        request = 'WSGIRequest_plug'
        backend = EmailAuthBackend()
        self.assertEqual(
            user,
            backend.authenticate(request, user.email, 'test_password'),
            "Can't authenticate throw email with good password."
        )
        self.assertEqual(
            None,
            backend.authenticate(request, user.username, 'bad_password'),
            "Authenticates throw email with bad password."
        )

    def test_authenticate_verified_and_unverified_users_by_email(self):
        verified_user = User.objects.get(username='verified_user')
        unverified_user = User.objects.get(username='unverified_user')
        request = 'WSGIRequest_plug'
        backend = EmailAuthBackend()
        self.assertEqual(
            verified_user,
            backend.authenticate(request, verified_user.email, 'verified_user_password'),
            "Can't authenticate throw verified email with good password."
        )
        self.assertEqual(
            None,
            backend.authenticate(request, unverified_user.email, 'unverified_user_password'),
            "Authenticates user with unverified email with his password instead of user with verified email."
        )
        self.assertEqual(
            verified_user,
            backend.authenticate(request, unverified_user.email, 'verified_user_password'),
            "Authenticates user with unverified email instead of user with verified email."
        )

    def test_authenticate_throw_bad_login(self):
        bad_user = User.objects.get(username='bad@user')
        request = 'WSGIRequest_plug'
        backend = EmailAuthBackend()
        self.assertEqual(
            bad_user,
            backend.authenticate(request, bad_user.username, 'bad_username_user_password')
        )
