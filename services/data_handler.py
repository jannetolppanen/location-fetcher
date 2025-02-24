# location_fetcher/services/data_handler.py
import json
from typing import Dict, List, Optional
from pathlib import Path
import os

class LocationDataHandler:
    def __init__(self, raw_data_dir: str = "data_cache", filtered_data_dir: str = "filtered_data"):
        """Initialize with directories for raw and filtered data"""
        self.raw_data_dir = Path(raw_data_dir)
        self.filtered_data_dir = Path(filtered_data_dir)
        
        # Ensure both directories exist
        self.raw_data_dir.mkdir(exist_ok=True)
        self.filtered_data_dir.mkdir(exist_ok=True)

    def load_data(self, filename: str) -> dict:
        """Load a JSON file from the raw data directory"""
        file_path = self.raw_data_dir / filename
        if not file_path.exists():
            raise FileNotFoundError(f"File {filename} not found in {self.raw_data_dir}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_filtered_data(self, data: dict, original_filename: str, suffix: str = "named_only") -> str:
        """Save filtered data to the filtered data directory"""
        # Create filename for filtered data
        base_name = original_filename.rsplit('.', 1)[0]  # Remove extension
        new_filename = f"{base_name}_{suffix}.json"
        file_path = self.filtered_data_dir / new_filename
        
        # Save the filtered data
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
            
        return new_filename

    def filter_named_locations(self, filename: str) -> str:
        """
        Filter locations that have names and save to a new file.
        Returns the name of the new filtered file.
        """
        # Load the original data
        data = self.load_data(filename)
        
        # Count original elements
        original_count = len(data['elements'])
        
        # Filter elements that have names
        filtered_elements = [
            elem for elem in data['elements']
            if 'tags' in elem and 'name' in elem['tags']
        ]
        
        # Create new data structure
        filtered_data = {
            'version': data.get('version', 0.6),
            'generator': 'Filtered Data',
            'original_file': filename,
            'filter_type': 'named_only',
            'original_count': original_count,
            'filtered_count': len(filtered_elements),
            'elements': filtered_elements
        }
        
        # Save and return the new filename
        new_filename = self.save_filtered_data(filtered_data, filename)
        
        # Print summary
        print(f"Filtering complete:")
        print(f"Original elements: {original_count}")
        print(f"Elements with names: {len(filtered_elements)}")
        print(f"Saved to: {self.filtered_data_dir / new_filename}")
        
        return new_filename
    
    def filter_unnamed_locations(self, filename: str) -> str:
        # Load the original data
        data = self.load_data(filename)
        
        # Count original elements
        original_count = len(data['elements'])
        
        # Filter elements that DON'T have names
        filtered_elements = [
            elem for elem in data['elements']
            if 'tags' not in elem or 'name' not in elem['tags']
        ]
        
        # Create new data structure
        filtered_data = {
            'version': data.get('version', 0.6),
            'generator': 'Filtered Data',
            'original_file': filename,
            'filter_type': 'unnamed_only',
            'original_count': original_count,
            'filtered_count': len(filtered_elements),
            'elements': filtered_elements
        }
        
        # Save with an appropriate suffix
        new_filename = self.save_filtered_data(filtered_data, filename, "unnamed_only")
        
        # Print summary
        print(f"Filtering complete:")
        print(f"Original elements: {original_count}")
        print(f"Elements without names: {len(filtered_elements)}")
        print(f"Saved to: {self.filtered_data_dir / new_filename}")
        
        return new_filename

    def list_raw_files(self) -> List[str]:
        """List all JSON files in the raw data directory"""
        return [f.name for f in self.raw_data_dir.glob("*.json")]

    def list_filtered_files(self) -> List[str]:
        """List all JSON files in the filtered data directory"""
        return [f.name for f in self.filtered_data_dir.glob("*.json")]

    def count_objects(self) -> Dict[str, Dict[str, int]]:
        """
        Count objects in both raw and filtered data directories.
        Returns a dictionary with counts for each file and total counts.
        """
        counts = {
            'raw_data': {'total_objects': 0, 'files': {}},
            'filtered_data': {'total_objects': 0, 'files': {}}
        }
        
        # Count objects in raw data files
        for file in self.raw_data_dir.glob("*.json"):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    num_objects = len(data.get('elements', []))
                    counts['raw_data']['files'][file.name] = num_objects
                    counts['raw_data']['total_objects'] += num_objects
            except json.JSONDecodeError:
                print(f"Error reading file {file.name} in raw data directory")
                counts['raw_data']['files'][file.name] = 0
        
        # Count objects in filtered data files
        for file in self.filtered_data_dir.glob("*.json"):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    num_objects = len(data.get('elements', []))
                    counts['filtered_data']['files'][file.name] = num_objects
                    counts['filtered_data']['total_objects'] += num_objects
            except json.JSONDecodeError:
                print(f"Error reading file {file.name} in filtered data directory")
                counts['filtered_data']['files'][file.name] = 0
        
        return counts

    def print_object_counts(self):
        """Print a formatted summary of object counts in both directories"""
        counts = self.count_objects()
        
        print("\n=== Object Count Summary ===")
        
        print("\nRaw Data Directory:")
        print(f"Total objects: {counts['raw_data']['total_objects']}")
        print("Files:")
        for filename, count in counts['raw_data']['files'].items():
            print(f"  - {filename}: {count} objects")
        
        print("\nFiltered Data Directory:")
        print(f"Total objects: {counts['filtered_data']['total_objects']}")
        print("Files:")
        for filename, count in counts['filtered_data']['files'].items():
            print(f"  - {filename}: {count} objects")

# Usage example:
if __name__ == "__main__":
    # Initialize handler
    handler = LocationDataHandler()
    
    # Show available raw files
    print("Available raw data files:")
    for file in handler.list_raw_files():
        print(f"- {file}")
    
    # Filter a specific file
    if handler.list_raw_files():
        file_to_filter = handler.list_raw_files()[0]
        print(f"\nFiltering file: {file_to_filter}")
        new_file = handler.filter_named_locations(file_to_filter)
        
        # Show filtered files
        print("\nAvailable filtered files:")
        for file in handler.list_filtered_files():
            print(f"- {file}")