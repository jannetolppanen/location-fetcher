# Location Fetcher

A Python tool for fetching location data from OpenStreetMap using the Overpass API. This tool can retrieve data about various locations (churches, police stations, parks, etc.) in different European regions and process the data for further use.

## Features

- Fetch location data from OpenStreetMap using Overpass API
- Support for different types of locations (churches, police stations, parks, schools, etc.)
- Predefined European regions with automatic subarea division to prevent timeout
- Progress tracking during data fetching
- Daily caching of results to prevent unnecessary API calls
- Tools for filtering and analyzing the fetched data

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/location-fetcher.git
cd location-fetcher
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Fetching Data

```python
from services.fetcher import OverpassFetcher

# Initialize fetcher
fetcher = OverpassFetcher()

# Fetch churches in northern Europe
data = fetcher.fetch_data("place_of_worship", "northern_europe")
```

### Processing Data

```python
from services.data_handler import LocationDataHandler

# Initialize handler
handler = LocationDataHandler()

# Filter locations to keep only named ones
new_file = handler.filter_named_locations("place_of_worship_northern_europe_20240224.json")

# View statistics
handler.print_object_counts()
```

## Available Location Types

- place_of_worship
- police
- park
- school
- hospital
- restaurant

## Available Regions

- northern_europe
- central_europe
- southern_europe

## Project Structure

```
location_fetcher/
├── __init__.py
├── main.py
└── services/
    ├── __init__.py
    ├── fetcher.py
    └── data_handler.py
```

## Data Storage

- Raw data is stored in `data_cache/`
- Filtered data is stored in `filtered_data/`
- Both directories are created automatically when needed

## Requirements

- Python 3.6+
- requests
- tqdm

## License

This project is licensed under the MIT License - see the LICENSE file for details.
