import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).parent
CONTENT_PATH = BASE_DIR / "content.json"
STATE_PATH = BASE_DIR / "state.json"
FEED_PATH = BASE_DIR / "docs" / "feed.json"
REDIRECTION_URL = "https://SEU-USUARIO.github.io/pausa-espiritual-feed/"

UUID_NAMESPACE = uuid.UUID("8a2c3b4d-0000-4000-8000-000000000000")


def main():
    content = json.loads(CONTENT_PATH.read_text(encoding="utf-8"))
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))

    idx = state["index"] % len(content)
    item = content[idx]

    now = datetime.now(timezone.utc)
    update_date = now.strftime("%Y-%m-%dT%H:%M:%S.0Z")
    uid = str(uuid.uuid5(UUID_NAMESPACE, f"{idx}-{now.date().isoformat()}"))

    feed_item = {
        "uid": uid,
        "updateDate": update_date,
        "titleText": f"Pausa Espiritual — {item['categoria']}",
        "mainText": item["texto"],
        "redirectionUrl": REDIRECTION_URL,
    }

    FEED_PATH.parent.mkdir(parents=True, exist_ok=True)
    FEED_PATH.write_text(
        json.dumps([feed_item], ensure_ascii=False, indent=2), encoding="utf-8"
    )

    state["index"] = (idx + 1) % len(content)
    STATE_PATH.write_text(json.dumps(state, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
