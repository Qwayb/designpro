import random

def captchasymbols():
    russian_letters = '1234567890абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    challenge = ''.join(random.choice(russian_letters) for _ in range(5))
    response = challenge
    return challenge, response
