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

def get_user_input():
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

def print_progress(message):
    sys.stdout.write(f"\r{message}")
    sys.stdout.flush()

def print_completion(message):
    print(f"\n{message}")