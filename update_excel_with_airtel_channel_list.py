import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
import logging

# Set up basic configuration for logging
logging.basicConfig(level=logging.INFO, format="%(message)s")

# URL of the webpage to scrape
url = "https://www.airtel.in/plans/dth/all-channel-list"

# Send a request to fetch the webpage
response = requests.get(url)
webpage = response.content

# Parse the webpage with BeautifulSoup
soup = BeautifulSoup(webpage, "html.parser")


# Function to clean channel names using regex
def clean_channel_name(name):
    # Removing patterns like ' @ FREE', '@ FREE', ' Rs 19', ' Rs 22.03', ' Rs 17'
    name = re.sub(r"\s*@ Free| Rs \d+(\.\d+)?", "", name, flags=re.IGNORECASE)
    return name


# Function to compare and report changes
def compare_and_report(new_data, old_data):
    new_set = set(new_data["Channel Number"])
    old_set = set(old_data["Channel Number"])

    new_channels = new_set - old_set
    deleted_channels = old_set - new_set
    updated_channels = []

    for ch_num in new_set & old_set:
        new_row = new_data[new_data["Channel Number"] == ch_num].iloc[0]
        old_row = old_data[old_data["Channel Number"] == ch_num].iloc[0]

        if not new_row.equals(old_row):
            updated_channels.append(ch_num)

    if new_channels or deleted_channels or updated_channels:
        logging.info("🔄 Changes detected:")
        if new_channels:
            logging.info(f"✨ New channels added: {sorted(list(new_channels))}")
        if deleted_channels:
            logging.info(f"🗑️ Channels deleted: {sorted(list(deleted_channels))}")
        if updated_channels:
            logging.info(f"🔧 Channels updated: {sorted(updated_channels)}")
    else:
        logging.info("👍 No changes detected in the channel list.")


# File path
file_path = r"C:\Users\lkaura\Desktop\Scripts\resources\Airtel_DTH_Channel_List.xlsx"

# Find all elements that could either be a channel or a language header
elements = soup.find_all(
    ["div", "span"], class_=["pack-inner-item", "accordion__header-2"]
)

# List to hold channel data
channel_data = []
current_language = ""

for element in elements:
    # Check if the element is a language header
    if "accordion__header-2" in element.get("class", []):
        current_language = element.span.text.strip()
    elif "pack-inner-item" in element.get("class", []):
        # It's a channel item
        hd_sd = element.find("div", class_="left-part").p.text.strip()
        channel_number = element.find("div", class_="right-part").p.text.strip()
        channel_logo = element.find("div", class_="image-part").img["src"].strip()
        channel_name = clean_channel_name(
            element.find("div", class_="data-box-2").p.text.strip()
        )
        genre = element.find("div", class_="pack-inner-bottom-text").div.p.text.strip()
        price = (
            element.find("div", class_="pack-inner-bottom-text")
            .find_all("p")[-1]
            .text.strip()
        )

        channel_data.append(
            {
                "Language": current_language,
                "Genre": genre,
                "Channel Name": channel_name,
                "Channel Number": channel_number,
                "SD/HD": hd_sd,
                "Price": price,
                "Channel Logo": channel_logo,
            }
        )

# Convert the data into a pandas DataFrame
df = pd.DataFrame(channel_data)

# Convert Channel Number to integer for proper sorting
df["Channel Number"] = pd.to_numeric(df["Channel Number"], errors="coerce")

# Sort the DataFrame by Channel Number in ascending order
df.sort_values(by="Channel Number", inplace=True)

# Check if the file exists
if os.path.exists(file_path):
    logging.info("📂 Existing file found. Comparing data...")
    existing_data = pd.read_excel(file_path)
    compare_and_report(df, existing_data)
else:
    logging.info("🆕 No existing file found. Creating new file.")

# Save the new data
df.to_excel(file_path, index=False)
logging.info("✔️ Data scraping and processing completed successfully.")
