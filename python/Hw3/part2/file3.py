books_list = [{"title": "abc", "authors": [], "year": 2013, "price": 100},
              {"title": "abc", "authors": [], "year": 1999, "price": 100},
              {"title": "abc", "authors": [], "year": 2013, "price": 100}]


def sale(books):
    return [{key: 4 * book["price"] // 5 if key == "price" else value for key, value in book.items()}
            if book["year"] < 2000 else book for book in books]


def gen_key_1(book):
    return -book["year"], book["title"]


def gen_key_2(book):
    return len(book["authors"]), -book["price"]


def gen_key_3(book):
    return book["authors"][0].split(' ')[1], book["authors"][0].split(' ')[0], book["title"], book["year"]


print(sale(books_list))
