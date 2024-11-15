# TODO: Создать 10+ классов в предметной области "интернет-магазин электронной техники"

class Product:
    def __init__(self, name, price, description, stockQuantity, category):
        self.__name = name
        self.__price = price
        self.__description = description
        self.__stockQuantity = stockQuantity
        self.__category = category

    def getDetails(self):
        return f'{self.__name}'


p = Product('Carrot', 178, 'orange veg', 150, 'Vegetable')

print(p.getDetails())
