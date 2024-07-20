from celery_app import app
from scanners import url_finder, javascript_scanner, vulnerability_scanner, search_scraper
from api import llm

@app.task
def find_urls_task(url, max_recursion_level):
    return url_finder.find_urls(url, max_recursion_level)

@app.task
def search_urls_task(query, engine, num_results):
    return search_scraper.search_urls(query, engine, num_results)

@app.task
def scan_javascript_task(input_file, output_file):
    return javascript_scanner.scan_javascript(input_file, output_file)

@app.task
def analyze_javascript_task(js_file_path):
    return llm.analyze_javascript(js_file_path)

@app.task
def filter_output_task(input_file):
    return vulnerability_scanner.filter_output(input_file)

@app.task
def interpret_results_task(js_file, url_file, output_file):
    return vulnerability_scanner.interpret_results(js_file, url_file, output_file)