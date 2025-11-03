import re
from datetime import datetime
from typing import List, Optional, cast

import spacy
from langchain.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, EmailStr, Field, field_validator
from spacy.matcher import Matcher

from src.modules.llm_models.model import LlmModelFactory


class CandidateExperience(BaseModel):
    months_in_experience: Optional[int] = Field(
        description="Number of months the candidate worked in a company", default=None
    )
    company: str = Field(description="Name of the company the candidate has worked at")
    start_date: datetime = Field(description="Start date at the company")
    end_data: Optional[datetime] = Field(description="End date at the company")
    skills: Optional[str] = Field(
        description="Comma separated list of skill at the company"
    )
    role: str = Field(description="Role at the company")
    additional_info: str = Field(
        description="Additional Information while the candidate was at the company"
    )


class ResumeMetadata(BaseModel):
    email: EmailStr = Field(description="Email of the candidate")
    name: str = Field(description="Name of the candidate")
    contact: Optional[str] = Field(
        description="Contact Number or Phone Number of the candidate"
    )
    years_of_experience: float = Field(
        description="Years of experience of the candidate"
    )

    skills: List[str] = Field(
        default=[], description="List of skills the candidate have"
    )
    certifications: List[str] = Field(
        default=[], description="List of certifications the candidate have"
    )
    experiences: List[CandidateExperience] = Field(default=[], description="")

    @field_validator("email", mode="before")
    def lower_case_email(cls, v: str) -> str:
        if isinstance(v, str):
            return v.lower()
        return v


class ResumeParser:
    def __init__(self):
        self.model_factory = LlmModelFactory()
        self.llm = self.model_factory.get_model("gpt-4o")

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

    def extract_resume_details(self, content: str) -> ResumeMetadata:
        prompt = (
            "You are a expert in reading a resume of an candidate and extract the relevant information\n"
            "Below is the content of the resume of the candidate\n\n"
            "<CONTENT>\n{content}</CONTENT>"
        )
        prompt = prompt.format(content=content)
        message = SystemMessage(content=prompt)
        user_message = HumanMessage(content="<CONTENT>\n{content}</CONTENT>")
        response = self.llm.with_structured_output(ResumeMetadata).invoke(
            input=[message, user_message]
        )
        response = cast(ResumeMetadata, response)

        return response
