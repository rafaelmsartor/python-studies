#1) Import the random function and generate both a random number between 0 and 1 as well as a random number between 1 and 10.
import random

print(random.random())
print((random.random()*9) + 1)

#2) Use the datetime library together with the random number to generate a random, unique value.
import datetime

print(str(datetime.datetime.today()) + str(int(random.random()*1000)))
