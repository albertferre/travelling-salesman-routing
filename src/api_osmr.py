import requests
import json
import pandas as pd

def get_data():
    df = pd.read_csv("data/places.csv")
    df = df[["lat", "lng"]]


    coordinates = list(df.itertuples(index=False, name=None))
    # print(len(coordinates))
    coordinates = [f"{c[0]},{c[1]}" for c in coordinates][:100]
    coordinates = ';'.join(coordinates)
    return(coordinates)


def get_matrix(coordinates):
    # coordinates = "13.388860,52.517037;13.397634,52.529407;13.428555,52.523219"

    url = f"http://router.project-osrm.org/table/v1/driving/{coordinates}?annotations=distance"
    response = requests.get(url)
    return json.loads(response.text)



if __name__ == "__main__":
    get_matrix(get_data())