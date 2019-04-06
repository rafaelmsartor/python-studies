#1) Create a list of “person” dictionaries with a name, age and list of hobbies for each person. Fill in any data you want.

people = [
    {
        'name'   : 'Rafael',
        'age'    : 32,
        'hobbies': ['reading', 'playing guitar']
    },
    { 
        'name'   : 'Fernanda',
        'age'    : 32,
        'hobbies': ['painting', 'playing videogames']
    },
    {
        'name'   : 'Slothinger',
        'age'    : 20,
        'hobbies': ['sleeping']

    }
]

#2) Use a list comprehension to convert this list of persons into a list of names (of the persons).

names = [person['name'] for person in people]
print(names)

#3) Use a list comprehension to check whether all persons are older than 20.

older_check = all([person['age'] > 20 for person in people])
print(older_check)

#4) Copy the person list such that you can safely edit the name of the first person (without changing the original list).

new_people = [person.copy() for person in people]
new_people[0]['name'] = "Xatu"
print(people[0]['name'])
print(new_people[0]['name'])

#5) Unpack the persons of the original list into different variables and output these variables.
a, b, c = people
print( a )
print( b )
print( c )