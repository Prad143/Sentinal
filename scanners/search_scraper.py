import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from utils.vpn_manager import VPNManager
import config

async def scrape_search_engine(query, engine, num_results=10):
    if engine.lower() == 'google':
        url = f"https://www.google.com/search?q={quote_plus(query)}&num={num_results}"
    elif engine.lower() == 'bing':
        url = f"https://www.bing.com/search?q={quote_plus(query)}&count={num_results}"
    else:
        raise ValueError("Unsupported search engine. Choose 'google' or 'bing'.")

    async with VPNManager(config.VPN_CONFIG_FILES) as vpn_manager:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers={'User-Agent': 'Mozilla/5.0'}) as response:
                soup = BeautifulSoup(await response.text(), 'html.parser')
                
                if engine.lower() == 'google':
                    return [div.a['href'] for div in soup.find_all('div', class_='yuRUbf')]
                else:  # Bing
                    return [a['href'] for a in soup.find_all('a', class_='b_attribution')]

async def search_urls(query, engine='google', num_results=10):
    return await scrape_search_engine(query, engine, num_results)