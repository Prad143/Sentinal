import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from utils.ui import print_progress

async def find_urls(start_url, max_recursion_level):
    visited_urls = set()
    all_urls = set()
    
    async def crawl_website(url, current_level):
        if current_level > max_recursion_level or url in visited_urls:
            return
        
        visited_urls.add(url)
        all_urls.add(url)
        
        print_progress(f"Crawling: {url}")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        tasks = []
                        for link in soup.find_all('a', href=True):
                            href = link['href']
                            full_url = urljoin(url, href)
                            parsed_url = urlparse(full_url)
                            if parsed_url.netloc == urlparse(start_url).netloc:
                                tasks.append(crawl_website(full_url, current_level + 1))
                        await asyncio.gather(*tasks)
        except aiohttp.ClientError as e:
            print(f"Error crawling {url}: {str(e)}")
        except Exception as e:
            print(f"Unexpected error crawling {url}: {str(e)}")
    
    await crawl_website(start_url, 0)
    return sorted(all_urls)

async def main(url, max_recursion_level):
    urls = await find_urls(url, max_recursion_level)
    print(f"\nFound {len(urls)} unique URLs:")
    for url in urls:
        print(url)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python url_finder.py <start_url> <max_recursion_level>")
        sys.exit(1)
    
    start_url = sys.argv[1]
    max_recursion_level = int(sys.argv[2])
    
    asyncio.run(main(start_url, max_recursion_level))