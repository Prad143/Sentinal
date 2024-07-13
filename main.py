from utils import ui, file_operations
from scanners import url_finder, javascript_scanner, vulnerability_scanner
from api import llm
import config

def main():
    ui.print_banner()
    
    url, max_recursion_level = ui.get_user_input()
    
    ui.print_progress("Crawling website for URLs...")
    urls = url_finder.find_urls(url, max_recursion_level)
    file_operations.write_urls_to_file(urls, config.FILE_NAME)
    ui.print_completion(f"Found {len(urls)} unique URLs. Results written to {config.FILE_NAME}")
    
    ui.print_progress("Scanning JavaScript files...")
    javascript_scanner.scan_javascript(config.FILE_NAME, config.JS_SCANNER_FILE_NAME)
    ui.print_completion("JavaScript scanning complete.")
    
    ui.print_progress("Analyzing JavaScript with LLM...")
    llm.analyze_javascript(config.JS_UNIQUE_FILE_NAME)
    ui.print_completion("LLM analysis complete.")
    
    ui.print_progress("Filtering LLM output...")
    vulnerability_scanner.filter_output(config.LLM_FILE_NAME)
    ui.print_completion("Filtering complete.")
    
    ui.print_progress("Interpreting results...")
    vulnerability_scanner.interpret_results(
        config.JS_UNIQUE_FILE_NAME,
        config.JS_URL_FILE_NAME,
        config.CLEAN_UP_FILE_NAME
    )
    ui.print_completion("Results interpretation complete.")
    
    file_operations.clean_up_files(config.CLEAN_UP_FILE_NAME)
    ui.print_completion("Temporary files cleaned up.")
    
    ui.print_completion(f"Scan complete. Final results can be found in {config.CLEAN_UP_FILE_NAME}")

if __name__ == "__main__":
    main()