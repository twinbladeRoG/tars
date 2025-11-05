from langchain.messages import SystemMessage

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
        retrieved_points = state["retrieved_points"]
        candidates = state["candidates"]
        retrieved_texts = ""
        retrieved_candidates = ""

        if retrieved_points is not None:
            for point in retrieved_points:
                if point.payload:
                    retrieved_texts += "\n" + point.payload["text"]

        if candidates is not None:
            for candidate in candidates:
                experiences = [
                    CandidateExperience(**exp) for exp in candidate.experiences
                ]
                candidate_text = (
                    f"{candidate.name}\n"
                    f"{candidate.email}\n"
                    f"{candidate.contact}\n"
                    f"{candidate.years_of_experience} years of experience\n"
                    f"{', '.join(candidate.skills)}\n"
                    f"{', '.join(candidate.certifications)}\n"
                    f"{'\n'.join(CandidateController._get_experience_texts(experiences))}\n"
                )
                retrieved_candidates += candidate_text + "\n\n"

        system_prompt = f"""
        You are an export in recruitment.
        You will be given retrieved chunks from resumes and candidate profiles matching the user query.
        Suggest the user the best candidate suitable for the job description.

        <Retrieved Candidates>
        {retrieved_candidates}
        </Retrieved Candidates>

        <Retrieved Chunks from Resumes>
        {retrieved_texts}
        </Retrieved Chunks from Resumes>
        """

        response = self.llm.invoke(
            [SystemMessage(content=system_prompt)] + state["messages"]
        )
        return {"messages": [response]}
