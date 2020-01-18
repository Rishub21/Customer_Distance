import pytest
from src.calculate import *
import random
import math
from faker import Faker

fake = Faker()

@pytest.fixture
def sample_coordinate():
    return [int(fake.longitude()),int(fake.latitude())]

@pytest.fixture
def customer_factory():
    def _customer_factory(close):
        customer = {
                        "latitude" : float(OFFICE_COORDINATES[0]),
                        "longitude" : float(OFFICE_COORDINATES[1]),
                        "user_id" : random.randint(1,101),
                        "name" : fake.name()
                    }
        if(not close):
            customer["latitude"] -= 2 # ensures this is far enough from office
        return customer
    return _customer_factory


def test_deg_to_radians(sample_coordinate):
    assert deg_to_radians([0,0]) == [0,0]
    assert(deg_to_radians([90,180])) == [math.pi/2, math.pi]
    assert(deg_to_radians([-90,-180])) == [-math.pi/2, -math.pi]
    assert(deg_to_radians([-90,-180])) == [-math.pi/2, -math.pi]
    assert(deg_to_radians(sample_coordinate)) == list(map(math.radians, sample_coordinate))

def test_distance_between(sample_coordinate):

    # the round to 3rd decimal means that as long as we are within a meter of zero  (allows for inconsistency of floating point computation)
    assert round(distance_between(sample_coordinate,sample_coordinate),3) == 0

    sample_coordinate_2 = sample_coordinate.copy()
    sample_coordinate_2[0] += 1
    assert distance_between(sample_coordinate, sample_coordinate_2) != 0

def test_close_to_office(customer_factory):
    assert(close_to_office(customer_factory(close = False)) == False)
    assert(close_to_office(customer_factory(close = True)) == True)
