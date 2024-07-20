from celery_app import app
from scanners.url_finder import find_urls_task
from scanners import javascript_scanner, vulnerability_scanner, search_scraper
from api import llm

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