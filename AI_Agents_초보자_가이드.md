# 🤖 AI Agents 초보자 완벽 가이드

## 📌 목차
1. [AI Agent 기본 개념](#1-ai-agent란)
2. [CrewAI 프레임워크](#2-crewai-프레임워크)
3. [프로젝트 구조 이해하기](#3-프로젝트-구조)
4. [코드 상세 설명](#4-코드-상세-설명)
5. [실습 가이드](#5-실습-가이드)
6. [다음 단계](#6-다음-단계)

---

## 1. AI Agent란?

### 🎯 핵심 개념
**AI Agent = 자율적으로 작동하는 AI 비서**

| 구분 | 일반 AI (ChatGPT) | AI Agent |
|------|------------------|----------|
| 작동 방식 | 질문 → 답변 | 목표 → 계획 → 실행 → 결과 |
| 자율성 | ❌ 수동적 | ✅ 능동적 |
| 도구 사용 | ❌ 불가능 | ✅ 가능 (웹 검색, 파일 읽기 등) |
| 협업 | ❌ 단독 작업 | ✅ 다른 Agent와 협력 |

### 💡 실생활 비유
- **일반 AI**: 계산기 (버튼 누르면 계산)
- **AI Agent**: 회계사 (목표 이해 → 자료 수집 → 분석 → 보고서 작성)

---

## 2. CrewAI 프레임워크

### 🏗️ 4대 구성 요소

#### 1️⃣ **Agent (에이전트)**
- **역할**: 특정 전문성을 가진 AI 개체
- **예시**: 번역가, 기자, 편집자, 분석가

#### 2️⃣ **Task (태스크)**
- **역할**: Agent가 수행할 구체적 작업
- **예시**: "뉴스 검색하기", "내용 요약하기"

#### 3️⃣ **Tool (도구)**
- **역할**: Agent가 사용할 수 있는 기능
- **예시**: 웹 검색, 웹페이지 읽기, 파일 저장

#### 4️⃣ **Crew (크루)**
- **역할**: 여러 Agent가 모인 팀
- **예시**: 뉴스팀 (기자 + 편집자 + 큐레이터)

---

## 3. 프로젝트 구조

```
agent_1/
├── 📁 First Agent/           # 프로젝트 1: 번역 Agent
│   ├── config/
│   │   ├── agents.yaml      # Agent 설정
│   │   └── tasks.yaml       # Task 설정
│   └── main.py              # 실행 파일
│
├── 📁 News Reader/           # 프로젝트 2: 뉴스 수집팀
│   ├── config/
│   │   ├── agents.yaml      # 3개 Agent 설정
│   │   └── tasks.yaml       # Task 설정
│   ├── output/              # 결과물 저장
│   └── main.py              # 실행 파일
│
└── 📄 tools.py              # 공통 도구 모음
```

---

## 4. 코드 상세 설명

### 📄 tools.py - 도구 모음

```python
# 1. 웹 검색 도구
search_tool = SerperDevTool(n_results=30)
# → Google처럼 웹에서 정보를 검색

# 2. 웹 스크래핑 도구
@tool
def scrape_tool(url: str):
    # Step 1: 브라우저 실행 (화면 없이)
    browser = p.chromium.launch(headless=True)

    # Step 2: 웹사이트 방문
    page.goto(url)
    time.sleep(5)  # 페이지 로딩 대기

    # Step 3: HTML 가져오기
    html = page.content()

    # Step 4: 불필요한 요소 제거
    # (광고, 메뉴, 이미지 등)
    unwanted_tags = ["header", "footer", "nav", ...]

    # Step 5: 깨끗한 텍스트만 반환
    return content
```

### 📄 First Agent - 번역 프로젝트

```python
@CrewBase
class TranslatorCrew:
    # 1. Agent 정의: 번역가
    @agent
    def translator_agent(self):
        return Agent(config=self.agents_config['translator_agent'])

    # 2. Task 정의: 번역 작업
    @task
    def translate_task(self):
        return Task(config=self.tasks_config['translate_task'])

    # 3. Crew 조립: Agent + Task
    @crew
    def assemble_crew(self):
        return Crew(
            agents=self.agents,  # 번역가
            tasks=self.tasks,    # 번역 작업
            verbose=True         # 과정 출력
        )

# 실행
TranslatorCrew().assemble_crew().kickoff(
    inputs={"sentence": "Hello, how are you?"}
)
```

### 📄 News Reader - 뉴스 수집팀

```python
@CrewBase
class NewsReaderAgent:
    # 3개의 Agent 정의

    # 1. 뉴스 사냥꾼 (검색 담당)
    @agent
    def news_hunter_agent(self):
        return Agent(
            config=self.agents_config['news_hunter_agent'],
            tools=[search_tool]  # 검색 도구 사용
        )

    # 2. 요약 전문가 (요약 담당)
    @agent
    def summarizer_agent(self):
        return Agent(config=self.agents_config['summarizer_agent'])

    # 3. 큐레이터 (최종 편집)
    @agent
    def curator_agent(self):
        return Agent(config=self.agents_config['curator_agent'])

    # Task 정의
    @task
    def content_harvesting_task(self):
        return Task(config=self.tasks_config['content_harvesting_task'])

    # Crew 조립
    @crew
    def crew(self):
        return Crew(
            agents=self.agents,  # 3명의 Agent
            tasks=self.tasks,    # 수집 → 요약 → 편집
            verbose=True
        )

# 실행
NewsReaderAgent().crew().kickoff(
    input={"topic": "Cambodia Thai War"}
)
```

---

## 5. 실습 가이드

### 🚀 Step 1: 환경 설정

```bash
# 1. 가상환경 생성
python -m venv .venv

# 2. 가상환경 활성화
# Windows: .venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate

# 3. 패키지 설치
pip install crewai crewai-tools playwright beautifulsoup4

# 4. Playwright 브라우저 설치
playwright install chromium
```

### 🔑 Step 2: API 키 설정

`.env` 파일 생성:
```bash
OPENAI_API_KEY=your_openai_key_here
SERPER_API_KEY=your_serper_key_here  # Google 검색용
```

### 📝 Step 3: 설정 파일 작성

`config/agents.yaml`:
```yaml
translator_agent:
  role: "전문 번역가"
  goal: "영어를 한국어로 정확하게 번역"
  backstory: "10년 경력의 전문 번역가입니다."
```

`config/tasks.yaml`:
```yaml
translate_task:
  description: "다음 문장을 한국어로 번역하세요: {sentence}"
  expected_output: "한국어로 번역된 문장"
```

### ▶️ Step 4: 실행

```bash
# 번역 Agent 실행
python "First Agent/main.py"

# 뉴스 수집팀 실행
python "News Reader Tasks and Agents/main.py"
```

---

## 6. 다음 단계

### 📚 학습 로드맵

#### Level 1: 기초 (현재 단계) ✅
- [x] Agent 개념 이해
- [x] CrewAI 기본 구조
- [x] 간단한 Agent 실행

#### Level 2: 중급
- [ ] 복잡한 Multi-Agent 시스템
- [ ] Custom Tool 제작
- [ ] Agent간 통신 패턴
- [ ] 에러 처리 및 재시도 로직

#### Level 3: 고급
- [ ] LangChain 통합
- [ ] Vector DB 활용 (RAG)
- [ ] 실시간 스트리밍
- [ ] Production 배포

### 💡 실습 아이디어

1. **날씨 리포터 Agent**
   - 날씨 API 연동
   - 일일 날씨 브리핑 생성

2. **주식 분석팀**
   - 데이터 수집 Agent
   - 기술적 분석 Agent
   - 리포트 작성 Agent

3. **고객 서비스 봇**
   - 질문 분류 Agent
   - 답변 생성 Agent
   - 품질 검증 Agent

### 🔧 트러블슈팅

**자주 발생하는 문제들:**

1. **"API key not found" 에러**
   - `.env` 파일 확인
   - 환경 변수 제대로 로드되었는지 확인

2. **"Agent not responding" 문제**
   - API 한도 확인
   - 네트워크 연결 상태 확인

3. **"Tool execution failed" 에러**
   - Tool의 입력 형식 확인
   - 필요한 패키지 설치 확인

### 📖 추가 학습 자료

- [CrewAI 공식 문서](https://docs.crewai.com)
- [LangChain 튜토리얼](https://python.langchain.com)
- [OpenAI API 가이드](https://platform.openai.com/docs)

---

## 🎯 핵심 요약

1. **AI Agent = 자율적 AI 비서**
2. **CrewAI = Agent 팀워크 프레임워크**
3. **구성요소 = Agent + Task + Tool + Crew**
4. **실행 흐름 = 입력 → Agent 작업 → 결과**

이제 여러분도 AI Agent를 만들 수 있습니다! 🚀

---

*질문이 있으시면 언제든지 물어보세요!*