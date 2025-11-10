from langchain.messages import SystemMessage

from src.core.logger import logger
from src.modules.candidate.controller import CandidateController
from src.modules.llm_models.model import LlmModelFactory
from src.utils.resume_parser import CandidateExperience

from ..state import AgentState


class ChatBotNode:
    def __init__(self):
        self.model_factory = LlmModelFactory()
        self.llm = self.model_factory.get_model("deepseek-r1")
        self.llm = self.llm.bind_tools([])

    def __call__(self, state: AgentState):
        resume_candidates = state["resume_candidates"]
        candidates = state["candidates"]
        retrieved_texts = ""
        retrieved_candidates = ""

        if resume_candidates is not None:
            for candidate in resume_candidates:
                candidate_text = (
                    f"Retrieved Text for Candidate: {candidate.name}\n"
                    f"{'\n'.join(candidate.chunks)}\n\n"
                )
                retrieved_texts += candidate_text + "\n\n"

        if candidates is not None:
            for candidate in candidates:
                experiences = [
                    CandidateExperience(**exp) for exp in candidate.experiences
                ]
                candidate_text = (
                    f"Name: {candidate.name}\n"
                    f"Email: {candidate.email}\n"
                    f"Contact: {candidate.contact}\n"
                    f"Years of experience: {candidate.years_of_experience}\n"
                    f"Skills: {', '.join(candidate.skills)}\n"
                    f"Certifications: {', '.join(candidate.certifications)}\n"
                    f"Experiences: {'\n'.join(CandidateController._get_experience_texts(experiences))}\n"
                )
                retrieved_candidates += candidate_text + "\n\n"

        system_prompt = f"""
        You are an expert in recruitment.
        You will be given retrieved chunks from resumes and candidate profiles matching the user query.
        Suggest the user the best candidate suitable for the job description.
        Always give priority to the "Retrieved Candidates" section, then look into the "Retrieved Chunks from Resumes" section for more information

        <Retrieved Candidates>
        {retrieved_candidates}
        </Retrieved Candidates>

        <Retrieved Chunks from Resumes>
        {retrieved_texts}
        </Retrieved Chunks from Resumes>
        """

        logger.debug(f"Messages already in state: {len(state['messages'])}")

        response = self.llm.invoke(
            [SystemMessage(content=system_prompt)] + state["messages"]
        )
        return {"messages": [response]}
