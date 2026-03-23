from fastapi import APIRouter

from workers import tasks

router = APIRouter(prefix="/waha", tags=["WAHA"])

@router.post(path="/webhook")
async def receive_whatsapp_message(data: dict) -> dict[str, str]:
    event_dispatcher(data)

    return {"status": "success"}


def event_dispatcher(data: dict) -> None:
    event_type = data.get("event", "")

    if event_type == "session.status":
        print(f"SESSION STATUS: {data['payload']['status']}")
    elif event_type == "message":
        message = data["payload"]["from"]
        body = data["payload"]["body"]

        tasks.task_answer.delay(message, body)
    else:
        print(f"Event: {event_type}")