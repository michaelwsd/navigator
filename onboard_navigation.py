"""
@file onboard_navigation.py
"""
from city import City, get_city_by_id
from country import Country, find_country_of_city, add_city_to_country
from itinerary import Itinerary
from vehicles import Vehicle, create_example_vehicles
from csv_parsing import create_cities_countries_from_csv
from path_finding import find_shortest_path
from map_plotting import plot_itinerary

def validate_input(prompt: str, valid_inputs: dict[str, any], show_options=True, item_descriptors=None):
    """
    Allows the user to choose something from a set of valid options.
    :param prompt: a string to prepend to the line the user types their selection on
    :param valid_inputs: a dictionary where the key is a string that the user inputs to get the value
    :param show_options: a boolean that determines whether or not to print all available options
    :param item_descriptors: a list of strings that contain additional information to print for each option
    :return: the value from valid_inputs that corresponds to the inputted key
    """
    # If true, prompt user to select an option
    if show_options:
        print("Enter a number to select an option: ")
        # compose the string for each option and print it
        # for each city in valid_inputs
        for index, (key, value) in enumerate(valid_inputs.items()):
            # Set the string to display
            choice_display = f"{key}: {str(value)}"
            # if a valid item descriptor exists for this option, add it to the string
            # item descriptor only exists if select_from_duplicate_cities has more than 1 cities
            if item_descriptors != None and index < len(item_descriptors):
                choice_display += f" ({item_descriptors[index]})"
            print(choice_display)
            
    # loop until a valid input is given
    # This is for choosing cities
    while True:
        user_input = input(prompt)
        if user_input in valid_inputs.keys():
            print()
            # This returns all the city instances in the dictionary
            return valid_inputs[user_input]
        else:
            print('Invalid input, please try again.')

def select_from_duplicate_cities(cities: list):
    """
    given a list of duplicate cities, allow the user to choose which one they meant.
    :param cities: a list of cities with the same name
    :return: the desired city
    """
    # Return the first city in the list if there's only one
    if len(cities) == 1:
        return cities[0]
    else:
        # create a dictionary of valid choices for cities more than 1
        city_choices = create_numbered_input_options(cities)
        # prints the string as a dictionary of every city with the same name
        # also append the country name to the display string
        return validate_input(
            f"There are multiple cities called {cities[0].name}. Select one: ", 
            city_choices, 
            show_options=True, 
            # Add the country name to the string of duplicate cities
            item_descriptors=[c.country for c in cities]
        )

# Creates a dictionary, numbering each items in the list to use with valid input
def create_numbered_input_options(items: list):
    """
    create a dictionary of valid choices to be used with validate_input
    :param items: a list of items to be selected from
    :return: a dictionary, where each key is a number starting from 1, and values are the given items
    """
    # create a list of numbers from 1 to len(items)+1
    # cast them all to strings using map
    # create a zip object to associate each number string with an item from items
    # cast to dict then return
    return dict(zip(map(str, range(1, len(items)+1)), items))
              
def navigate():
    """
    allows a user to:
    - select a vehicle
    - select an origin and destination city
    - view a plotted map of the shortest path between those cities if it exists
    :return: None
    """
    create_cities_countries_from_csv("worldcities_truncated.csv")
    
    # Number the vehices using create number input options
    vehicle_choices = create_numbered_input_options(create_example_vehicles())
    # Prompt user to choose vehicle
    vehicle_chosen = validate_input('Please pick a vehicle: ', vehicle_choices)

    # select from duplicate cities check if the city is equal to 1
    # if not, select function returns the duplicate cities along with its countries
    origin = select_from_duplicate_cities(validate_input('Please enter an origin city: ', City.name_to_cities, show_options=False))
    destination = select_from_duplicate_cities(validate_input('Please enter a destination city: ', City.name_to_cities, show_options=False))

    itinerary = find_shortest_path(vehicle_chosen, origin, destination)
    if itinerary != None:
        print(f"Path found! {str(itinerary)}\nPlotting...")
        plot_itinerary(itinerary, projection = 'robin', line_width=2, colour='b')
    else:
        print("Could not find a path.")
    return

if __name__ == "__main__":
    navigate()
