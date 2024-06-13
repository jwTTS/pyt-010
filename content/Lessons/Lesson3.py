#%% Section 8 - Functions
#Slide 45
#creating your own formulas that don't exist in Python
#also useful for creating "mini programs" that can be reused in your code
    #e.g. function that imports data from files, scrapes websites, etc.

def fnCube(x):
    cube = x ** 3
    return cube #outputting the result

def fnSquare(x):
    return x ** 2

#functions do not always have to return a value
def printGreeting(fName, lName):
    print("Hello " + fName + " " + lName)

#functions can return multiple outputs
def perimAreaRectangle(length, width):
    area = length * width
    perim = 2* (length + width)
    return perim, area 

#functions have to be written and loaded in memory before using them
    #typically declare functions at the top of our codes
x = 5
y = 10
print(fnSquare(x))

fnCube(y)
perim, area = perimAreaRectangle(x, y)

#%%% Lambda Functions
#Slide 47
#Advanced Topic
#Useful for writing simple "one-liner" functions

#lambda input(s): what to do with the input
lambdaSquare = lambda x: x**2

print(lambdaSquare(25))

hypLength = lambda x, y: (x**2 + y**2) ** 0.5 #could also use math.sqrt
print(hypLength(4,3))