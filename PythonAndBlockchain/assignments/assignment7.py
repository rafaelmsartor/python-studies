
# 1) Create a Food class with a “name” and a “kind” attribute as well as a “describe() ” method (which prints “name” and “kind” in a sentence).
# 2) Try turning describe()  from an instance method into a class and a static method. Change it back to an instance method thereafter.
# 4) Overwrite a “dunder” method to be able to print your “Food” class.

class Food:

    name = ""
    kind = ""
        
    @classmethod
    def describe(cls):
        print('This is a {} food, called {}'.format(cls.kind, cls.name))


    def __repr__(self):
        return 'This is a {}'.format(self.name)



# 3) Create a  “Meat” and a “Fruit” class – both should inherit from “Food”. Add a “cook() ” method to “Meat” and “clean() ” to “Fruit”.

class Meat(Food):
     
    def __init__(self):
        self.__cooked = False
        self.kind = 'meat'


    def cook(self):
        self.__cooked = True
        print('The meat is cooked')


        
class Fruit(Food):

    def __init__(self):
        self.__clean = False
        self.kind = "fruit"
 

    def clean(self):
        self.__clean = True
        print('The Fruit is clean')


banana = Fruit()
banana.name = "banana"

banana.describe()
print( banana )