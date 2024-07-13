import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import concurrent.futures
import itertools
import sys
import time

def find_urls(start_url, max_recursion_level):
    visited_urls = set()
    
    def crawl_website(url, current_level):
        if current_level > max_recursion_level or url in visited_urls:
            return []
        
        visited_urls.add(url)
        found_urls = [url]
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    full_url = urljoin(url, href)
                    parsed_url = urlparse(full_url)
                    if parsed_url.netloc == urlparse(start_url).netloc:
                        found_urls.extend(crawl_website(full_url, current_level + 1))
        except requests.RequestException:
            pass
        
        return found_urls
    
    def run_animation():
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if crawl_future.done():
                break
            sys.stdout.write('\rCrawling ' + c)
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write('\rCrawling complete!\n')
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        crawl_future = executor.submit(crawl_website, start_url, 0)
        animation_future = executor.submit(run_animation)
        
        urls = crawl_future.result()
        animation_future.result()  # Wait for animation to complete
    
    return sorted(set(urls))

if __name__ == "__main__":
    # This allows the script to be run standalone for testing
    import argparse
    from utils.file_operations import write_urls_to_file
    
    parser = argparse.ArgumentParser(description="Find URLs on a website.")
    parser.add_argument("url", help="The starting URL to crawl")
    parser.add_argument("--max-level", type=int, default=3, help="Maximum recursion level")
    parser.add_argument("--output", default="output.txt", help="Output file name")
    args = parser.parse_args()
    
    urls = find_urls(args.url, args.max_level)
    write_urls_to_file(urls, args.output)
    print(f"Found {len(urls)} unique URLs. Results written to {args.output}")