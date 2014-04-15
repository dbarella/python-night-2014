'''
Make sure you put info about your programs 
and yourself at the top of your programs!

This is just a demo script to accompany python night, 
and to remind you of the cool stuff that we taught!

Dan Barella <dbarella@oberlin.edu>
'''

# Sometimes it's appropriate to do stuff like this.
# This is from a program I wrote over winter term at UW in Seattle

__status__ = "Beta"
__author__ = "Daniel Barella"
__email__ = "dan.barella@gmail.com"
__copyright__ = "Copyright (c) 2013 SCCL, University of Washington (http://depts.washington.edu/sccl)"
__license__ = "GPL"
__version__ = "0.2"

# These are actually variables in your program, which can be referenced by other scripts
# if they import this file

# Here's a nifty trick:
DEBUG = False


#--- First-class functions ---
def square(n):
	'''
	Just a stupid function to pass around.
	'''
	return n*n

def plus_one(n):
	return n+1

def caller(function, thing):
	'''
	Example of first-class functions. This is just a fancy way of saying that
	functions are objects. You can pass them around and call them whenever you want
	'''

	# Because functions are objects, you can make new vars that refer to them
	f = function

	'''
	You can check that they point to the same function in memory by doing
	Assertions are great for defensive programming, if you want to make sure
	in one line that something is true, instead of assuming that it is
		http://en.wikipedia.org/wiki/Assertion_(computing)

	When assertions fail, they raise an AssertionException
	Be careful about depending on assertions – in python they can be removed
	by running the interpreter with the -oo flags (optimize). You should only
	use them for sanity checks, like making sure that something is an object.
	'''
	assert f is function

	return f(thing)

def compose(f, g):
	'''
	Take in two functions, and return a function that composes them on one argument
	'''

	def result(n):
		'''
		Bet you didn't know this was possible (;
		'''
		return f(g(n))

	# Remember that names in python are all tags on objects
	# When we say 'return result', we're returning the function that we just defined.
	# i.e. You don't have to just call functions, you can treat them like objects
	return result

'''
Here's a real-world example from some code I wrote in Compilers (CS331)

<import regex at the top of the program>

tok_spec = [
            ('T_NUM',           r'\d+'),                       #Numbers
            ('T_STRING',        r'"[^"]*"'),                   #Strings
            ('IGNORE',          r'\s|\n'),                     #Ignore spaces and newlines
        ]

tok_regex = '|'.join('(?P<{0}>{1})'.format(*pair) for pair in tok_spec) #Named regex pairs for each item in tok_spec
get_tok = re.compile(tok_regex).match #Regex match function

#Later on you can just call get_tok on a string, and it will return a regex match object
match_object = get_tok(line)
'''

#--- Decorators ---

# Like the `compose` function above, sometimes we want to modify the
# functionality of one function in some generic way *without* changing
# the function itself. Python provides a feature to generalize
# function composition, called function decorators.

def to_paragraph(string):
        '''
        Returns the given string, wrapped in HTML paragraph tags.
        '''
        return '<p>' + string + '</p>'

# The above function will allow us to turn any string into an HTML
# paragraph (without proper HTML escaping, but that's a whole
# different topic).

def a_cool_string(string):
        'Makes strings really cool.'
        return string + '. Whoaaaaa cool.'

# Now, what if we want to wrap the `string` argument of
# `a_cool_string` in paragraph tags? We could either call
# `to_paragraph` inside the function, OR we could use a decorator.

def to_paragraph_decorator(function):
        '''
        Decorators are just regular functions. They are given a
        function as an argument (so they're higher-order functions),
        and they return one as a result.

        The power of decorators is that when we apply them, as we'll
        see later, they take the function they're applied to as an
        argument, and get a chance to replace it with something
        else. Usually that something else is a new function which
        wraps the old one.

        This all gets done when the function is being defined, so the
        code in this function will be run once.
        '''
        print('wrapping function...')
        def wrapper(*args):
                print("I'm the wrapper function!")
                return function(to_paragraph(args[0]))
        print('done wrapping...')
        return wrapper

# We apply decorators to functions by using the @-syntax.

@to_paragraph_decorator
def decorated_cool_string(string):
        return string + '. Whoaaaaa cool.'

# Decorators are used in a variety of different ways. For example,
# some Python web frameworks use decorators in order to route URLs to
# the appropriate handler function. You can also easily implement
# caching/memoization with a decorator, or enforce type-correctness of
# function arguments and results.

def main():
	if DEBUG:
		print("Debugged")

	print(caller(square, 5))
	
	square_of_plus_one = compose(square, plus_one)
	print(square_of_plus_one(1))

	plus_one_of_square = compose(plus_one, square)
	print(plus_one_of_square(1))

	print(decorated_cool_string('Look at this string.'))

''' 
__name__ is a special variable which is set by the python interpreter. 
It will be '__main__' if your program is being run from the command line,
	but if your program is being imported by some other script, it will be
	the name of your program. For example:

<From the python3 interpreter>
>>> import demo
demo 
'''
if __name__ == '__main__':
	main()

print(__name__)
