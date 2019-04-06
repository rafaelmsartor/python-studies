
def print_header(header_text):
    print(header_text)
    print('-' * len(header_text))

# 1) Create a list of names and use a for loop to output the length of each name (len() ).


names_list = ['Rafael', 'Fernanda', 'Anthony',
              'Maria', 'Ana', 'Joe', 'Nathaly', 'Noah']

print_header('First Task')

for name in names_list:
    print(name + ': ' + str(len(name)))

print()

# 2) Add an if  check inside the loop to only output names longer than 5 characters.

print_header('Second task')

for name in names_list:
    if len(name) > 5:
        print(name + ': ' + str(len(name)))

print()

# 3) Add another if  check to see whether a name includes a “n”  or “N”  character.

print_header('Third task')

for name in names_list:
    if len(name) > 5 and ('n' in name or 'N' in name):
        print(name + ': ' + str(len(name)))

print()

# 4) Use a while  loop to empty the list of names (via pop() )

print_header('Fourth task')

print('List before emptying: ' + str(names_list))

while len(names_list) > 0:
    names_list.pop()

print('List after emptying: ' + str(names_list))
