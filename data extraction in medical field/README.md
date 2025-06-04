# Medical Data Extraction Project

This project provides tools for extracting and processing medical data from various sources. It includes functionality for text processing, entity recognition, and data analysis of medical records.

## Features

- Medical text extraction and processing
- Named Entity Recognition (NER) for medical terms
- Data cleaning and normalization
- Basic medical data analysis
- Support for various input formats

## Installation

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Download the spaCy medical model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Project Structure

```
medical_data_extraction/
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── extractor.py
│   └── utils.py
├── data/
│   └── sample/
└── tests/
    └── __init__.py
```

## Usage

1. Place your medical data files in the `data` directory
2. Run the main script:
   ```bash
   python src/extractor.py
   ```

## Contributing

Feel free to submit issues and enhancement requests! 