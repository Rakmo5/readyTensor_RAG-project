from app.memory import save_message, load_recent_messages
import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"

user = "rak"

save_message(user, "user", "Hello PKB!")
save_message(user, "assistant", "Hello Rak, I remember you.")

messages = load_recent_messages(user)

for role, content in messages:
    print(f"{role}: {content}")
