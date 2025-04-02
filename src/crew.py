from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from src.config.config import MODEL_NAME
import os
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
from utils.outlook_connector import get_sent_emails

os.environ["LITELLM_SUPPRESS_PROVIDER_LIST"] = "true"
llm = LLM(
    model=f"ollama/{MODEL_NAME}",
    temperature=0.1,
    timeout=300,
    max_tokens=1000
    )

def build_email_style_knowledge_base():
    sent_samples = get_sent_emails()
    text = "\n\n---\n\n".join(sent_samples)
    # Create a knowledge source
    writing_style_knowledge = StringKnowledgeSource(
        content=text,
    )
    return writing_style_knowledge

@CrewBase
class OutlookAgentsCrew():
    """Outlook Multi-Agent System"""

    @agent
    def email_classifier(self) -> Agent:
        return Agent(
            config=self.agents_config['email_classifier'],
            llm=llm,
            verbose=True
        )

    @agent
    def summarizer(self) -> Agent:
        return Agent(
            config=self.agents_config['summarizer'],
            llm=llm,
            verbose=True
        )

    @agent
    def urgency_detector(self) -> Agent:
        return Agent(
            config=self.agents_config['urgency_detector'],
            llm=llm,
            verbose=True
        )

    @agent
    def tone_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['tone_analyzer'],
            llm=llm,
            verbose=True
        )

    @agent
    def draft_creator(self) -> Agent:
        return Agent(
            config=self.agents_config['draft_creator'],
            llm=llm,
            memory=True,
            verbose=True
        )

    @task
    def classify_email(self) -> Task:
        return Task(
            config=self.tasks_config['classify_email'],
        )

    @task
    def summarize_content(self) -> Task:
        return Task(
            config=self.tasks_config['summarize_content']
        )

    @task
    def detect_urgency(self) -> Task:
        return Task(
            config=self.tasks_config['detect_urgency']
        )

    @task
    def analyze_tone(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_tone']
        )

    @task
    def generate_response(self) -> Task:
        return Task(
            config=self.tasks_config['generate_response']
        )

    @crew
    def crew(self) -> Crew:
        """Initialize the Outlook agents crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential, #concurrent/sequential
            verbose=False,
            max_workers=4,
            # knowledge_sources=[build_email_style_knowledge_base()]
        )