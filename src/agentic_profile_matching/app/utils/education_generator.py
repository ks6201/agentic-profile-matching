import random

UNDERGRAD_DEGREES = [
    "B.Tech Computer Science",
    "B.Tech Information Technology",
    "B.E Computer Science",
    "B.E Information Technology",
    "B.Sc Computer Science",
    "BCA",
    "B.Com",
    "BA Economics",
    "BBA",
    "B.Sc Mathematics"
]

POSTGRAD_DEGREES = [
    "M.Tech Computer Science",
    "MCA",
    "MBA",
    "M.Com"
]


def generate_education() -> list[str]:
    if random.random() < 0.7:
        return [random.choice(UNDERGRAD_DEGREES)]

    undergrad = random.choice(UNDERGRAD_DEGREES)
    postgrad = random.choice(POSTGRAD_DEGREES)

    return [undergrad, postgrad]