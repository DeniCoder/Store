import json

class Store:
    def __init__(self, name, address, items=None):
        # Инициализация атрибутов
        self.name = name
        self.address = address
        # Проверка, чтобы items был пустым словарем, если ничего не передано
        self.items = items if items is not None else {}

    def add_item(self, name, price):
        """Добавляет новый товар в ассортимент."""
        if name in self.items:
            print(f"Товар '{name}' уже существует.")
        else:
            self.items[name] = price
            print(f"Товар '{name}' добавлен.")

    def remove_item(self, name):
        """Удаляет товар из ассортимента."""
        if name in self.items:
            del self.items[name]
            print(f"Товар '{name}' удален.")
        else:
            print(f"Товар '{name}' не найден.")

    def get_item_price(self, name):
        """Возвращает цену товара по его названию. Если товар отсутствует, возвращает None."""
        price = self.items.get(name)
        if price is None:
            print(f"Товар '{name}' не найден.")
        return price

    def update_item_price(self, name, new_price):
        """Обновляет цену товара."""
        if name in self.items:
            self.items[name] = new_price
            print(f"Цена товара '{name}' обновлена.")
        else:
            print(f"Товар '{name}' не найден.")

    def list_items(self):
        """Возвращает список всех товаров с их ценами."""
        for key, value in self.items.items():
            print(f"{key}: {value}")

    def save_to_file(self, filename="store_data.json"):
        """Сохранение состояния магазина в JSON-файл."""
        with open(filename, "w") as file:
            json.dump({
                "name": self.name,
                "address": self.address,
                "items": self.items
            }, file)

    @classmethod
    def load_from_file(cls, filename="store_data.json"):
        """Загрузка состояния магазина из JSON-файла."""
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                return cls(data["name"], data["address"], data["items"])
        except FileNotFoundError:
            print("Файл с данными не найден. Создается новый экземпляр магазина.")
            return cls("", "", {})

# Функция меню
def menu(store):
    while True:
        print("\nМеню:")
        print("1. Добавить товар")
        print("2. Удалить товар")
        print("3. Получить цену товара")
        print("4. Обновить цену товара")
        print("5. Показать все товары")
        print("0. Сохранить и выйти")

        try:
            choice = int(input("Выберите действие, указав его номер: "))
        except ValueError:
            print("Введено некорректное значение, укажите число от 0 до 5")
            continue

        if choice == 0:
            store.save_to_file()
            break
        elif choice == 1:
            name = input("Введите название товара: ")
            price = float(input("Введите цену товара: "))
            store.add_item(name, price)
        elif choice == 2:
            name = input("Введите название товара: ")
            store.remove_item(name)
        elif choice == 3:
            name = input("Введите название товара: ")
            price = store.get_item_price(name)
            if price is not None:
                print(f"Цена товара '{name}': {price}")
        elif choice == 4:
            name = input("Введите название товара: ")
            new_price = float(input("Введите новую цену товара: "))
            store.update_item_price(name, new_price)
        elif choice == 5:
            store.list_items()
        else:
            print("Неверный выбор. Пожалуйста, выберите число от 0 до 5.")

# Пример использования
store = Store.load_from_file()
menu(store)