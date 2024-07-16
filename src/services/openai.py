import os
from openai import OpenAI

print("os.getenv(OPENAI_API_KEY)", os.getenv("OPENAI_API_KEY"))

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

def getMedicalContent(name, age, illness, startDate, endDate):
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a expert doctor."},
        {"role": "user", "content": f"Write the 200 words content of medical application starting with 'to whom it may concern' explainging that your paitent {name}, {age}, was unwell due to {illness} and will not be able to attend office from {startDate} to {endDate}. Do not mention the dates just the number of days. Also the end should not contain any signature or doctor information"}
    ]
    )

    print(completion.choices[0].message.content)
    
    return completion.choices[0].message.content