import json
import math


OFFICE_COORDINATES = [37.788802,-122.4025067] #degrees
THRESHOLD = 100 # kilometers
EARTH_RADIUS = 6371

# gets list of closeby customers
def get_closeby_customer_list(customer_list):
    closeby_customer_list = []
    for customer in customer_list:
        if(close_to_office(customer)):
            closeby_customer_list.append((customer["name"], customer["user_id"]))
    return sorted(closeby_customer_list, key=lambda x: x[1])

# determines if a customer is close to office
def close_to_office(customer):
    customer_coordinates = deg_to_radians([float(customer["latitude"]), float(customer["longitude"])])
    office_coordinates = deg_to_radians(OFFICE_COORDINATES)

    return (distance_between(customer_coordinates, office_coordinates) <=  THRESHOLD)

# finds distance between two radian coordinates
def distance_between(customer_coordinates, office_coordinates): # uses spherical law of cosines formula
    customer_lat, customer_long = customer_coordinates[0], customer_coordinates[1]
    office_lat, office_long = office_coordinates[0], office_coordinates[1]

    part_one = (math.sin(customer_lat) * math.sin(office_lat))
    part_two = (math.cos(customer_lat) * math.cos(office_lat)) * math.cos(office_long - customer_long)

    angle = math.acos(round(part_one + part_two,7)) # rounding to 7th place allows for inconsistency in floating point

    distance = EARTH_RADIUS * angle
    return distance

# converts degree coordinates to radians
def deg_to_radians(degree_coordinates):
    radian_coordinates = (map(math.radians, [degree_coordinates[0], degree_coordinates[1]]))
    return list(radian_coordinates)

def read_customer_file(customer_file):
    json_list = []
    with open (customer_file) as customer_json:
        for line in customer_json:
            json_list.append(json.loads(line))
    return json_list


if __name__ == "__main__":

    customer_list = read_customer_file("../input/Customer_List.txt")
    closeby_customer_list = get_closeby_customer_list(customer_list)

    with open('../output.txt', 'w') as file:
        file.write("CUSTOMERS WITHIN " + str(THRESHOLD) + " KILOMETERS OF OFFICE \n")
        for customer in closeby_customer_list:
            customer_string = " Customer:   " + customer[0] + " ID:  " + str(customer[1]) + "\n"
            print(customer_string )
            file.write(customer_string)
