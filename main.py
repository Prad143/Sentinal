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

async def wait_for_task(task):
    try:
        return await asyncio.to_thread(task.get, timeout=None)
    except Exception as e:
        ui.print_error(f"Task failed: {str(e)}")
        return None

async def scan_url(url, max_recursion_level):
    ui.print_progress("Crawling website for URLs...")
    try:
        task = find_urls_task.delay(url, max_recursion_level)
        urls = await wait_for_task(task)
        if urls is None:
            return None
        file_operations.write_urls_to_file(urls, config.FILE_NAME)
        ui.print_completion(f"Found {len(urls)} unique URLs. Results written to {config.FILE_NAME}")
        return urls
    except Exception as e:
        ui.print_error(f"Error during URL scanning: {str(e)}")
        return None

async def main():
    try:
        ui.print_banner()
        
        scan_type = ui.get_scan_type()
        
        if scan_type == 1:
            url, max_recursion_level = ui.get_custom_url_input()
            urls = await scan_url(url, max_recursion_level)
            if urls is None:
                return
        else:
            query, engine, num_results = ui.get_search_input()
            ui.print_progress(f"Searching {engine} for '{query}'...")
            try:
                task = search_urls_task.delay(query, engine, num_results)
                urls = await wait_for_task(task)
                if urls is None:
                    return
                file_operations.write_urls_to_file(urls, config.FILE_NAME)
                ui.print_completion(f"Found {len(urls)} URLs from {engine} search. Results written to {config.FILE_NAME}")
            except Exception as e:
                ui.print_error(f"Error during search: {str(e)}")
                return
        
        ui.print_progress("Scanning JavaScript files...")
        try:
            task = scan_javascript_task.delay(config.FILE_NAME, config.JS_SCANNER_FILE_NAME)
            result = await wait_for_task(task)
            if result is None:
                return
            ui.print_completion("JavaScript scanning complete.")
        except Exception as e:
            ui.print_error(f"Error during JavaScript scanning: {str(e)}")
            return
        
        ui.print_progress("Analyzing JavaScript with LLM...")
        try:
            task = analyze_javascript_task.delay(config.JS_UNIQUE_FILE_NAME)
            analysis_file = await wait_for_task(task)
            if analysis_file:
                ui.print_completion(f"LLM analysis complete. Results written to {analysis_file}")
            else:
                ui.print_error("LLM analysis failed.")
                return
        except Exception as e:
            ui.print_error(f"Error during LLM analysis: {str(e)}")
            return
        
        ui.print_progress("Filtering LLM output...")
        try:
            task = filter_output_task.delay(config.LLM_FILE_NAME)
            result = await wait_for_task(task)
            if result is None:
                return
            ui.print_completion("Filtering complete.")
        except Exception as e:
            ui.print_error(f"Error during output filtering: {str(e)}")
            return
        
        ui.print_progress("Interpreting results...")
        try:
            task = interpret_results_task.delay(
                config.JS_UNIQUE_FILE_NAME,
                config.JS_URL_FILE_NAME,
                config.CLEAN_UP_FILE_NAME
            )
            result = await wait_for_task(task)
            if result is None:
                return
            ui.print_completion("Results interpretation complete.")
        except Exception as e:
            ui.print_error(f"Error during results interpretation: {str(e)}")
            return
        
        try:
            file_operations.clean_up_files(config.CLEAN_UP_FILE_NAME)
            ui.print_completion("Temporary files cleaned up.")
        except Exception as e:
            ui.print_error(f"Error during file cleanup: {str(e)}")
        
        ui.print_completion(f"Scan complete. Final results can be found in {config.CLEAN_UP_FILE_NAME}")
    except KeyboardInterrupt:
        ui.print_error("\nScan interrupted by user.")
    except Exception as e:
        ui.print_error(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())