import random
from typing import Literal

Category = Literal[
    "Fiction",
    "Dystopian",
    "Science Fiction",
    "Fantasy",
    "Mystery",
    "Non-Fiction",
    "Science",
    "History",
    "Biography",
    "Technology",
    "Art",
    "Philosophy",
    "Romance",
    "Thriller",
    "Self-Help",
    "Business",
    "Children",
    "Poetry",
    "Drama",
    "Travel",
]
first_names = [
    "Alex",
    "Jordan",
    "Taylor",
    "Morgan",
    "Casey",
    "Riley",
    "Jamie",
    "Avery",
    "Cameron",
    "Skyler",
]
last_names = [
    "Smith",
    "Johnson",
    "Williams",
    "Brown",
    "Jones",
    "Garcia",
    "Miller",
    "Davis",
    "Rodriguez",
    "Martinez",
]
title_parts1 = [
    "The",
    "A",
    "My",
    "Our",
    "An Echo of",
    "Whispers of",
    "Shadows in",
    "The Secret of",
    "Journey to",
    "Chronicles of",
]
title_parts2 = [
    "Crimson",
    "Golden",
    "Silent",
    "Forgotten",
    "Lost",
    "Ancient",
    "Hidden",
    "Quantum",
    "Starlight",
    "Midnight",
]
title_parts3 = [
    "River",
    "Mountain",
    "Throne",
    "Garden",
    "Key",
    "Cipher",
    "Legacy",
    "Prophecy",
    "Paradox",
    "Odyssey",
]
desc_parts1 = [
    "In a world where",
    "The story of a",
    "Discover the tale of",
    "A gripping narrative about",
    "Explore the life of",
]
desc_parts2 = [
    "magic is forbidden",
    "technology reigns supreme",
    "dreams can kill",
    "the past haunts the present",
    "a forgotten hero",
]
desc_parts3 = [
    "one person must",
    "a small group of rebels will",
    "an unlikely hero emerges to",
    "a journey begins to",
    "the fate of the universe rests on",
]
desc_parts4 = [
    "challenge the system.",
    "find their destiny.",
    "uncover a dark secret.",
    "save their world.",
    "change the course of history.",
]


def generate_books(num_books: int = 100) -> list[dict]:
    books = []
    categories = list(Category.__args__)
    for i in range(1, num_books + 1):
        author_first = random.choice(first_names)
        author_last = random.choice(last_names)
        title = f"{random.choice(title_parts1)} {random.choice(title_parts2)} {random.choice(title_parts3)}"
        description = f"{random.choice(desc_parts1)} {random.choice(desc_parts2)}, {random.choice(desc_parts3)} {random.choice(desc_parts4)}"
        isbn_part1 = random.randint(100, 999)
        isbn_part2 = random.randint(10, 99)
        isbn_part3 = random.randint(1000, 9999)
        isbn_part4 = random.randint(100000, 999999)
        isbn_part5 = random.randint(0, 9)
        isbn = f"{isbn_part1}-{isbn_part2}-{isbn_part3}-{isbn_part4}-{isbn_part5}"
        publication_year = random.randint(1950, 2024)
        category = random.choice(categories)
        books.append(
            {
                "id": i,
                "title": title,
                "author": f"{author_first} {author_last}",
                "category": category,
                "cover_image_url": f"https://picsum.photos/seed/{isbn}/400/600",
                "is_available": random.random() > 0.2,
                "description": description,
                "isbn": isbn,
                "publication_year": publication_year,
            }
        )
    return books