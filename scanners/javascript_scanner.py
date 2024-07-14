import asyncio
import pyppeteer
import re
from urllib.parse import urljoin
from utils.file_operations import read_urls_from_file, write_to_file

async def extract_js_content(page, url):
    # Extract external JavaScript
    script_tags = await page.evaluate('''() => {
        return Array.from(document.getElementsByTagName('script'))
            .filter(script => script.src)
            .map(script => script.src);
    }''')
    
    external_js = []
    for src in script_tags:
        full_url = urljoin(url, src)
        js_content = await fetch_js_content(full_url)
        if js_content:
            external_js.append((full_url, js_content))
    
    # Extract inline JavaScript
    inline_js = await page.evaluate('''() => {
        return Array.from(document.getElementsByTagName('script'))
            .filter(script => !script.src)
            .map(script => script.innerHTML);
    }''')
    
    return external_js, inline_js

async def fetch_js_content(url):
    try:
        browser = await pyppeteer.launch()
        page = await browser.newPage()
        response = await page.goto(url)
        content = await response.text()
        await browser.close()
        return content
    except Exception:
        return None

async def scan_single_url(url, all_js_content, js_url_mapping):
    try:
        browser = await pyppeteer.launch()
        page = await browser.newPage()
        await page.goto(url)
        
        external_js, inline_js = await extract_js_content(page, url)
        
        for js_url, js_content in external_js:
            all_js_content.add(js_content)
            if js_content not in js_url_mapping:
                js_url_mapping[js_content] = []
            js_url_mapping[js_content].append(js_url)
        
        for js in inline_js:
            all_js_content.add(js)
            if js not in js_url_mapping:
                js_url_mapping[js] = []
            js_url_mapping[js].append(f"{url} (inline)")
        
        await browser.close()
    except Exception as e:
        print(f"Error scanning {url}: {str(e)}")

async def scan_javascript(input_file, output_file):
    urls = read_urls_from_file(input_file)
    all_js_content = set()
    js_url_mapping = {}

    tasks = [scan_single_url(url, all_js_content, js_url_mapping) for url in urls]
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

if __name__ == "__main__":
    # This allows the script to be run standalone for testing
    from config import FILE_NAME, JS_SCANNER_FILE_NAME
    asyncio.get_event_loop().run_until_complete(scan_javascript(FILE_NAME, JS_SCANNER_FILE_NAME))