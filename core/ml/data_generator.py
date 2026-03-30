import random
import pandas as pd

data = []

for _ in range(5000):

    user_rate = random.randint(1, 200)
    queue_length = random.randint(1, 100)
    priority_score = random.randint(1, 10)

    if queue_length > 80 and priority_score < 5:
        decision = "DROP"
    elif queue_length > 60:
        decision = "DEGRADE"
    else:
        decision = "ALLOW"

    data.append([user_rate, queue_length, priority_score, decision])

df = pd.DataFrame(data, columns=[
    "user_rate", "queue_length", "priority_score", "decision"
])
df.to_csv("training_data.csv", index=False)