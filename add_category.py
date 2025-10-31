"""
Helper script to easily add new categories to the scraper
"""

import json
import sys

def add_category():
    print("="*60)
    print("ADD NEW CATEGORY TO UNIVERSAL SCRAPER")
    print("="*60)
    print()
    
    # Get category details
    category_key = input("Category key (e.g., 'python_tutorials'): ").strip()
    if not category_key:
        print("Category key is required!")
        return
    
    query = input("Search query (e.g., 'python programming tutorials'): ").strip()
    if not query:
        print("Search query is required!")
        return
    
    print("\nAvailable platforms:")
    platforms_list = ["youtube", "wikipedia", "google", "spotify", "imdb"]
    for i, p in enumerate(platforms_list, 1):
        print(f"  {i}. {p}")
    
    platforms_input = input("\nEnter platform numbers (comma-separated, e.g., 1,2,3): ").strip()
    try:
        platform_indices = [int(x.strip()) - 1 for x in platforms_input.split(',')]
        platforms = [platforms_list[i] for i in platform_indices if 0 <= i < len(platforms_list)]
    except:
        print("Invalid input. Using default: youtube, wikipedia, google")
        platforms = ["youtube", "wikipedia", "google"]
    
    category_type = input("Type (e.g., 'education', 'music', 'movie') [default: 'general']: ").strip() or "general"
    
    # Create category entry
    category_entry = f'''    "{category_key}": {{
        "query": "{query}",
        "platforms": {json.dumps(platforms)},
        "type": "{category_type}"
    }}'''
    
    print("\n" + "="*60)
    print("CATEGORY TO ADD:")
    print("="*60)
    print(category_entry)
    print()
    
    confirm = input("Add this category? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("Cancelled.")
        return
    
    # Read current config
    try:
        with open('generic_config.py', 'r', encoding='utf-8') as f:
            config_content = f.read()
    except Exception as e:
        print(f"Error reading config file: {e}")
        return
    
    # Find the GLOBAL_CATEGORIES section and add new category
    # Look for the last category entry before the closing brace
    if '"your_category"' in config_content:
        # Replace the example with our new category
        config_content = config_content.replace(
            '    # Add YOUR custom categories here:\n    # "your_category": {',
            f'    # Add YOUR custom categories here:\n    {category_entry},\n    "your_category": {{'
        )
    else:
        # Find the last category before the closing brace
        last_bracket = config_content.rfind('}')
        before_bracket = config_content[:last_bracket]
        after_bracket = config_content[last_bracket:]
        
        # Add comma and new category
        if before_bracket.rstrip().endswith('}'):
            # Need to add comma first
            before_bracket = before_bracket.rstrip()[:-1] + ',\n' + category_entry + '\n}'
            config_content = before_bracket + after_bracket
        else:
            config_content = before_bracket + ',\n' + category_entry + after_bracket
    
    # Write back
    try:
        with open('generic_config.py', 'w', encoding='utf-8') as f:
            f.write(config_content)
        print("\n✅ Category added successfully!")
        print(f"   Key: {category_key}")
        print(f"   Query: {query}")
        print(f"   Platforms: {', '.join(platforms)}")
        print("\n   You can now run: python universal_main.py")
    except Exception as e:
        print(f"\n❌ Error writing to config file: {e}")
        print("\nPlease manually add this to generic_config.py:")
        print(category_entry)

if __name__ == "__main__":
    try:
        add_category()
    except KeyboardInterrupt:
        print("\n\nCancelled.")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

