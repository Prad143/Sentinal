import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from utils.ui import print_progress
from utils.vpn_manager import VPNManager
import config

async def find_urls(start_url, max_recursion_level):
    visited_urls = set()
    all_urls = set()
    request_count = 0
    
    async with VPNManager(config.VPN_CONFIG_FILES) as vpn_manager:
        async def crawl_website(url, current_level):
            nonlocal request_count
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
                            
                            request_count += 1
                            if request_count >= config.VPN_ROTATION_INTERVAL:
                                await vpn_manager.rotate()
                                request_count = 0
                            
                            await asyncio.gather(*tasks)
            except aiohttp.ClientError as e:
                print(f"Error crawling {url}: {str(e)}")
            except Exception as e:
                print(f"Unexpected error crawling {url}: {str(e)}")
    
    return sorted(all_urls)