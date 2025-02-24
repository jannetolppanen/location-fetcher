# Overpass Location Data Fetcher

A Python application for fetching and processing location data from OpenStreetMap using the Overpass API.

## Features

- Fetch location data for different types of places (churches, police stations, parks, etc.)
- Divides large areas into manageable subareas to avoid API timeouts
- Caches results locally to avoid unnecessary API calls
- Shows detailed progress and status updates during fetching
- Handles errors gracefully with automatic retries

## Installation

1. Clone the repository
2. Install required packages:
```bash
pip install requests tqdm
```

## Usage

### Basic Usage

```python
from services.fetcher import OverpassFetcher

# Initialize the fetcher
fetcher = OverpassFetcher()

# Fetch all churches in northern Europe
data = fetcher.fetch_data("place_of_worship", "northern_europe")

# Data is returned as a JSON string, you might want to parse it:
import json
locations = json.loads(data)
print(f"Found {len(locations['elements'])} locations")
```

### Available Location Types

The following location types are currently supported:

| Type | Tag Key | Tag Value |
|------|---------|-----------|
| Churches/Temples | amenity | place_of_worship |
| Police Stations | amenity | police |
| Parks | leisure | park |
| Schools | amenity | school |
| Hospitals | amenity | hospital |
| Restaurants | amenity | restaurant |

To fetch different types of locations, simply use the type name as defined in the fetcher:
```python
# Fetch police stations
police_data = fetcher.fetch_data("police", "central_europe")

# Fetch parks
parks_data = fetcher.fetch_data("park", "southern_europe")
```

### Available Areas

The following geographic areas are predefined:

1. Northern Europe
   - Bounds: 55.0°N to 71.0°N, 4.0°E to 32.0°E
   - Divided into 4 subareas

2. Central Europe
   - Bounds: 45.0°N to 55.0°N, 6.0°E to 24.0°E
   - Divided into 4 subareas

3. Southern Europe
   - Bounds: 35.0°N to 45.0°N, -10.0°E to 28.0°E
   - Divided into 4 subareas

### Caching

- Results are cached by default in the `data_cache` directory
- Cache files are named using the pattern: `{location_type}_{area}_{date}.json`
- Cache files are valid for one day
- You can specify a different cache directory when initializing:
```python
fetcher = OverpassFetcher(cache_dir="my_custom_cache")
```

### Progress Tracking

The fetcher provides detailed progress information:
- Overall progress across subareas
- Download progress for each request
- Number of elements found in each subarea
- Error messages and retry attempts

Example output:
```
Fetching place_of_worship data for northern_europe
Total subareas to process: 4

Processing subarea 1/4
Bounds: 55.00°N, 4.00°E to 63.00°N, 18.00°E
Sending request... (attempt 1/3)
Downloading data: 100%|██████████| 2.34M/2.34M [00:02<00:00, 1.02MB/s]
Found 1234 elements in this subarea
```

### Error Handling

- Automatic retries (3 attempts by default)
- 5-second delay between retries
- Continues to next subarea if one fails
- Detailed error messages

## Project Structure

```
location_fetcher/
├── __init__.py
├── main.py
└── services/
    ├── __init__.py
    └── fetcher.py
```

## Adding New Location Types

To add support for new location types, modify the tag mappings in `fetcher.py`:

```python
def get_tag_key(self, node_type: str) -> str:
    tag_mapping = {
        "new_type": "appropriate_key",  # Add your new type here
        "place_of_worship": "amenity",
        "police": "amenity",
        # ...
    }
    return tag_mapping.get(node_type, node_type)

def get_tag_value(self, node_type: str) -> str:
    value_mapping = {
        "new_type": "appropriate_value",  # Add your new type here
        "place_of_worship": "place_of_worship",
        "police": "police",
        # ...
    }
    return value_mapping.get(node_type, node_type)
```

## Adding New Areas

To add new geographic areas, modify the areas dictionary in the OverpassFetcher class:

```python
self.areas["new_area"] = {
    "bounds": (min_lat, min_lon, max_lat, max_lon),
    "subareas": [
        (subarea1_min_lat, subarea1_min_lon, subarea1_max_lat, subarea1_max_lon),
        (subarea2_min_lat, subarea2_min_lon, subarea2_max_lat, subarea2_max_lon),
        # ...
    ]
}
```

## Future Enhancements

- Addition of more location types
- Support for more geographic regions
- Advanced filtering options
- Custom query building

## Limitations

- API rate limits apply
- Large areas need to be divided into subareas
- Some data might be incomplete or missing
- Cache files can grow large for extensive queries

## Troubleshooting

If you encounter timeouts:
- The area might be too large - try using a smaller area
- The API might be busy - the fetcher will automatically retry
- Check your internet connection

If data is missing:
- Verify the location type is correctly mapped
- Check if the area coordinates are correct
- Some locations might not be tagged in OpenStreetMap
