"""
@file map_plotting.py
"""
from mpl_toolkits.basemap import Basemap #have to do 'pip install basemap'
import matplotlib.pyplot as plt
from itinerary import Itinerary
from city import City

def plot_itinerary(itinerary: Itinerary, projection = 'robin', line_width=2, colour='b') -> None:
    """
    Plots an itinerary on a map and writes it to a file.
    Ensures a size of at least 50 degrees in each direction.
    Ensures the cities are not on the edge of the map by padding by 5 degrees.
    The name of the file is map_city1_city2_city3_..._cityX.png.

    :param itinerary: The itinerary to plot.
    :param projection: The map projection to use.
    :param line_width: The width of the line to draw.
    :param colour: The colour of the line to draw.
    """
    # Setting the latitude and longitude limits
    min_lat = min(city.coordinates[0] for city in itinerary.cities) - 5
    max_lat = max(city.coordinates[0] for city in itinerary.cities) + 5
    min_lon = min(city.coordinates[1] for city in itinerary.cities) - 5
    max_lon = max(city.coordinates[1] for city in itinerary.cities) + 5

    # Creating the map 
    world_map = Basemap(projection=projection, lat_0=0, lon_0=0, resolution='l', llcrnrlat=min_lat, urcrnrlat=max_lat, llcrnrlon=min_lon, urcrnrlon=max_lon)
    world_map.drawcoastlines(linewidth=1, color='gray')
    world_map.drawcountries(linewidth=1, color='gray')
    world_map.fillcontinents(color='#C1BBBA', lake_color='white')

    # Adding city courdinates to a list
    city_locations = [city.coordinates for city in itinerary.cities]

    # For every city coordinate in the list, draw a line between consecutive cities using drawgreatcircle
    for index, city in enumerate(city_locations[:-1]):
        start = city
        end = city_locations[index+1]
        world_map.drawgreatcircle(start[1], start[0], end[1], end[0], linewidth=line_width, color=colour)
    
    # Save the file and output
    plt.savefig('Map of Itinerary from {} to {}'.format(itinerary.cities[0].name, itinerary.cities[-1].name))
    
if __name__ == "__main__":
    # create some cities
    city_list = list()

    city_list.append(City("Melbourne", (-37.8136, 144.9631), "primary", 4529500, 1036533631))
    city_list.append(City("Sydney", (-33.8688, 151.2093), "primary", 4840600, 1036074917))
    city_list.append(City("Brisbane", (-27.4698, 153.0251), "primary", 2314000, 1036192929))
    city_list.append(City("Perth", (-31.9505, 115.8605), "1992000", 2039200, 1036178956))

    # plot itinerary
    plot_itinerary(Itinerary(city_list))

    

