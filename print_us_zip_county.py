import pandas as pd

# URLs for data
zcta_to_place_url = (
    "http://www2.census.gov/geo/docs/maps-data/data/rel/zcta_place_rel_10.txt"
)
census_codes_to_names_url = "http://www2.census.gov/geo/docs/reference/state.txt"

try:
    # Load relevant data
    df = pd.read_csv(
        zcta_to_place_url, dtype={"ZCTA5": str}, usecols=["ZCTA5", "STATE"]
    )

    # Remove duplicates
    df = df.drop_duplicates()

    # Count each ZCTA appearance
    counts = df["ZCTA5"].value_counts()

    # Get ZCTAs listed more than once
    multi_state_zips = df[df.ZCTA5.isin(counts[counts > 1].index)]

    # Load state names
    states = pd.read_csv(census_codes_to_names_url, sep="|")

    # Merge and print results
    merged = pd.merge(multi_state_zips, states, on="STATE")[["ZCTA5", "STATE_NAME"]]
    print(merged.sort_values(["ZCTA5", "STATE_NAME"]).to_string(index=False))
except Exception as e:
    print("An error occurred:", e)
