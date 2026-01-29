from app.auth import get_user_dir
import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"

u1 = get_user_dir("rak")
u2 = get_user_dir("guest")

print("Rak dir:", u1)
print("Guest dir:", u2)
