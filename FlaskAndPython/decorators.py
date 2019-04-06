import functools

# simple decorator that wraps arround a function
def my_decorator( func ):
    @functools.wraps( func )
    def function_that_runs_func():
        print( "I'm in the decorator!" )
        func()
        print( "After the decorator!" )
    return function_that_runs_func

# use the decorator on the function
@my_decorator
def my_function():
    print( "Inside the function" )

#my_function()

#######################################################################

# a decorator that accepts parameters
def decorator_with_parameters( number ):
    def new_decorator( func ):
        @functools.wraps( func )
        def function_that_runs_func( *args, **kwargs ):
            print( "I'm in the decorator!" )
            if number == 42:
                print( "The answer is already given, won't run the function" )
            else:
                func( *args, **kwargs )
            print( "After the function" )
        return function_that_runs_func
    return new_decorator

@decorator_with_parameters( 42 )
def other_function():
    print( "This shouldn't run" )

@decorator_with_parameters( 43 )
def other_function2( ):
    print( "This should run" )

other_function()
other_function2()