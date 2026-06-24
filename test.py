books = [
    {
        "id": 1,
        "title": "Тихий Дэн",
        "author": "Озон Л.П",
    },
    {
        "id": 2,
        "title": "Гульман",
        "author": "Некий Ш.А",
    },
]

for book in books:
    if 2 in book.values():
        print(book)