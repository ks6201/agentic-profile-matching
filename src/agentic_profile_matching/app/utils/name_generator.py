

import random

FIRST_NAMES = [
    "Amit", "Rahul", "Neha", "Priya", "Karan", "Sneha", "Vikram",
    "Anjali", "Rohit", "Pooja", "Arjun", "Ishita", "Manish",
    "Kavya", "Deepak", "Shreya", "Varun", "Nisha", "Aditya",
    "Meera"
]

LAST_NAMES = [
    "Sharma", "Verma", "Gupta", "Mehta", "Kapoor", "Reddy",
    "Nair", "Iyer", "Singh", "Patel", "Das", "Kulkarni",
    "Joshi", "Desai", "Bansal", "Agarwal", "Malhotra",
    "Saxena", "Yadav", "Chauhan"
]


def generate_name() -> str:
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"