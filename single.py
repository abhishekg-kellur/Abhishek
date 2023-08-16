class Animal:
    def __init__(self, name):
        self.name = name
    def eat(self):
        print(f"{self.name} is eating.")
class Dog(Animal):
    def bark(self):
        print(f"{self.name} is barking.")
my_dog = Dog("Buddy")
my_dog.eat()
my_dog.bark()
