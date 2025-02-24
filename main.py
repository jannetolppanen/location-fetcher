from services.fetcher import OverpassFetcher
from services.data_handler import LocationDataHandler

def fetch_example():
    """Example of fetching data"""
    fetcher = OverpassFetcher()
    
    # Fetch churches in northern Europe
    data = fetcher.fetch_data("place_of_worship", "northern_europe")
    print("Fetched data successfully")
    
    return data

def analyze_example(filename: str):
    """Example of analyzing previously fetched data"""
    handler = LocationDataHandler()
    
    # Load and analyze the data
    data = handler.load_data(filename)
    
    # Get basic statistics
    stats = handler.get_statistics(data)
    print("\nDataset Statistics:")
    print(f"Total elements: {stats['total_elements']}")
    print(f"Elements with names: {stats['elements_with_names']}")
    
    # Find specific locations
    filtered = handler.filter_by_tags(data, {"religion": "christian"})
    print(f"\nFound {len(filtered['elements'])} Christian places of worship")

if __name__ == "__main__":
# Create the handler
    handler = LocationDataHandler()

    # You can also compare both filters on the same file:
    named_file = handler.filter_named_locations("hospital_northern_europe_20250224.json")
    unnamed_file = handler.filter_unnamed_locations("hospital_northern_europe_20250224.json")

    # Check the counts in both directories
    handler.print_object_counts()

    # Get counts as data
    # counts = handler.count_objects()
    # print(f"Total raw objects: {counts['raw_data']['total_objects']}")
    # print(f"Total filtered objects: {counts['filtered_data']['total_objects']}")

    # Or get a nicely formatted print out
    # handler.print_object_counts()

    # See what raw files you have
    # raw_files = handler.list_raw_files()
    # print("Available raw files:", raw_files)
    # Might show: ['churches_northern_europe_20240224.json', 'parks_central_europe_20240224.json']

    # Filter one file to keep only named locations
    # new_file = handler.filter_named_locations("hospital_northern_europe_20250224.json")
    # This will:
    # 1. Load the original churches file
    # 2. Filter out any churches without names
    # 3. Save to something like: 'churches_northern_europe_20240224_named_only.json'
    # 4. Print a summary of how many locations were kept/removed

    # See your filtered files
    # filtered_files = handler.list_filtered_files()
    # print("Available filtered files:", filtered_files)

    # fetcher = OverpassFetcher()
    

    # Fetch all places of worship in northern Europe
    # data = fetcher.fetch_data("hospital", "northern_europe")