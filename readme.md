https://goo.gl/maps/mFtLHFZs2XbvHa7V7
**README**

## Description

This code performs routing optimization for cities using the OR-Tools library. It calculates the optimal routes between selected points in each city and saves the results to CSV files.

## Requirements

- Python 3.x
- pandas
- numpy
- OR-Tools

## Installation

1. Install the required Python libraries using pip:

```bash
pip install pandas numpy ortools
```

2. Clone the repository or download the code files.

3. Prepare the necessary data:
   - Ensure you have the `cities.csv` and `pos.csv` files containing city information and point of interest data, respectively.
   - Update the file paths accordingly in the code if the data is located in a different directory.

## Usage

1. Import the required functions and libraries:

```python
import pandas as pd
from src.api_osmr import get_matrix
from src.routing import optimize_routes
import numpy as np
```

2. Load city data and prepare coordinates:

```python
cities = pd.read_csv("data/cities.csv")
df = cities[["lat_city", "lng_city"]]
cities_list = cities.city
coordinates = list(df.itertuples(index=False, name=None))
coordinates = [f"{c[1]},{c[0]}" for c in coordinates]
coordinates = ';'.join(coordinates)
```

3. Obtain distance matrix using the Open Source Routing Machine (OSRM) API:

```python
response_distances = get_matrix(coordinates)
distances = np.array(response_distances["distances"]).astype(int)
```

4. Perform routing optimization for each city and save the results:

```python
places = pd.read_csv("data/pos.csv")

for city in places.city.unique():
    df_city = places[places.city == city][:10].reset_index(drop=True)

    df = df_city[["lat", "lng"]]
    coordinates = list(df.itertuples(index=False, name=None))
    coordinates = [f"{c[1]},{c[0]}" for c in coordinates]
    coordinates = ';'.join(coordinates)

    response_distances = get_matrix(coordinates)
    distances = np.array(response_distances["distances"]).astype(int)
    df_city.name[optimize_routes(distances, 0)[:-1]].to_csv(f"data/{city}_routing.csv")
```

5. The optimized routes for each city are saved as `{city}_routing.csv` in the `data/` directory.

## Acknowledgments

The code utilizes the OR-Tools library and the Open Source Routing Machine (OSRM) API for routing optimization. Credits and thanks go to the developers of these tools for their valuable contributions.

## License

This project is licensed under the MIT License - see the LICENSE file for details.