from celery import Celery, signals
from services.waha_services import send_message
from agno.agent import Agent
from agno.models.groq import Groq
from redisvl.extensions.cache.llm import SemanticCache

app = Celery("tasks", broker="pyamqp://guest:guest@rabbitmq//")

agent: Agent = None
cache: SemanticCache = None

@signals.worker_process_init.connect
def initialize_global_resource():
    global agent, cache

    with open("data/World_fantasy.md", "r") as f:
        world_fantasy_doc = f.read()

    with open("data/prompt.xml", "r") as f:
        prompt_doc = f.read()

    cache = connect_semantic_cache()

    agent = Agent(
        model=Groq(id="openai/gpt-oss-120b"),
        instructions=f"<fatos>\n{world_fantasy_doc}\n</fatos>\n{prompt_doc}"
    )


@app.task
def task_answer(chat_id: str, prompt: str) -> None:
    if response := get_semantic_cache_answer(cache, prompt):
        # message = f"(cache) {response}" #TODO somente para testes
        message = response

        send_message(chat_id, message)
        return
    
    message = get_ai_answer(prompt)

    if message == None:
        message = "Tente novamente mais tarde!"
    
    set_semantic_cache_answer(cache, prompt, message)

    send_message(chat_id, message)


def get_ai_answer(prompt: str) -> str | None:
    try:
        response = agent.run(input=prompt)
        return response.content
    except Exception as e:
        print(f"Exception: {e}")
        return None


def connect_semantic_cache() -> SemanticCache:
    return SemanticCache(
        name="llmcache",
        ttl=360,
        redis_url="redis://redis:6379",
        distance_threshold=0.1
    )


def get_semantic_cache_answer(cache: SemanticCache, prompt: str) -> str | None:
    response = cache.check(prompt=prompt)

    if len(response) == 0:
        return None

    return response[0]["response"]


def set_semantic_cache_answer(cache: SemanticCache, prompt: str, answer: str) -> None:
    cache.store(prompt=prompt, response=answer)