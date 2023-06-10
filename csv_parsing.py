"""
@file city_country_csv_reader.py
"""
import csv
from city import City
from country import Country, add_city_to_country

def create_cities_countries_from_csv(path_to_csv: str) -> None:
    """
    Reads a CSV file given its path and creates instances of City and Country for each line.

    :param path_to_csv: The path to the CSV file.
    """
    with open(path_to_csv, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)

        # Creating the country by iterating through each row in csv file
        for row in csvreader:
            country = str(row['country'])
            iso3 = str(row['iso3'])
            name = str(row['city_ascii'])
            coordinates = (float(row['lat']), float(row['lng']))
            city_type = str(row['capital'])
            try:
                city_population = int(row['population'])
            except ValueError:
                city_population = 0
            city_id = int(row['id'])

            # create and add city to country specified
            city_created = City(name, coordinates, city_type, city_population, city_id)
            add_city_to_country(city_created, country, iso3)

if __name__ == "__main__":
    create_cities_countries_from_csv("worldcities_truncated.csv")
    for country in Country.name_to_countries.values():
        country.print_cities()
