from Agent import agent

def get_products_from_user():
    products = []

    print("Enter products (press Enter to finish):")

    while True:
        product = input("Product: ").strip()

        if product == "":
            break

        products.append(product)

    return products


def get_level_from_user():
    print("\nChoose difficulty level:")
    print("1 - אני רוצה משהו בקליל")
    print("2 - להשקיע יותר")
    print("3 - למצות יכולות")

    level_map = {
        "1": "easy",
        "2": "medium",
        "3": "hard"
    }

    while True:
        choice = input("Enter 1, 2 or 3: ").strip()

        if choice in level_map:
            return level_map[choice]
        else:
            print("Invalid choice. Please enter only 1, 2 or 3.")


def main():
    products = get_products_from_user()
    level = get_level_from_user()

    # יצירת dict אחד שמכיל את כל הנתונים
    request_data = {
        "products": products,
        "level": level
    }

    # שליחה ל-agent
    response = agent(request_data)

    print("\nAgent Response:")
    print(response)


if __name__ == "__main__":
    main()

