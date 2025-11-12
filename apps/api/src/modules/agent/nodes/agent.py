from uuid import UUID, uuid4

from langchain.agents import create_agent
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import InMemorySaver

from src.core.exception import NotFoundException
from src.core.logger import logger
from src.modules.candidate.controller import CandidateController
from src.modules.llm_models.model import LlmModelFactory
from src.utils.resume_parser import CandidateExperience
from src.utils.time import utcnow

from ..state import AgentState
from .calendar_tool import check_candidate_calendar
from .email_tool import send_email

memory = InMemorySaver()


class AgentNode:
    def __init__(self, candidate_controller: CandidateController) -> None:
        self.candidate_controller = candidate_controller
        self.model_factory = LlmModelFactory()
        self.llm = self.model_factory.get_model()
        self.tools = [send_email, check_candidate_calendar]

    def __call__(self, state: AgentState, config: RunnableConfig):
        candidate_id = (
            UUID(state["candidate_id"]) if state["candidate_id"] is not None else None
        )

        if candidate_id is None:
            raise NotFoundException("No candidate found")

        candidate = self.candidate_controller.get_by_id(candidate_id)

        logger.debug(f"Selected candidate: {candidate_id}")

        experiences = [CandidateExperience(**exp) for exp in candidate.experiences]
        candidate_details = (
            f"Name: {candidate.name}\n"
            f"Email: {candidate.email}\n"
            f"Contact: {candidate.contact}\n"
            f"Years of experience: {candidate.years_of_experience}\n"
            f"Skills: {', '.join(candidate.skills)}\n"
            f"Certifications: {', '.join(candidate.certifications)}\n"
            f"Experiences: {'\n'.join(CandidateController._get_experience_texts(experiences))}\n"
        )

        system_prompt = f"""
        You are an expert in recruitment.
        You will be given a candidate's details.

        Current time: {utcnow().isoformat()}
        
        <Candidate Details>
        {candidate_details}
        </Candidate Details>
        """

        agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=system_prompt,
            checkpointer=memory,
        )

        thread_id = config.get("configurable", {}).get("thread_id", uuid4())

        response = agent.invoke(
            {"messages": [{"role": "user", "content": state["messages"][-1].content}]},
            {"configurable": {"thread_id": thread_id}},
        )
        output = response["messages"][-1]
        return {"messages": [output]}
