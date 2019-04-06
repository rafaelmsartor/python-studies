
my_name = 'Rafael'
my_age = 32

def print_my_data():
    print( 'My name is ' + my_name + ' and my age is ' + str(my_age) )


def print_any_data( first_data, second_data ):
    print(str(first_data), str(second_data))


def print_number_of_decades_lived( ):
    print( 'I\'ve lived ' + str(int( my_age / 10 )) + ' decades')


print_my_data()

print_any_data('Nobody expects the spanish inquisition', 42 )

print_number_of_decades_lived()