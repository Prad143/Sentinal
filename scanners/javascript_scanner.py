import asyncio
import aiohttp
from bs4 import BeautifulSoup
from utils.file_operations import read_urls_from_file, write_to_file
from utils.vpn_manager import VPNManager
import config
from celery_app import app

async def extract_js_content(html, url):
    soup = BeautifulSoup(html, 'html.parser')
    external_js = []
    inline_js = []

    for script in soup.find_all('script'):
        if script.get('src'):
            js_url = script['src']
            if not js_url.startswith(('http://', 'https://')):
                js_url = f"{url.rstrip('/')}/{js_url.lstrip('/')}"
            external_js.append(js_url)
        elif script.string:
            inline_js.append(script.string)

    return external_js, inline_js

async def fetch_js_content(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                return await response.text()
    except Exception as e:
        print(f"Error fetching JavaScript from {url}: {str(e)}")
    return None

async def scan_single_url(url, all_js_content, js_url_mapping, session):
    try:
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                html = await response.text()
                external_js, inline_js = await extract_js_content(html, url)
                
                for js_url in external_js:
                    js_content = await fetch_js_content(session, js_url)
                    if js_content:
                        all_js_content.add(js_content)
                        if js_content not in js_url_mapping:
                            js_url_mapping[js_content] = []
                        js_url_mapping[js_content].append(js_url)
                
                for js in inline_js:
                    all_js_content.add(js)
                    if js not in js_url_mapping:
                        js_url_mapping[js] = []
                    js_url_mapping[js].append(f"{url} (inline)")
    except Exception as e:
        print(f"Error scanning {url}: {str(e)}")

@app.task
async def scan_javascript(input_file, output_file):
    urls = read_urls_from_file(input_file)
    all_js_content = set()
    js_url_mapping = {}

    async with VPNManager(config.VPN_CONFIG_FILES) as vpn_manager:
        async with aiohttp.ClientSession() as session:
            tasks = []
            for url in urls:
                tasks.append(scan_single_url(url, all_js_content, js_url_mapping, session))
                if len(tasks) >= config.VPN_ROTATION_INTERVAL:
                    await asyncio.gather(*tasks)
                    tasks = []
                    await vpn_manager.rotate()
            
            if tasks:
                await asyncio.gather(*tasks)

    # Write unique JavaScript content to file
    write_to_file(output_file, "\n".join(all_js_content))

    # Write JavaScript URL mapping to file
    url_mapping_file = output_file.replace('.txt', '_url_mapping.txt')
    with open(url_mapping_file, 'w') as f:
        for content, urls in js_url_mapping.items():
            f.write(f"Content Hash: {hash(content)}\n")
            f.write("URLs:\n")
            for url in urls:
                f.write(f"- {url}\n")
            f.write("\n")

    print(f"JavaScript scanning complete. Results written to {output_file} and {url_mapping_file}")
    return output_file, url_mapping_file

if __name__ == "__main__":
    # This allows the script to be run standalone for testing
    from config import FILE_NAME, JS_SCANNER_FILE_NAME
    asyncio.get_event_loop().run_until_complete(scan_javascript(FILE_NAME, JS_SCANNER_FILE_NAME))