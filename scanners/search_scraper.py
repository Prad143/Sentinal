import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

async def scrape_google(query, num_results=10):
    url = f"https://www.google.com/search?q={quote_plus(query)}&num={num_results}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers={'User-Agent': 'Mozilla/5.0'}) as response:
            soup = BeautifulSoup(await response.text(), 'html.parser')
            return [div.a['href'] for div in soup.find_all('div', class_='yuRUbf')]

async def scrape_bing(query, num_results=10):
    url = f"https://www.bing.com/search?q={quote_plus(query)}&count={num_results}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers={'User-Agent': 'Mozilla/5.0'}) as response:
            soup = BeautifulSoup(await response.text(), 'html.parser')
            return [a['href'] for a in soup.find_all('a', class_='b_attribution')]

async def search_urls(query, engine='google', num_results=10):
    if engine.lower() == 'google':
        return await scrape_google(query, num_results)
    elif engine.lower() == 'bing':
        return await scrape_bing(query, num_results)
    else:
        raise ValueError("Unsupported search engine. Choose 'google' or 'bing'.")