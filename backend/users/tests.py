from django.test import TestCase
from .models import CustomUser
import datetime

class CustomUserTests(TestCase):
    def setUp(self):
        # Create a sample user for testing
        self.user = CustomUser.objects.create(
            first_name='John',
            surname='Doe',
            username='john_doe',
            phone_number='123-456-7890',
            email='john.doe@example.com',
            date_of_birth='1990-01-01',
        )

    def test_custom_user_fields(self):
        """
        Test that the custom user fields are set correctly.
        """
        # Retrieve the user from the database
        my_model = CustomUser.objects.get(username='john_doe')
        # Check if custom fields are set correctly
        self.assertEqual(my_model.first_name, 'John')
        self.assertEqual(my_model.surname, 'Doe')
        self.assertEqual(my_model.username, 'john_doe')
        self.assertEqual(my_model.phone_number, '123-456-7890')
        self.assertEqual(my_model.email, 'john.doe@example.com')
        self.assertEqual(my_model.date_of_birth, datetime.date(1990, 1, 1))

    def test_custom_user_str_method(self):
        """
        Test the __str__ method of the custom user model.
        """
        # Check the __str__ method
        expected_str = 'john_doe'
        self.assertEqual(str(self.user), expected_str)

    def test_unique_email(self):
        """
        Test that creating two users with the same email raises an exception.
        """
        # Attempt to create two users with the same email
        # This should raise an exception
        with self.assertRaises(Exception):
            CustomUser.objects.create(
                first_name='John',
                surname='Doe',
                username='john_doe',
                phone_number='123-456-7890',
                email='john.doe@example.com',
                date_of_birth='1990-01-01',
            )

    # Additional tests for max lengths and validation
    # ...
    def test_max_length_username(self):
        CustomUser.objects.all().delete()
        max_length = CustomUser._meta.get_field('username').max_length
        with self.assertRaises(Exception):
            CustomUser.objects.create(
                first_name='John',
                surname='Doe',
                username='a' * max_length+1,
                phone_number='123-456-78901',
                email='john.doe@example.com1',
                date_of_birth='1990-01-01',
            )

        
    def test_max_length_phone_number(self):
        CustomUser.objects.all().delete()
        max_length = CustomUser._meta.get_field('phone_number').max_length
        with self.assertRaises(Exception):
            CustomUser.objects.create(
                first_name='John',
                surname='Doe',
                username='john_doe',
                phone_number='1' * max_length+1,
                email='john.doe@example.com1',
                date_of_birth='1990-01-01',
            )
    
    def test_max_length_email(self):
        CustomUser.objects.all().delete()
        max_length = CustomUser._meta.get_field('email').max_length
        with self.assertRaises(Exception):
            CustomUser.objects.create(
                first_name='John',
                surname='Doe',
                username='john_doe',
                phone_number='123-456-78901',
                email='a' * max_length+1,
                date_of_birth='1990-01-01',
            )
    
    def test_max_length_first_name(self):
        CustomUser.objects.all().delete()
        max_length = CustomUser._meta.get_field('first_name').max_length
        with self.assertRaises(Exception):
            CustomUser.objects.create(
                first_name='a' * max_length+1,
                surname='Doe',
                username='john_doe',
                phone_number='123-456-78901',
                email='john.doe@example.com1',
                date_of_birth='1990-01-01',
            )
    
    def test_max_length_surname(self):
        CustomUser.objects.all().delete()
        max_length = CustomUser._meta.get_field('surname').max_length
        with self.assertRaises(Exception):
            CustomUser.objects.create(
                first_name='John',
                surname='a' * max_length+1,
                username='john_doe',
                phone_number='123-456-78901',
                email='john.doe@example.com1',
                date_of_birth='1990-01-01',
            )

    def test_email_validation(self):
        """
        Test that creating a user without a valid email raises an exception.
        """
        # Attempt to create a user without a valid email
        # This should raise an exception
        with self.assertRaises(Exception):
            CustomUser.objects.create(
                first_name='John',
                surname='Doe',
                username='john_doe',
                phone_number='123-456-7890',
                # No email provided
            )