import json
from pprint import pprint
from typing import List, Dict
from collections import Counter

def analyze_data(filepath: str):
    """Analyze and display JSON data in a readable format"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    elements = data['elements']
    
    # Basic statistics
    print(f"\n=== Basic Statistics ===")
    print(f"Total number of elements: {len(elements)}")
    
    # Count elements by type
    type_counts = Counter(elem['type'] for elem in elements)
    print("\n=== Element Types ===")
    for type_name, count in type_counts.items():
        print(f"{type_name}: {count}")
    
    # Analyze available tags
    all_tags = set()
    for elem in elements:
        if 'tags' in elem:
            all_tags.update(elem['tags'].keys())
    
    print("\n=== Available Tags ===")
    print(", ".join(sorted(all_tags)))
    
    # Show 3 sample elements with full details
    print("\n=== Sample Elements (first 3) ===")
    for elem in elements[:3]:
        pprint(elem)
        print("-" * 50)
    
    # Summary of religious buildings
    religions = Counter(elem.get('tags', {}).get('religion') for elem in elements)
    print("\n=== Religions ===")
    for religion, count in religions.items():
        if religion:  # Skip None values
            print(f"{religion}: {count}")
    
    # Summary of denominations
    denominations = Counter(elem.get('tags', {}).get('denomination') for elem in elements)
    print("\n=== Denominations ===")
    for denomination, count in denominations.items():
        if denomination:  # Skip None values
            print(f"{denomination}: {count}")

def search_locations(filepath: str, search_term: str):
    """Search for locations containing the search term in their name"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"\n=== Search Results for '{search_term}' ===")
    for elem in data['elements']:
        name = elem.get('tags', {}).get('name', '')
        if name and search_term.lower() in name.lower():
            print(f"\nName: {name}")
            print(f"Location: {elem.get('lat')}, {elem.get('lon')}")
            print(f"Tags: {elem.get('tags')}")
            print("-" * 50)

if __name__ == "__main__":
    filepath = "filtered_data\place_of_worship_central_europe_20250224_named_only.json"  # Change this to your JSON file path
    
    print("1. Analyze all data")
    print("2. Search for specific locations")
    choice = input("Choose an option (1/2): ")
    
    if choice == "1":
        analyze_data(filepath)
    elif choice == "2":
        search_term = input("Enter search term: ")
        search_locations(filepath, search_term)
    else:
        print("Invalid choice")