# Sentinal

Sentinal is an advanced web vulnerability scanner powered by AI, designed to identify potential security risks in JavaScript code across websites. It combines web crawling, JavaScript analysis, and AI-powered vulnerability detection to provide comprehensive security assessments.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- Web crawling with customizable recursion levels
- JavaScript extraction from web pages
- AI-powered vulnerability analysis using Google's Gemini model
- VPN rotation for anonymity
- Search engine integration (Google and Bing) for targeted scanning
- Asynchronous processing for improved performance
- Detailed vulnerability reports with mitigation recommendations

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/sentinal.git
   cd sentinal
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up Redis for Celery:
   - Install Redis on your system
   - Ensure Redis is running on localhost:6379

4. Configure your environment variables:
   - Create a `.env` file in the project root
   - Add the following variables:
     ```
     LLM_API_KEY=your_gemini_api_key
     LLM_MODEL=gemini-pro
     ```

5. Create a `config.py` file (see [Configuration](#configuration) section for details)

## Usage

To start Sentinal, run:
```
python main.py
```

Follow the on-screen prompts to choose between:
1. Scanning a specific URL
2. Searching for URLs based on a query

## Configuration

Create a `config.py` file in the project root directory. This file is not included in the repository for security reasons. Use the following template and adjust the values as needed:
```
import os
from dotenv import load_dotenv

Load environment variables from .env file
load_dotenv()


# VPN settings
VPN_CONFIG_FILES = [
'/path/to/vpn1.ovpn',
'/path/to/vpn2.ovpn',
# Add more VPN config files as needed
]
VPN_ROTATION_INTERVAL = 50 # Number of requests before rotating VPN

# File names
FILE_NAME = "urls.txt"
JS_SCANNER_FILE_NAME = "js_content.txt"
JS_UNIQUE_FILE_NAME = "js_unique_content.txt"
LLM_FILE_NAME = "llm_analysis.txt"
JS_URL_FILE_NAME = "js_url_mapping.txt"
CLEAN_UP_FILE_NAME = "final_results.txt"

# LLM settings
LLM_API_KEY = os.getenv('LLM_API_KEY')
LLM_MODEL = os.getenv('LLM_MODEL', 'gemini-pro')

# LLM instructions
INSTRUCTIONS = """
You're working in Cybersecurity. You have been searching for vulnerabilities through source code for 20 years.
Analyze the following JavaScript code for potential security vulnerabilities:
{js_content}
Please provide a detailed report on any vulnerabilities found, including:
1. The type of vulnerability
2. The location in the code
3. The potential impact
4. Recommendations for mitigation
"""

# Maximum recursion level for URL crawling
MAX_RECURSION_LEVEL = 3
```


Adjust the following key configuration options as needed:
- `VPN_CONFIG_FILES`: List of VPN configuration files
- `VPN_ROTATION_INTERVAL`: Number of requests before rotating VPN
- `MAX_RECURSION_LEVEL`: Maximum depth for URL crawling
- File names for various outputs
- LLM settings and instructions

## How It Works

1. **URL Collection**: Sentinal either crawls a given URL or searches for URLs based on a user query.
2. **JavaScript Extraction**: It extracts JavaScript code from the collected URLs.
3. **AI Analysis**: The extracted JavaScript is analyzed by the Gemini AI model for potential vulnerabilities.
4. **Result Interpretation**: The AI's output is processed to identify and categorize vulnerabilities.
5. **Report Generation**: A detailed report is generated, listing vulnerabilities, their locations, potential impacts, and mitigation strategies.

## Project Structure

- `main.py`: The entry point of the application
- `scanners/`: Contains modules for URL finding, JavaScript scanning, and vulnerability scanning
  - `url_finder.py`: Implements web crawling functionality
  - `javascript_scanner.py`: Extracts JavaScript from web pages
  - `vulnerability_scanner.py`: Processes and interprets vulnerability data
  - `search_scraper.py`: Implements search engine scraping
- `api/`: Handles interaction with the Gemini AI model
  - `llm.py`: Implements the AI analysis using the Gemini model
- `utils/`: Utility functions for file operations, UI, and VPN management
  - `file_operations.py`: Handles file read/write operations
  - `ui.py`: Manages user interface and console output
  - `vpn_manager.py`: Handles VPN rotation
- `tasks.py`: Defines Celery tasks for asynchronous processing
- `celery_app.py`: Configures the Celery application
- `config.py`: Configuration file (not included in repository)

## Contributing

Contributions to Sentinal are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch: `git checkout -b feature-branch-name`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-branch-name`
5. Submit a pull request

Please ensure that your code adheres to the project's coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Google Gemini for providing the AI model used in vulnerability analysis
- The open-source community for various libraries and tools used in this project

---

**Disclaimer**: Sentinal is a tool designed for educational and authorized security testing purposes only. Always obtain proper permission before scanning any website or network that you do not own or have explicit permission to test. The authors and contributors of Sentinal are not responsible for any misuse or damage caused by this tool.

