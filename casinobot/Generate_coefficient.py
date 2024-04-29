import random

def generate_multiplier():
    rand = random.randint(1, 100)
    if rand <= 60:
        return round(random.uniform(1.0, 2.6), 2)
    elif 60 < rand <= 80:
        return round(random.uniform(2.6, 8.4), 2)
    elif 80 < rand <= 90:
        return round(random.uniform(8.4, 15), 2)
    elif 90 < rand <= 98:
        return round(random.uniform(15, 40), 2)
    else:
        return round(random.uniform(40, 50), 2)