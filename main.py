import asyncio
from celery.result import AsyncResult
from utils import ui, file_operations
import config
from scanners.url_finder import find_urls_task
from tasks import (
    search_urls_task,
    scan_javascript_task,
    analyze_javascript_task,
    filter_output_task,
    interpret_results_task
)

async def scan_url(url, max_recursion_level):
    ui.print_progress("Crawling website for URLs...")
    task = find_urls_task.delay(url, max_recursion_level)
    urls = await wait_for_task(task)
    file_operations.write_urls_to_file(urls, config.FILE_NAME)
    ui.print_completion(f"Found {len(urls)} unique URLs. Results written to {config.FILE_NAME}")
    return urls

async def wait_for_task(task):
    return await asyncio.to_thread(task.get, timeout=None)

async def main():
    ui.print_banner()
    
    scan_type = ui.get_scan_type()
    
    if scan_type == 1:
        url, max_recursion_level = ui.get_custom_url_input()
        urls = await scan_url(url, max_recursion_level)
    else:
        query, engine, num_results = ui.get_search_input()
        ui.print_progress(f"Searching {engine} for '{query}'...")
        task = search_urls_task.delay(query, engine, num_results)
        urls = await wait_for_task(task)
        file_operations.write_urls_to_file(urls, config.FILE_NAME)
        ui.print_completion(f"Found {len(urls)} URLs from {engine} search. Results written to {config.FILE_NAME}")
    
    ui.print_progress("Scanning JavaScript files...")
    task = scan_javascript_task.delay(config.FILE_NAME, config.JS_SCANNER_FILE_NAME)
    await wait_for_task(task)
    ui.print_completion("JavaScript scanning complete.")
    
    ui.print_progress("Analyzing JavaScript with LLM...")
    task = analyze_javascript_task.delay(config.JS_UNIQUE_FILE_NAME)
    analysis_file = await wait_for_task(task)
    if analysis_file:
        ui.print_completion(f"LLM analysis complete. Results written to {analysis_file}")
    else:
        ui.print_completion("LLM analysis failed.")
        return
    
    ui.print_progress("Filtering LLM output...")
    task = filter_output_task.delay(config.LLM_FILE_NAME)
    await wait_for_task(task)
    ui.print_completion("Filtering complete.")
    
    ui.print_progress("Interpreting results...")
    task = interpret_results_task.delay(
        config.JS_UNIQUE_FILE_NAME,
        config.JS_URL_FILE_NAME,
        config.CLEAN_UP_FILE_NAME
    )
    await wait_for_task(task)
    ui.print_completion("Results interpretation complete.")
    
    file_operations.clean_up_files(config.CLEAN_UP_FILE_NAME)
    ui.print_completion("Temporary files cleaned up.")
    
    ui.print_completion(f"Scan complete. Final results can be found in {config.CLEAN_UP_FILE_NAME}")

if __name__ == "__main__":
    asyncio.run(main())