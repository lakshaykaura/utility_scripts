import requests
import pandas as pd

# Insert your API Key here
API_KEY = "6dc386525fd408bea8e234f980afc521abf8cd37"

# Define the base URL for the API endpoint
base_url = "https://api.census.gov/data/2022/acs/acs5"


# Function to make API requests
def get_census_data(url, params):
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return pd.DataFrame(response.json()[1:], columns=response.json()[0])
    else:
        print("Failed to retrieve data:", response.status_code)
        return pd.DataFrame()


# Retrieve state and county names
state_county_data = get_census_data(
    base_url, {"get": "NAME,GEO_ID", "for": "county:*", "in": "state:*", "key": API_KEY}
)

# If state and county data is retrieved successfully
if not state_county_data.empty:
    # Splitting the 'NAME' column to get state and county names
    state_county_data[["County", "State"]] = state_county_data["NAME"].str.split(
        ",", expand=True
    )

    # Retrieve ZCTA-level data
    zcta_data = get_census_data(
        base_url, {"get": "GEO_ID", "for": "zip code tabulation area:*", "key": API_KEY}
    )

    # If ZCTA data is retrieved successfully
    if not zcta_data.empty:
        # Extracting the ZIP Code from GEO_ID
        zcta_data["ZIPCode"] = zcta_data["GEO_ID"].str[7:]

        # NOTE: At this point, you have two separate dataframes:
        # `state_county_data` with state and county names
        # `zcta_data` with ZIP codes

        # To associate ZIP codes with counties, you would need an additional crosswalk or mapping
        # between ZIP codes and counties as this information is not directly available from the API

        # For demonstration, let's just print the first few rows of each dataframe
        print("State and County Data:")
        print(state_county_data.head())
        print("\nZCTA Data:")
        print(zcta_data.head())

        # Here you would implement your logic to merge or map these datasets based on your available resources or crosswalks
    else:
        print("Failed to retrieve ZCTA data.")
else:
    print("Failed to retrieve state and county data.")
