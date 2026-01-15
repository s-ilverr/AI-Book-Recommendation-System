# Book Recommendation System (Class 12 CBSE)
# CSV Format: genre, book title, description, author

import csv

# -------------------------------------
# STEP 1: Load CSV File into a List
# -------------------------------------
books = []

try:
    f = open("book_recommendations.csv", "r", encoding="utf-8")
    reader = csv.reader(f)
    next(reader)  # skip header

    for row in reader:
        books.append({
            "genre": row[0],          # contains multiple genres
            "title": row[1],
            "description": row[2],
            "author": row[3]
        })

    f.close()

except FileNotFoundError:
    print("Error: CSV file 'book_recommendations.csv' not found!")
    exit()


# -------------------------------------
# STEP 2: User Input (multiple genres allowed)
# -------------------------------------
print("Enter genres separated by commas (Example: fantasy, mystery, romance)")
user_genres = input("Enter preferred genres: ").strip().lower()

user_genre_list = [g.strip() for g in user_genres.split(",")]

user_desc = input("Describe the type of book you want: ").strip().lower()


# ----------------------------------------------------------
# STEP 3: Simple Similarity Based on Matching Words
# ----------------------------------------------------------
def similarity(desc1, desc2):
    words1 = set(desc1.split())
    words2 = set(desc2.split())
    common = words1.intersection(words2)
    return len(common)


# ----------------------------------------------------------
# STEP 4: Filter Books by Any Matching Genre + Description
# ----------------------------------------------------------
filtered_books = []

for b in books:
    book_genres = b["genre"].lower()

    # Check if ANY of the user's genres appear in the book's genre field
    genre_match = False
    for g in user_genre_list:
        if g in book_genres:
            genre_match = True
            break

    if genre_match:
        filtered_books.append(b)

# If no genre matches, use all books
if len(filtered_books) == 0:
    print("\nNo genre match found. Showing best matches by description.\n")
    filtered_books = books.copy()


# ----------------------------------------------------------
# STEP 5: Compute similarity using BOTH genre and description
# ----------------------------------------------------------
scores = []
for b in filtered_books:
    desc_score = similarity(user_desc, b["description"].lower())
    
    # Additional small genre boost for books having more matching genres
    genre_count = 0
    for g in user_genre_list:
        if g in b["genre"].lower():
            genre_count += 1

    total_score = desc_score + genre_count  # simple combined score

    scores.append((total_score, b))

# Sort by highest total score
scores.sort(reverse=True, key=lambda x: x[0])


# ----------------------------------------------------------
# STEP 6: Display Top 3 Books
# ----------------------------------------------------------
print("\n📚 Top 3 Book Recommendations:\n")

top = min(3, len(scores))
for i in range(top):
    score, book = scores[i]
    print(f"Recommendation {i+1}:")
    print(f"• Title: {book['title']}")
    print(f"• Author: {book['author']}")
    print(f"• Genres: {book['genre']}")
    print(f"• Description: {book['description']}")
    print("-" * 50)
