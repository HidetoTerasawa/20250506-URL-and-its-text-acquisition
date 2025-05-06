# URL Summary Tool

## Overview
The URL Summary Tool is a Python application designed to extract URLs from a sitemap, fetch text from each URL, and summarize the content using ChatGPT. This tool is useful for quickly obtaining summaries of web pages, making it easier to digest large amounts of information.

## Project Structure
```
url-summary-tool
├── src
│   ├── main.py                # Entry point for the application
│   ├── utils
│   │   ├── sitemap.py         # Functions for extracting URLs from a sitemap
│   │   ├── text_extraction.py  # Functions for fetching and extracting text from URLs
│   │   └── summarization.py    # Functions for summarizing text using ChatGPT
├── requirements.txt           # List of dependencies
└── README.md                  # Documentation for the project
```

## Installation
To set up the project, follow these steps:

1. Clone the repository:
   ```
   git clone <repository-url>
   cd url-summary-tool
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
To run the application, execute the following command:
```
python src/main.py
```

### Configuration
You may need to modify the `sitemap_url` variable in `src/main.py` to point to the desired sitemap.

## Functionality
- **Extract URLs**: The tool fetches URLs from a specified sitemap using the functions defined in `src/utils/sitemap.py`.
- **Text Extraction**: It retrieves the text content from each URL using the functions in `src/utils/text_extraction.py`.
- **Summarization**: The extracted text is summarized using the ChatGPT API, as implemented in `src/utils/summarization.py`.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.