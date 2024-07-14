import sys

def print_banner():
    banner = """
    ╔═══════════════════════════════════════════════╗
    ║                                               ║
    ║   Web Vulnerability Scanner                   ║
    ║   Powered by AI                               ║
    ║                                               ║
    ╚═══════════════════════════════════════════════╝
    """
    print(banner)

def get_scan_type():
    while True:
        print("\nChoose a scan type:")
        print("1. Scan a custom URL")
        print("2. Search and scan multiple URLs")
        choice = input("Enter your choice (1 or 2): ").strip()
        if choice in ['1', '2']:
            return int(choice)
        print("Invalid choice. Please enter 1 or 2.")

def get_custom_url_input():
    url = input("Enter the URL to scan: ").strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    while True:
        try:
            max_recursion_level = int(input("Enter the maximum recursion level (1-5): "))
            if 1 <= max_recursion_level <= 5:
                break
            else:
                print("Please enter a number between 1 and 5.")
        except ValueError:
            print("Please enter a valid number.")
    
    return url, max_recursion_level

def get_search_input():
    query = input("Enter your search query: ").strip()
    engine = input("Choose search engine (google/bing): ").lower()
    while engine not in ['google', 'bing']:
        print("Invalid choice. Please enter 'google' or 'bing'.")
        engine = input("Choose search engine (google/bing): ").lower()
    
    while True:
        try:
            num_results = int(input("Enter the number of results to scan (1-20): "))
            if 1 <= num_results <= 20:
                break
            else:
                print("Please enter a number between 1 and 20.")
        except ValueError:
            print("Please enter a valid number.")
    
    return query, engine, num_results

def print_progress(message):
    sys.stdout.write(f"\r{message}")
    sys.stdout.flush()

def print_completion(message):
    print(f"\n{message}")