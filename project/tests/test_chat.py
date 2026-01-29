from app.chat import answer_question
import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"
import warnings
warnings.filterwarnings("ignore")


user = "rak"

question = "What is this document about?"

answer = answer_question(user, question)

print("ANSWER:")
print(answer)
