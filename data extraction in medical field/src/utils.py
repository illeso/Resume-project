import re
from typing import Dict, List, Any
from spacy.tokens import Doc

def clean_text(text: str) -> str:
    """
    Clean and normalize input text.
    
    Args:
        text (str): Input text to clean
        
    Returns:
        str: Cleaned text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep medical symbols
    text = re.sub(r'[^\w\s.,;:()°-]', '', text)
    
    # Normalize whitespace
    text = text.strip()
    
    return text

def extract_medical_entities(doc: Doc) -> Dict[str, List[str]]:
    """
    Extract medical entities from spaCy processed document.
    
    Args:
        doc (Doc): spaCy processed document
        
    Returns:
        Dict[str, List[str]]: Dictionary of medical entities by type
    """
    entities = {
        "conditions": [],
        "medications": [],
        "measurements": [],
        "procedures": [],
        "other": []
    }
    
    # Medical condition patterns
    condition_patterns = [
        r'\b(?:hypertension|diabetes|fever|cough|fatigue|pain)\b',
        r'\b(?:type\s+\d+\s+diabetes)\b',
        r'\b(?:high\s+blood\s+pressure)\b'
    ]
    
    # Medication patterns
    medication_patterns = [
        r'\b(?:Amoxicillin|Aspirin|Ibuprofen|Paracetamol)\b',
        r'\b(?:mg|g|ml)\b'
    ]
    
    # Measurement patterns
    measurement_patterns = [
        r'\d+(?:\.\d+)?\s*°[CF]',
        r'\d+(?:\.\d+)?\s*(?:mg|g|ml|L)',
        r'\d+(?:\.\d+)?\s*(?:mmHg|bpm)'
    ]
    
    # Extract entities based on patterns
    text = doc.text.lower()
    
    # Extract conditions
    for pattern in condition_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        entities["conditions"].extend(match.group() for match in matches)
    
    # Extract medications
    for pattern in medication_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        entities["medications"].extend(match.group() for match in matches)
    
    # Extract measurements
    for pattern in measurement_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        entities["measurements"].extend(match.group() for match in matches)
    
    # Extract named entities from spaCy
    for ent in doc.ents:
        if ent.label_ in ["DISEASE", "CONDITION"]:
            entities["conditions"].append(ent.text)
        elif ent.label_ in ["DRUG", "MEDICATION"]:
            entities["medications"].append(ent.text)
        elif ent.label_ in ["PROCEDURE"]:
            entities["procedures"].append(ent.text)
        else:
            entities["other"].append(ent.text)
    
    # Remove duplicates and sort
    for key in entities:
        entities[key] = sorted(list(set(entities[key])))
    
    return entities

def validate_medical_data(data: Dict[str, Any]) -> bool:
    """
    Validate extracted medical data.
    
    Args:
        data (Dict[str, Any]): Extracted medical data
        
    Returns:
        bool: True if data is valid, False otherwise
    """
    required_fields = ["entities", "processed_text", "sentence_count", "word_count"]
    
    # Check if all required fields are present
    if not all(field in data for field in required_fields):
        return False
    
    # Validate entity structure
    if not isinstance(data["entities"], dict):
        return False
    
    required_entity_types = ["conditions", "medications", "measurements", "procedures", "other"]
    if not all(entity_type in data["entities"] for entity_type in required_entity_types):
        return False
    
    # Validate counts
    if not isinstance(data["sentence_count"], int) or data["sentence_count"] < 0:
        return False
    if not isinstance(data["word_count"], int) or data["word_count"] < 0:
        return False
    
    return True 