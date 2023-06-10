"""
@file path_finding.py
"""
import math
import networkx as nx
from country import find_country_of_city
from city import City, get_city_by_id
from itinerary import Itinerary
from vehicles import Vehicle, create_example_vehicles, CrappyCrepeCar, DiplomacyDonutDinghy, TeleportingTarteTrolley
from csv_parsing import create_cities_countries_from_csv


def find_shortest_path(vehicle: Vehicle, from_city: City, to_city: City) -> Itinerary | None:
    """
    Returns a shortest path between two cities for a given vehicle as an Itinerary,
    or None if there is no path.

    :param vehicle: The vehicle to use.
    :param from_city: The departure city.
    :param to_city: The arrival city.
    :return: A shortest path from departure to arrival, or None if there is none.
    """
    # return the trivial cases so we don't waste resources on a graph if not necessary
    match vehicle:
        case CrappyCrepeCar():
            # trivial as can go from anywhere to anywhere so the fastest route is always just A to B
            return Itinerary([from_city, to_city])

        case DiplomacyDonutDinghy():
            # trivial case where both cities are primary
            if (from_city.city_type == 'primary' and to_city.city_type == 'primary' 
                and vehicle.between_primary_speed > vehicle.in_country_speed):
                return Itinerary([from_city, to_city])

            # create two complete graphs of the origin and destination countries, then merge
            country1_graph = nx.complete_graph(find_country_of_city(from_city).get_cities())
            country2_graph = nx.complete_graph(find_country_of_city(to_city).get_cities())
            country_graph = nx.compose(country1_graph, country2_graph)
            # iterate through all edges of merged country graphs and update edge weights
            for city1, city2 in country_graph.edges:
                country_graph[city1][city2]["weight"] = vehicle.compute_travel_time(city1, city2)

            # create complete graph of all primary cities, then update edge weights
            primarycity_graph = nx.complete_graph([c for c in country_graph.nodes if c.city_type == "primary"])
            for city1, city2 in primarycity_graph.edges:
                primarycity_graph[city1][city2]["weight"] = vehicle.compute_travel_time(city1, city2)

            # merge primary city and country graphs
            mapgraph = nx.compose(country_graph, primarycity_graph)

            # return shortest path of our graph
            try:
                return Itinerary(nx.shortest_path(mapgraph, from_city, to_city))
            except:
                return None

        case TeleportingTarteTrolley():
            # trivial case if we can hop directly to the end
            if from_city.distance(to_city) < vehicle.max_distance:
                return Itinerary([from_city, to_city])

            # create a complete graph
            mapgraph = nx.complete_graph(City.id_to_cities.values())
            # create a subgraph comprised of edges in complete graph that are possible
            final_graph = nx.Graph()
            for city1, city2 in mapgraph.edges:
                time = vehicle.compute_travel_time(city1, city2)
                if time != math.inf:
                    final_graph.add_edge(city1, city2, weight=time)

            # return the shortest path of our graph
            try:
                return Itinerary(nx.shortest_path(final_graph, from_city, to_city))
            except:
                return None

if __name__ == "__main__":
    create_cities_countries_from_csv("worldcities_truncated.csv")
    vehicles = create_example_vehicles()

    from_cities = set()
    for city_id in [1036533631, 1036142029, 1458988644]:
        from_cities.add(get_city_by_id(city_id))

    #we create some vehicles
    vehicles = create_example_vehicles()

    to_cities = set(from_cities)
    for from_city in from_cities:
        to_cities -= {from_city}
        for to_city in to_cities:
            print(f"{from_city} to {to_city}:")
            for test_vehicle in vehicles:
                shortest_path = find_shortest_path(test_vehicle, from_city, to_city)
                print(f"\t{test_vehicle.compute_itinerary_time(shortest_path)}"
                      f" hours with {test_vehicle} with path {shortest_path}.")

