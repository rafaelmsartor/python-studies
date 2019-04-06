# 1) Write a short Python script which queries the user for input (infinite loop with exit possibility) and writes the input to a file.
# 2) Add another option to your user interface: The user should be able to output the data stored in the file in the terminal.

waiting_for_input = True
data_filename = 'data_output.txt'

def handle_user_input(user_data):
    with open(data_filename, 'a') as f:
        f.write(user_data + '\n')


def handle_file_output():
    with open(data_filename, 'r') as f:
        for data in f.readlines():
            print(data[:-1])

while waiting_for_input:

    print('Enter one of the following choices:')
    print('i: input data to a text file')
    print('o: output the data from the file')
    print('q: exit the program')

    user_choice = input('#: ')

    if user_choice == 'i':
        print('Please input your data now')
        user_data = input()
        handle_user_input(user_data)
    elif user_choice == 'o':
        handle_file_output()
    elif user_choice == 'q':
        print('Exiting the program')
        break


# 3) Store user input in a list (instead of directly adding it to the file) and write that list to the file – both with pickle and json.
# 4) Adjust the logic to load the file content to work with pickled/ json data.

import json
import pickle

waiting_for_input = True
json_filename = 'data_output.txt'
pickle_filename = 'data_output.p'
user_input_list = []

USE_JSON = False

def handle_user_input(user_data):
    user_input_list.append(user_data)
    write_to_file()

def write_to_file():
    if USE_JSON:
        with open(json_filename, 'w') as f:
            f.write(json.dumps(user_input_list))
    else:
        with open(pickle_filename, 'wb') as f:
            f.write(pickle.dumps(user_input_list))


def handle_file_output():
    load_from_file()
    for data in user_input_list:
            print(data)


def load_from_file():
    global user_input_list
    if USE_JSON:
        with open(json_filename, 'r') as f:
            user_input_list = json.loads(f.read())
    else:
        with open(pickle_filename, 'rb') as f:
            user_input_list = pickle.loads(f.read())


while waiting_for_input:

    print('Enter one of the following choices:')
    print('i: input data to a text file')
    print('o: output the data from the file')
    print('q: exit the program')

    user_choice = input('#: ')

    if user_choice == 'i':
        print('Please input your data now')
        user_data = input()
        handle_user_input(user_data)
    elif user_choice == 'o':
        handle_file_output()
    elif user_choice == 'q':
        print('Exiting the program')
        break
