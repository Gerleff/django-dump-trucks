"""Tests to support Dump Trucks app"""
from django.test import TestCase, Client
from shapely import wkt

from .models import Machine, Storage


class TrucksTest(TestCase):
    """Main test case"""
    fixtures = ['test_data.json']

    def test_ping(self):
        """Testing app and server with ping"""
        c = Client()
        response = c.get('/ping')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'pong', 'not pong!')

    def test_get_app(self):
        """Testing GET /"""
        c = Client()
        print('RUN GET /')
        response = c.get('/')
        print('Checking response code... ', response.status_code)
        self.assertEqual(response.status_code, 200)
        print('OK')

    def test_invalid_data_posted(self):
        """Testing POST / with invalid data"""
        c = Client()
        data = {'101': '23'}
        print('RUN POST / with ', data)
        response = c.post('/', data=data)
        print('Checking response code... ', response.status_code)
        self.assertEqual(response.status_code, 200)
        print('OK')
        print('Checking reaction on invalid data...')
        self.assertEqual(response.content, b'Invalid coordinates inserted')
        print('OK')

    def _polygon_check(self, coordinate: str, storage: Storage) -> bool:
        """Checking out if ore point in polygon"""
        polygon = 'POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))'
        self.assertEqual(storage.coordinates, polygon)
        polygon = wkt.loads(polygon)
        point = wkt.loads(f'POINT ({coordinate})')
        return polygon.contains(point) or polygon.covers(point)

    def test_ideal_scenario(self):
        """Testing ideal but various scenario"""
        c = Client()
        data = {'101': '30 40',
                '102': '40 40',
                'K103': '0 0'}
        print('RUN POST / with ', data)
        response = c.post('/', data=data)
        print('Checking response code... ', response.status_code)
        self.assertEqual(response.status_code, 301)
        print('OK')
        print('Checking emptiness in machines...')
        for item in data.keys():
            machine = Machine.objects.get(pk=item)
            self.assertEqual(machine.amount, 0)
            self.assertEqual(machine.silicon_dioxide, 0)
            self.assertEqual(machine.iron, 0)
        print('OK')
        print('Checking if polygon contains point of drop ...')
        storage = Storage.objects.first()
        self.assertEqual(
            [self._polygon_check(coordinate=coord, storage=storage)
             for coord in data.values()], [True, True, False]
        )
        print('OK')
        print('Checking if math was right...')
        self.assertEqual(storage.amount, 1125.0)
        self.assertEqual(storage.iron, 0.65)
        self.assertEqual(storage.silicon_dioxide, 0.34)
        print('OK')
