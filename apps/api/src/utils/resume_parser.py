import re

import spacy
from spacy.matcher import Matcher


class ResumeParser:
    @staticmethod
    def extract_email_from_resume(text: str):
        email = None

        # Use regex pattern to find a potential email address
        pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
        match = re.search(pattern, text)
        if match:
            email = match.group()

        return email

    @staticmethod
    def extract_name(resume_text: str):
        nlp = spacy.load("en_core_web_sm")
        matcher = Matcher(nlp.vocab)

        # Define name patterns
        patterns = [
            [{"POS": "PROPN"}, {"POS": "PROPN"}],  # First name and Last name
            [
                {"POS": "PROPN"},
                {"POS": "PROPN"},
                {"POS": "PROPN"},
            ],  # First name, Middle name, and Last name
            [
                {"POS": "PROPN"},
                {"POS": "PROPN"},
                {"POS": "PROPN"},
                {"POS": "PROPN"},
            ],  # First name, Middle name, Middle name, and Last name
            # Add more patterns as needed
        ]

        for pattern in patterns:
            matcher.add("NAME", patterns=[pattern])

        doc = nlp(resume_text)
        matches = matcher(doc)

        for match_id, start, end in matches:
            span = doc[start:end]
            return span.text

        return None

    @staticmethod
    def extract_contact_number_from_resume(text: str):
        contact_number = None

        # Use regex pattern to find a potential contact number
        pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
        match = re.search(pattern, text)
        if match:
            contact_number = match.group()

        return contact_number
