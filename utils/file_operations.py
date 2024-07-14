def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_to_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def read_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def write_urls_to_file(urls, file_path):
    with open(file_path, 'w') as file:
        for url in urls:
            file.write(f"{url}\n")

def append_to_file(file_path, content):
    with open(file_path, 'a') as file:
        file.write(content)

def read_js_content(file_path):
    with open(file_path, 'r') as file:
        return file.read()
    
def clean_up_files(file_path):
    import os
    directory = os.path.dirname(file_path)
    base_name = os.path.basename(file_path)
    for filename in os.listdir(directory):
        if filename.startswith(base_name.split('_')[0]) and filename != base_name:
            os.remove(os.path.join(directory, filename))
    print("Temporary files cleaned up.")