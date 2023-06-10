"""
@file itinerary.py
"""
from city import City, create_example_cities, get_cities_by_name

class Itinerary():
    """
    A sequence of cities.
    """
    def __init__(self, cities: list[City]) -> None:
        """
        Creates an itinerary with the provided sequence of cities,
        conserving order.
        :param cities: a sequence of cities, possibly empty.
        :return: None
        """
        # Associate self.cities to the list of cities
        self.cities = cities

    def total_distance(self) -> int:
        """
        Returns the total distance (in km) of the itinerary, which is
        the sum of the distances between successive cities.
        :return: the total distance.
        """
        # Loop through the self.cities list
        # Add the distance between successive cities using distance method 
        total_distance = 0
        for index, city in enumerate(self.cities[:-1]):
            total_distance += City.distance(city, self.cities[index+1])
        return total_distance

    def append_city(self, city: City) -> None:
        """
        Adds a city at the end of the sequence of cities to visit.
        :param city: the city to append
        :return: None.
        """
        self.cities.append(city)

    def min_distance_insert_city(self, city: City) -> None:
        """
        Inserts a city in the itinerary so that the resulting
        total distance of the itinerary is minimised.
        :param city: the city to insert
        :return: None.
        """
        # Creating a list for the possible total distances
        min_distance = []

        # Loop through the list
        for index, _ in enumerate(self.cities):
            # Create a shallow copy of the list
            test_list = self.cities[:]
            # Insert the city in each index
            test_list.insert(index, city)

            # Create an instance for the new list, calculate its distance
            itinerary = Itinerary(test_list)
            new_distance = itinerary.total_distance()
            # Append the new distance to the list of distances
            min_distance.append(new_distance)
        
        # Find the index of the minimum index and insert the city in that index
        min_index = min_distance.index(min(min_distance))
        self.cities.insert(min_index, city)
            
    def __str__(self) -> str:
        """
        Returns the sequence of cities and the distance in parentheses
        For example, "Melbourne -> Kuala Lumpur (6368 km)"

        :return: a string representing the itinerary.
        """
        # Calculates the total distance to travel
        total_distance = self.total_distance()

        # Creates an empty string
        sequence_of_cities = ''
        # Loop through the list, adding the city name and the connectives
        for index, city in enumerate(self.cities):
            if index > 0:
                sequence_of_cities += '-> '
                # This ensures only the city name is printed
            sequence_of_cities += str(city)[:-(len(str(city.city_id))+2)]
        return sequence_of_cities + f'({total_distance} km)'

if __name__ == "__main__":
    create_example_cities()
    test_itin = Itinerary([get_cities_by_name("Melbourne")[0],
                           get_cities_by_name("Kuala Lumpur")[0]])
    print(test_itin)

    #we try adding a city
    test_itin.append_city(get_cities_by_name("Baoding")[0])
    print(test_itin)

    #we try inserting a city
    test_itin.min_distance_insert_city(get_cities_by_name("Sydney")[0])
    print(test_itin)

    #we try inserting another city
    test_itin.min_distance_insert_city(get_cities_by_name("Canberra")[0])
    print(test_itin)

