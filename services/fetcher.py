import os
from datetime import datetime
import requests
from typing import Dict, List, Tuple
import json
from tqdm import tqdm
import time

class OverpassFetcher:
    def __init__(self, cache_dir: str = "data_cache"):
        self.cache_dir = cache_dir
        self.ensure_cache_directory()
        
        self.areas: Dict[str, Dict] = {
            "northern_europe": {
                "bounds": (55.0, 4.0, 71.0, 32.0),
                "subareas": [
                    (55.0, 4.0, 63.0, 18.0),
                    (63.0, 4.0, 71.0, 18.0),
                    (55.0, 18.0, 63.0, 32.0),
                    (63.0, 18.0, 71.0, 32.0)
                ]
            },
            "central_europe": {
                "bounds": (45.0, 6.0, 55.0, 24.0),
                "subareas": [
                    (45.0, 6.0, 50.0, 15.0),
                    (50.0, 6.0, 55.0, 15.0),
                    (45.0, 15.0, 50.0, 24.0),
                    (50.0, 15.0, 55.0, 24.0)
                ]
            },
            "southern_europe": {
                "bounds": (35.0, -10.0, 45.0, 28.0),
                "subareas": [
                    (35.0, -10.0, 40.0, 9.0),
                    (40.0, -10.0, 45.0, 9.0),
                    (35.0, 9.0, 40.0, 28.0),
                    (40.0, 9.0, 45.0, 28.0)
                ]
            }
        }
        
    def ensure_cache_directory(self):
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def get_subareas(self, area_name: str) -> List[Tuple[float, float, float, float]]:
        """Get the list of subareas for a predefined area"""
        if area_name not in self.areas:
            raise ValueError(f"Unknown area: {area_name}. Available areas: {list(self.areas.keys())}")
        return self.areas[area_name]["subareas"]

    def get_tag_key(self, node_type: str) -> str:
        tag_mapping = {
            "place_of_worship": "amenity",
            "police": "amenity",
            "park": "leisure",
            "school": "amenity",
            "hospital": "amenity",
            "restaurant": "amenity",
        }
        return tag_mapping.get(node_type, node_type)

    def get_tag_value(self, node_type: str) -> str:
        value_mapping = {
            "place_of_worship": "place_of_worship",
            "police": "police",
            "park": "park",
            "school": "school",
            "hospital": "hospital",
            "restaurant": "restaurant",
        }
        return value_mapping.get(node_type, node_type)

    def build_query(self, node_type: str, bounds: Tuple[float, float, float, float]) -> str:
        min_lat, min_lon, max_lat, max_lon = bounds
        
        query = f"""
            [out:json][timeout:300];
            (
              node["{self.get_tag_key(node_type)}"="{self.get_tag_value(node_type)}"]
                ({min_lat},{min_lon},{max_lat},{max_lon});
              way["{self.get_tag_key(node_type)}"="{self.get_tag_value(node_type)}"]
                ({min_lat},{min_lon},{max_lat},{max_lon});
              relation["{self.get_tag_key(node_type)}"="{self.get_tag_value(node_type)}"]
                ({min_lat},{min_lon},{max_lat},{max_lon});
            );
            out body;
            >;
            out skel qt;
        """
        return query

    def fetch_with_progress(self, query: str, retries: int = 3, delay: int = 5) -> dict:
        for attempt in range(retries):
            try:
                print(f"Sending request... (attempt {attempt + 1}/{retries})")
                response = requests.post(
                    "https://overpass-api.de/api/interpreter",
                    data={"data": query},
                    timeout=60,
                    stream=True
                )
                response.raise_for_status()
                
                total_size = int(response.headers.get('content-length', 0))
                block_size = 1024
                progress_bar = tqdm(
                    total=total_size,
                    unit='iB',
                    unit_scale=True,
                    desc="Downloading data"
                )
                
                content = bytearray()
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    content.extend(data)
                
                progress_bar.close()
                return json.loads(content)
                
            except requests.exceptions.RequestException as e:
                print(f"Error during attempt {attempt + 1}: {str(e)}")
                if attempt < retries - 1:
                    print(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    raise

    def fetch_data(self, node_type: str, area_name: str) -> str:
        cache_file = f"{self.cache_dir}/{node_type}_{area_name}_{datetime.now().strftime('%Y%m%d')}.json"
        
        if os.path.exists(cache_file):
            print(f"Using cached data from {cache_file}")
            with open(cache_file, 'r', encoding='utf-8') as f:
                return f.read()
        
        all_elements = []
        subareas = self.get_subareas(area_name)
        
        print(f"\nFetching {node_type} data for {area_name}")
        print(f"Total subareas to process: {len(subareas)}")
        
        for idx, subarea in enumerate(subareas, 1):
            min_lat, min_lon, max_lat, max_lon = subarea
            print(f"\nProcessing subarea {idx}/{len(subareas)}")
            print(f"Bounds: {min_lat:.2f}°N, {min_lon:.2f}°E to {max_lat:.2f}°N, {max_lon:.2f}°E")
            
            query = self.build_query(node_type, subarea)
            try:
                data = self.fetch_with_progress(query)
                elements = data.get("elements", [])
                all_elements.extend(elements)
                print(f"Found {len(elements)} elements in this subarea")
                
            except Exception as e:
                print(f"Error processing subarea {idx}: {str(e)}")
                continue
        
        combined_data = {
            "version": 0.6,
            "generator": "Overpass API",
            "elements": all_elements
        }
        
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(combined_data, f)
        
        return json.dumps(combined_data)

# Example usage:
"""
from services.fetcher import OverpassFetcher

fetcher = OverpassFetcher()

# Fetch all places of worship in northern Europe
data = fetcher.fetch_data("place_of_worship", "northern_europe")
"""