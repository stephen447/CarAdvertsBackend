
# Create your tests here.
from django.test import TestCase
from .models import Advert

class AdvertModelTest(TestCase):
    def setUp(self):
        # Set up test data
        self.advert_data = {
            'description': 'Test description',
            'make': 'TestMake',
            'model': 'TestModel',
            'year': 2022,
            'mileage': 10000,
            'price': 25000.50,
            'fuel_type': 'Gasoline',
            'transmission': 'Automatic',
            'color': 'Red',
            'condition': 'Excellent',
        }

    def test_create_advert(self):
        # Test creating an Advert instance
        advert = Advert.objects.create(**self.advert_data)

        # Check if the instance was created successfully
        self.assertIsInstance(advert, Advert)
        self.assertEqual(str(advert), f"{advert.year} {advert.make} {advert.model} - {advert.price}")

    def test_advert_fields(self):
        # Test each field of the Advert model
        advert = Advert.objects.create(**self.advert_data)

        self.assertEqual(advert.description, 'Test description')
        self.assertEqual(advert.make, 'TestMake')
        self.assertEqual(advert.model, 'TestModel')
        self.assertEqual(advert.year, 2022)
        self.assertEqual(advert.mileage, 10000)
        self.assertEqual(advert.price, 25000.50)
        self.assertEqual(advert.fuel_type, 'Gasoline')
        self.assertEqual(advert.transmission, 'Automatic')
        self.assertEqual(advert.color, 'Red')
        self.assertEqual(advert.condition, 'Excellent')

    def test_model_str_method(self):
        # Test the __str__ method of the Advert model
        advert = Advert.objects.create(**self.advert_data)

        expected_str = f"{advert.year} {advert.make} {advert.model} - {advert.price}"
        self.assertEqual(str(advert), expected_str)

    #

    def test_model_update(self):
        # Test updating an Advert instance
        advert = Advert.objects.create(**self.advert_data)

        # Modify a field and save
        advert.price = 27000.75
        advert.save()

        # Retrieve the updated instance from the database
        updated_advert = Advert.objects.get(id=advert.id)

        # Check if the field was updated successfully
        self.assertEqual(updated_advert.price, 27000.75)
    
    def test_example_api_view(self):
            # Define the URL for the API view
            #url = reverse('example_api')
            url = '/adverts/search/'

            # Make a GET request to the API view
            response = self.client.get(url)

            # Check if the response has a 200 status code
            self.assertEqual(response.status_code, 200)

            # Check the content of the JSON response
            expected_data = []
            self.assertJSONEqual(str(response.content, encoding='utf-8'), expected_data)
    
    
        