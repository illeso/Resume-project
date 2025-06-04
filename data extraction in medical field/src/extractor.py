import spacy
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any
import logging
from .utils import clean_text, extract_medical_entities

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MedicalDataExtractor:
    def __init__(self):
        """Initialize the MedicalDataExtractor with spaCy model."""
        try:
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("Successfully loaded spaCy model")
        except OSError:
            logger.error("Please download the spaCy model first: python -m spacy download en_core_web_sm")
            raise

    def extract_from_text(self, text: str) -> Dict[str, Any]:
        """
        Extract medical information from text.
        
        Args:
            text (str): Input text containing medical information
            
        Returns:
            Dict[str, Any]: Dictionary containing extracted medical entities and information
        """
        # Clean the input text
        cleaned_text = clean_text(text)
        
        # Process with spaCy
        doc = self.nlp(cleaned_text)
        
        # Extract medical entities
        entities = extract_medical_entities(doc)
        
        return {
            "entities": entities,
            "processed_text": cleaned_text,
            "sentence_count": len(list(doc.sents)),
            "word_count": len([token for token in doc if not token.is_punct])
        }

    def process_file(self, file_path: str) -> Dict[str, Any]:
        """
        Process a medical data file.
        
        Args:
            file_path (str): Path to the input file
            
        Returns:
            Dict[str, Any]: Dictionary containing extracted information
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return self.extract_from_text(content)
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {str(e)}")
            raise

    def batch_process(self, directory: str) -> pd.DataFrame:
        """
        Process multiple files in a directory.
        
        Args:
            directory (str): Path to directory containing medical data files
            
        Returns:
            pd.DataFrame: DataFrame containing extracted information from all files
        """
        results = []
        directory_path = Path(directory)
        
        for file_path in directory_path.glob("**/*"):
            if file_path.is_file():
                try:
                    result = self.process_file(str(file_path))
                    result["file_name"] = file_path.name
                    results.append(result)
                except Exception as e:
                    logger.error(f"Error processing {file_path}: {str(e)}")
                    continue
        
        return pd.DataFrame(results)

def main():
    """Main function to demonstrate usage."""
    extractor = MedicalDataExtractor()
    
    # Example usage
    sample_text = """
    Patient presents with symptoms of fever (38.5°C), cough, and fatigue.
    Medical history includes hypertension and type 2 diabetes.
    Prescribed: Amoxicillin 500mg TID for 7 days.
    """
    
    result = extractor.extract_from_text(sample_text)
    print("\nExtracted Medical Information:")
    print("-----------------------------")
    print(f"Processed Text: {result['processed_text']}")
    print(f"Found Entities: {result['entities']}")
    print(f"Sentence Count: {result['sentence_count']}")
    print(f"Word Count: {result['word_count']}")

if __name__ == "__main__":
    main() 