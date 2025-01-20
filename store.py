import json

class Store:
    def __init__(self, name, address, items=None):
        self.name = name
        self.address = address
        self.items = items if items is not None else {}

    def add_item(self, item_name, price):
        """Добавляет новый товар в ассортимент."""
        if item_name in self.items:
            print(f"Товар '{item_name}' уже существует.")
        elif price < 0:
            print("Цена не может быть отрицательной.")
        else:
            self.items[item_name] = price
            print(f"Товар '{item_name}' добавлен.")

    def remove_item(self, item_name):
        """Удаляет товар из ассортимента."""
        if item_name in self.items:
            del self.items[item_name]
            print(f"Товар '{item_name}' удален.")
        else:
            print(f"Товар '{item_name}' не найден.")

    def get_item_price(self, item_name):
        """Возвращает цену товара по его названию. Если товар отсутствует, возвращает None."""
        return self.items.get(item_name)

    def update_item_price(self, item_name, new_price):
        """Обновляет цену товара."""
        if item_name in self.items:
            if new_price < 0:
                print("Цена не может быть отрицательной.")
            else:
                self.items[item_name] = new_price
                print(f"Цена товара '{item_name}' обновлена.")
        else:
            print(f"Товар '{item_name}' не найден.")

    def get_all_items_with_prices(self):
        """Возвращает список всех товаров с их ценами."""
        return [(item, price) for item, price in self.items.items()]

    def to_dict(self):
        """Возвращает словарь, представляющий магазин."""
        return {
            "name": self.name,
            "address": self.address,
            "items": self.items
        }

    @classmethod
    def from_dict(cls, data):
        """Создает экземпляр Store из словаря."""
        return cls(data["name"], data["address"], data["items"])


class StoreManager:
    def __init__(self):
        self.stores = self.load_all_stores()

    def create_new_store(self):
        name = input("Введите название нового магазина: ")
        address = input("Введите адрес нового магазина: ")
        new_store = Store(name, address)
        self.stores.append(new_store)
        self.save_all_stores()
        return new_store

    def select_store(self):
        if len(self.stores) == 0:
            print("Нет доступных магазинов. Сначала создайте магазин.")
            return None
        print("\nДоступные магазины:")
        for i, store in enumerate(self.stores):
            print(f"{i + 1}. Название: {store.name}, Адрес: {store.address}")
        try:
            choice = int(input("Выберите магазин, введя его номер: "))
            selected_store = self.stores[choice - 1]
            return selected_store
        except (ValueError, IndexError):
            print("Некорректный ввод. Попробуйте снова.")
            return None

    def list_stores_and_their_items(self):
        if len(self.stores) == 0:
            print("Магазины отсутствуют.")
            return
        for store in self.stores:
            print(f"\nНазвание магазина: {store.name}\nАдрес: {store.address}")
            for item, price in store.get_all_items_with_prices():
                print(f"Товар: {item}, Цена: {price}")

    def edit_store(self, store):
        """Редактирует название и адрес магазина."""
        new_name = input(f"Введите новое название для магазина '{store.name}': ")
        new_address = input(f"Введите новый адрес для магазина '{store.address}': ")
        store.name = new_name
        store.address = new_address
        self.save_all_stores()

    def delete_store(self, store):
        """Удаляет магазин со всеми его товарами."""
        self.stores.remove(store)
        self.save_all_stores()
        print(f"Магазин '{store.name}' удален.")

    def save_all_stores(self, filename="all_stores_data.json"):
        """Сохраняет все магазины в файл."""
        with open(filename, "w") as file:
            json.dump([store.to_dict() for store in self.stores], file)

    def load_all_stores(self, filename="all_stores_data.json"):
        """Загружает все магазины из файла."""
        try:
            with open(filename, "r") as file:
                stores_data = json.load(file)
                return [Store.from_dict(data) for data in stores_data]
        except FileNotFoundError:
            print("Файл с данными не найден. Создается новый список магазинов.")
            return []

# Управление магазинами
if __name__ == "__main__":
    manager = StoreManager()
    while True:
        print("\n1. Создать новый магазин")
        print("2. Выбрать магазин")
        print("3. Список магазинов и их товары")
        print("4. Редактировать магазин")
        print("5. Удалить магазин")
        print("6. Выйти")
        choice = input("Введите номер действия: ")

        if choice == "1":
            manager.create_new_store()
        elif choice == "2":
            store = manager.select_store()
            if store:
                while True:
                    print("\n1. Добавить товар")
                    print("2. Удалить товар")
                    print("3. Обновить цену товара")
                    print("4. Список товаров и их цен")
                    print("5. Получить цену товара")
                    print("6. Вернуться в главное меню")
                    sub_choice = input("Введите номер действия: ")

                    if sub_choice == "1":
                        item_name = input("Введите название товара: ")
                        price = float(input("Введите цену товара: "))
                        store.add_item(item_name, price)
                        manager.save_all_stores()
                    elif sub_choice == "2":
                        item_name = input("Введите название товара для удаления: ")
                        store.remove_item(item_name)
                        manager.save_all_stores()
                    elif sub_choice == "3":
                        item_name = input("Введите название товара для обновления цены: ")
                        new_price = float(input("Введите новую цену товара: "))
                        store.update_item_price(item_name, new_price)
                        manager.save_all_stores()
                    elif sub_choice == "4":
                        store.get_all_items_with_prices()
                        for item, price in store.get_all_items_with_prices():
                            print(f"{item}: {price}")
                    elif sub_choice == "5":
                        item_name = input("Введите название товара: ")
                        print(f"Цена товара '{item_name}':", store.get_item_price(item_name))
                    elif sub_choice == "6":
                        break
                    else:
                        print("Некорректный ввод. Введите номер из меню.")
        elif choice == "3":
            manager.list_stores_and_their_items()
        elif choice == "4":
            store = manager.select_store()
            if store:
                manager.edit_store(store)
        elif choice == "5":
            store = manager.select_store()
            if store:
                manager.delete_store(store)
        elif choice == "6":
            break
        else:
            print("Некорректный ввод. Введите номер из меню.")