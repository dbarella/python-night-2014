'''
Make sure you put info about your programs 
and yourself at the top of your programs!

This is just a demo script to accompany python night, 
and to remind you of the cool stuff that we taught!

Function-writing stuff
- First-class functions
- Decorators
- With statements
- Comprehensions

TODO:
- Named arguments, splats, *args, **kwargs

Class-writing stuff
- Magic methods
- Subclassing builtins to do cool stuff

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

#--- Function-writing stuff. Write better functions ---
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

	# Because functions are objects, you can make new vars that refer to them and call them later
	f = function

	'''
	You can check that they point to the same function in memory by using an assert statement

		(the `is` keyword compares memory addresses)

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
		Bet you didn't know this was possible ;)

		We're defining a new function inside of this function
			(Sure you can use lambdas but I think they are less readable when being introduced to the idea)
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

#!!! The special sauce !!!
get_tok = re.compile(tok_regex).match #match is a function in the regex library that takes a string

#Later on you can just call get_tok on a string, and it will return a regex match object
match_object = get_tok(line)

#This way you don't need to re-compile the regex each time you use it, which takes more memory and slows things down
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
        		# assert(isinstance(args[0], str))
                print("I'm the wrapper function!")
                result = function(to_paragraph(args[0]))
                # assert(isinstance(result, str))
                return result
        print('done wrapping...')
        return wrapper

# We apply decorators to functions by using the @-syntax.

@to_paragraph_decorator
def decorated_cool_string(string):
        return string + '. Whoaaaaa cool.'

# decorated_cool_string = to_paragraph_decorator(decorated_cool_string)

# Decorators are used in a variety of different ways. For example,
# some Python web frameworks use decorators in order to route URLs to
# the appropriate handler function. You can also easily implement
# caching/memoization with a decorator, or enforce type-correctness of
# function arguments and results.

#--- With statements ---

# There are many operations in programming which involve getting some
# resource, doing something with it, and then disposing of the
# resource. For example, you need to open a file to read from it, and
# you should generally close the file as soon as you're done with
# it. But this leads to repetitive code (open, do something, close,
# open, do something, close, etc.). Furthermore, what if you forget
# to close the file?

# With statements abstract away the opening and closing, allowing us
# to write cleaner code and be sure we'll always dispose of the
# resource correctly (even in the face of exceptions).

def using_with_statement(filename):
        '''
        A with statement consists of the syntax:

        with <some resource> as <variable name>:
            <do stuff here>
        '''
        contents = None
        with open(filename) as f:
                contents = f.read()
        return contents

# The given file will always be closed once the with statement
# completes. Cool!

# With statements are used in a variety of contexts, like ensuring
# that locks (a concurrency primitive) as used correctly.


#--- Comprehensions ---
'''
Probably one of the most powerful python shorthands
'''
def dup_n_times_old(item, n, prompt0=None, prompt1=None, *args, **kwargs):
	'''
	Say we want to return a list of n 'item's. 
	The typical way to do that would be:'''
	
	print('args: {0}\nkwargs: {1}'.format(args, kwargs))

	if prompt0:
		print(prompt0, prompt1)

	temp = []
	for i in range(n):
		temp.append(item)

	return temp

def dup_n_times_comp(item, n):
	'''
	There is a shorthand to do exactly the same thing, called a list comprehension.
	These are a way to construct lists by specifying what you want in them
	'''

	# List Comps become lists - Note the [] braces:
	# [<object> for thing in <iterable>] -> [<object>, <object>, ..., <object>]
	[0 for i in range(5)] # -> [0, 0, 0, 0, 0]

	# [thing for thing in <iterable>] -> [thing0, thing1, ..., thing_N_minus_1]
	[i for i in range(5)] # -> [0, 1, 2, 3, 4]

	# You can also do awesome filtering using if/else conditions
	# [thing for thing in <iterable> if condition(thing)] -> [thing0, thing1, ..., thing_N_minus_1]
	# [function(thing) for thing in <iterable>] -> [function(thing0), function(thing1), ..., function(thing_N_minus_1)]
	[i for i in range(10) if i%2 == 1] #Becomes a list of odd numbers from 0 to 10
	[i**2 for i in range(10)] #Becomes a list of squares
	[i**2 for i in range(10) if i%2 == 1] #Becomes a list of squares of odd numbers

	#if-else
	[i if i%2 == 0 else i+100 for i in range(5)]

	#DICTIONARY COMPS
	#{key: val for key in <iterable0> for val in <iterable1>}
	{}

	return [item for i in range(n)]

