import requests
import json
import pandas as pd
from typing import List


def get_data(file_path: str, max_coordinates: int = 100) -> str:
    """
    Read latitude and longitude data from a CSV file and format it for the API request.

    Args:
        file_path (str): Path to the CSV file containing latitude and longitude data.
        max_coordinates (int, optional): Maximum number of coordinates to consider. Defaults to 100.

    Returns:
        str: Formatted coordinates string for the API request.
    """
    try:
        # Read the CSV file and extract latitude and longitude columns
        df = pd.read_csv(file_path)
        df = df[["lat", "lng"]]

        # Convert DataFrame to a list of tuples and format as "lat,lng"
        coordinates = list(df.itertuples(index=False, name=None))
        coordinates = [f"{c[0]},{c[1]}" for c in coordinates][:max_coordinates]

        # Join the formatted coordinates with a semicolon
        return ";".join(coordinates)
    except FileNotFoundError:
        raise FileNotFoundError("CSV file not found.")
    except Exception as e:
        raise Exception(f"An error occurred while processing the data: {e}")


def get_matrix(coordinates: str) -> dict:
    """
    Get the distance matrix from the OSRM API for the given coordinates.

    Args:
        coordinates (str): Formatted coordinates string for the API request.

    Returns:
        dict: JSON response containing the distance matrix and annotations.
    """
    try:
        url = f"http://router.project-osrm.org/table/v1/driving/{coordinates}?annotations=distance"
        response = requests.get(url)

        # Raise an exception if the API request was not successful
        response.raise_for_status()

        # Parse the JSON response and return the result as a dictionary
        return json.loads(response.text)
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"API request failed: {e}")
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON response from the API.")
    except Exception as e:
        raise Exception(f"An error occurred while fetching the distance matrix: {e}")


def parse_coordinates(df: pd.DataFrame) -> str:
    """
    Parse latitude and longitude data from a DataFrame and format it for the API request.

    Args:
        df (pd.DataFrame): DataFrame containing 'lat' and 'lng' columns.

    Returns:
        str: Formatted coordinates string for the API request.
    """
    # Extract latitude and longitude columns from the DataFrame
    coordinates = df[["lat", "lng"]]

    # Convert DataFrame to a list of tuples and format as "lng,lat"
    coordinates = list(coordinates.itertuples(index=False, name=None))
    coordinates = [f"{c[1]},{c[0]}" for c in coordinates]

    # Join the formatted coordinates with a semicolon
    return ";".join(coordinates)


if __name__ == "__main__":
    try:
        # Specify the path to the CSV file containing latitude and longitude data
        csv_file_path = "data/places.csv"

        # Get the coordinates data and fetch the distance matrix
        coordinates_data = get_data(csv_file_path)
        distance_matrix = get_matrix(coordinates_data)

        # Print the distance matrix
        print(distance_matrix)
    except Exception as e:
        print(f"Error: {e}")
