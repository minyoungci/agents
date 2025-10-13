import dotenv

dotenv.load_dotenv()

from crewai import Crew, Agent, Task
from crewai.project import CrewBase, agent, task, crew
from tools import search_tool, scrape_tool


@CrewBase
class NewsReaderAgent:

    @agent
    def news_hunter_agent(self):
        return Agent(
            config=self.agents_config["news_hunter_agent"],
            tools=[search_tool, scrape_tool],
        )

    @agent
    def summarizer_agent(self):
        return Agent(
            config=self.agents_config["summarizer_agent"],
            # 수정: scrape_tool 제거 - summarizer는 이미 수집된 컨텐츠만 요약해야 함
            # tools=[scrape_tool] 제거됨
        )

    @agent
    def curator_agent(self):
        return Agent(
            config=self.agents_config["curator_agent"],
        )

    @task
    def content_harvesting_task(self):
        return Task(
            config=self.tasks_config["content_harvesting_task"],
        )

    @task
    def summarization_task(self):
        return Task(
            config=self.tasks_config["summarization_task"],
            # 중요: context를 추가하여 이전 task의 결과를 받아옴
            # 이렇게 하면 summarizer가 content_harvest.md의 내용을 직접 접근 가능
            context=[self.content_harvesting_task()],
        )

    @task
    def final_report_assembly_task(self):
        return Task(
            config=self.tasks_config["final_report_assembly_task"],
            # 중요: 이전 두 task의 결과를 모두 context로 전달
            # curator가 content_harvest.md와 summary.md 둘 다 참조 가능
            context=[
                self.content_harvesting_task(),
                self.summarization_task(),
            ],
        )

    @crew
    def crew(self):
        return Crew(
            tasks=self.tasks,
            agents=self.agents,
            verbose=True,
            # 추가: Agent간 메모리 공유를 활성화하여 데이터 전달 개선
            memory=True,
        )


# 실행 예제: 실제 존재하는 뉴스 주제를 사용하는 것이 좋음
# 예: "AI technology 2024", "climate change", "electric vehicles" 등
result = NewsReaderAgent().crew().kickoff(inputs={"topic": "Cambodia Thailand War."})

# 각 task의 결과를 출력하여 디버깅에 도움
for task_output in result.tasks_output:
    print(f"\n{'='*50}")
    print(f"Task 완료: {task_output.name if hasattr(task_output, 'name') else 'Unknown'}")
    print(f"결과 일부: {str(task_output)[:200]}...")  # 처음 200자만 출력