#--- Named args, splats, *args, **kwargs ---	
#TODO

#--- Class writing stuff. How to make your classes cooler ---
#--- Magic Methods ---
'''
We'll cover magic methods briefly, but they are amazingly powerful for writing beautiful code.
Magic methods are all the methods that have double-underscores (dunders) around them

Many smarter people than us have written about this. 
See http://www.rafekettler.com/magicmethods.html for a great post.
'''
class ListWrapper(object):
	'''
	I wrote ListWrapper(object) on purpose
					   ^^^^^^^^

	This is a 'new-style' class definition, different from the old-style definitions
		which looked like 'class ListWrapper:'
	It allows you to use both inheritance and the new class methods
	'''

	def __init__(self, *args):
		'''
		__init__ is a magic method, but you always have to define it to do anything useful
		'''
		self.data = args

	def __len__(self):
		'''
		Called whenever you write `len(thing)`
		'''
		return len(self.data)

	def __getitem__(self, key):
		'''
		This method is called whenever you write `thing[key]`
		'''
		return self.data[key]

	def __setitem__(self, key, value):
		'''
		This method is called when you write `thing[key] = value`,
			and then sets the item at index `key` to be `value`.
		'''
		self.data[key] = value

	# Don't use del.
	# def __delitem__(self, key):
	# 	'''
	# 	Called whenever `del thing[key]` is called
	# 	'''
	# 	del self.data[key]

	def __add__(self, other):
		'''
		Define your own addition. Be careful to return a new object, not to modify self.
		'''
		return self.data + other.data

	def __str__(self):
		'''
		String representation of this object
		'''
		return '{0}'.format(self.data) #Equivalent to str(self.data)

	def __repr__(self):
		'''
		Usually called only by the interpreter to represent your object
		
		In this case I want it to be the same as __str__
		'''
		return str(self) #or you could write self.__str__() or a bunch of other crap

class DefaultDict(dict):
	'''
	Here's an example of something that might actually be useful, 
		via https://www.python.org/download/releases/2.2.3/descrintro 
	Here we're subclassing the builtin dict object
	'''

	def __init__(self, default=None):
		dict.__init__(self)
		self.default = default

	def __getitem__(self, key):
		try:
			return dict.__getitem__(self, key)
		except KeyError:
			return self.default

	def get(self, key, *args):
	    if not args:
	        args = (self.default,)
	    return dict.get(self, key, *args)

def main():
	if DEBUG:
		print("Debugged")

	print(caller(square, 5))
	
	square_of_plus_one = compose(square, plus_one)
	print(square_of_plus_one(1))

	plus_one_of_square = compose(plus_one, square)
	print(plus_one_of_square(1))

	print(decorated_cool_string('Look at this string.'))

	print(using_with_statement('file.txt'))

	print(dup_n_times_comp('cat', 5))

	#Class stuff
	l = ListWrapper(1, 2, 3)
	
	#for loops use the __iter__ method to iterate over the contained objects
	for item in l:
		print(item)

	d = DefaultDict('DEFAULT')
	d['a'] = 5

	print(d['a']) # 5
	print(d['b']) # DEFAULT



#--- Misc. Cool Stuff.
'''
This is a good way of defining main() methods and having them only run when you do:
	python program.py

and not when you do: 
	import program

from another program'''

if __name__ == '__main__':
	main()

'''
Explanation:

__name__ is a special variable which is set by the python interpreter. 
It will be '__main__' if your program is being run from the command line,
	but if your program is being imported by some other script, it will be
	the name of your program. For example:'''

print(__name__)

'''
<From the python3 interpreter>
>>> import demo #When imported, this file prints 'demo'
demo

<From the command line>
Dan$ python3 demo.py
__main__

Note: This may not always print demo when imported (imports of imports of imports)
But when run from the command line it will always print '__main__' 
'''
