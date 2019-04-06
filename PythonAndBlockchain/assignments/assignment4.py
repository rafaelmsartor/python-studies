# 1) Write a normal function that accepts another function as an argument. Output the result of that other function in your “normal” function.


def function_as_param(other_function):
    print(other_function())

# 2) Call your “normal” function by passing a lambda function – which performs any operation of your choice – as an argument.


power = 3
function_as_param(lambda: 2 ** power)

# 3) Tweak your normal function by allowing an infinite amount of arguments on which your lambda function will be executed.


def function_as_param_with_params(other_function, *other_params):
    print(other_function(other_params))


function_as_param_with_params(lambda params: [param * 2 for param in params], 1, 2, 3)

# 4) Format the output of your “normal” function such that numbers look nice and are centered in a 20 character column.

def function_as_param_with_params_formatted(other_function, *other_params):
    print('{:^20d}'.format(other_function(other_params)))

function_as_param_with_params_formatted(lambda params: len(params), 1, 2, 3, 4, 5)

