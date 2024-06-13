"""
Python Programming - Assignment 1 Questions
"""

#%% Exercise 1
#In this exercise you will practice creating variables and learn the behaviour of casting.
# 1. Create the following variable(s):
    # a. Assign 4.3 to j.
    # b. Assign 5.5 to k.
# 2. Calculate j * k and cast the result as an integer to a variable ‘i’.
    # a. To cast to integer use int().
# 3. Print the value and type of ‘i’.
# 4. Print the value and type of ‘j*k’.
# What do you notice about the behavior of casting a float to an integer?



################################################################

#%% Exercise 2
# Convert string $123,456,789 into a useable integer using .strip(), .split() and .join()

# In this exercise you will practice how to clean a numeric value that is stored as a string formatted for display purposes.
# 1. Assign '$123,456,789' to a variable name deal_value.
# 2. Use .strip() to remove the '$'.
    # a. Remember to use '' or "" around the $.
# 3. Use .split() to create a list divided at the commas.
# 4. Use .join() to create a string with no spaces in between.
# 5. Make the number useable (cast either to integer or float).
    # a. Check that you can multiply the number by 2.
    


################################################################

#%% Exercise 3
# In this exercise you will practice looping through values in a list and using if statements to control execution. 
# 1. Create the following list: [100, 99, 105, 110, 95, 102] and store the values in variable named 'mylist'.
# 2. Loop through the elements in the list and perform the following inside the loop:
    # a. If > 102 print "Sell"
    # b. If < 100 print "Buy"
    # c. Else print "Hold"

mylist = [100,99,105,110,95,102]



################################################################

#%% Exercise 4
# In this exercise your will practice using dictionaries and how to structure if statements effectively. 
# Create a script that converts number grades to letter grades.
# 1. Create the following dictionary {'Bob':71, 'Alice':65, 'Jim':70, 'Jen':90, 'Tim':86, 'Trish':85, 'Tony':75}
     # and store the values in a variable named ‘grades’.
# 2. Loop through the keys in the ‘grades’ dictionary and convert each grade into letters following the rules below.
     # Store the letter grades in a new dictionary. 
# Hint: create an empty dictionary named ‘letter_grades’ before the loop (letter_grades = {}).
# Hint: use if/elif/else statement in a clever order so that you only need one logical check per if.
    # a. 90 and above: A+
    # b. 85-90: A
    # c. 80-85: A-
    # d. 75-80: B+
    # e. 70-75: B
    # f. 65-70: B-
# 3. Print the new dictionary with letter grades and double check that the letter grades correspond with 
    # the proper number grades in the original dictionary.

grades = {'Bob':71, 'Alice':65, 'Jim':70, 'Jen':90, 'Tim':86, 'Trish':85, 'Tony':75}


################################################################

#%% Exercise 5
# In this exercise you will practice removing items from a list.
# 1. Create the following list: mylist = ['A', 'B', 'C', 'D', 'D', 'D'].
# 2. Create a loop using the syntax while ‘D’ in mylist, that will remove all instances of ‘D’ from the list.
    # a. Since .remove() will only remove the first instance of ‘D’, 
        # we need to use a loop to remove all instances of ‘D’ from the list.

mylist = ['A','B','C','D','D','D']


################################################################

#%% Exercise 6
#Convert string $123,456,789 into a useable integer

# For this exercise, we will repeat Exercise 2, but instead of casting the whole string as a number, we will cast each individual chunk then combine them by adding the numbers (e.g. 123,000,000 + 456,000 + 789). You will practice using for loops using a range, and programming logic.
# 1. Use .split() to get a list ['123', '456', '789'].
# 2. Use a for loop to iterate over the range 0 to 2.
# Hint: The function len() will get you the number of elements.
# Hint: Initialize the variable you will store the sum before the loop.
# 3. Inside the loop, cast each number to an integer, and multiply by 1,000^(number of elements – index - 1) to get the proper magnitude.
# Hint: To access the values stored in the list, use the loop index: mylist[i].


################################################################

#%% Exercise 7
# In this exercise you will practice using functions, working with lists & dictionaries and formatting output. 
    # The function will simulate random prices movements of stocks.
# 1. Create a dictionary with the following {'AAPL':100.0, 'CAT':50.0, 'MSFT':150}.
    # These will be the starting prices for tickers AAPL, CAT, MSFT.
# 2. Create a function that takes the dictionary as defined above and generates 5 random prices movements
     # using the standard normal distribution. Store each of the movements in a dictionary and return this dictionary.
# Hint: Remember that you can only store a single value for each key, you will need to use a list to store
         # the five prices movements ({key:[list]}).
# 3. The output should be formatted to display the ticker name and then the five price movements,
     # to two (2) decimal places, in one line. e.g.:
        # AAPL: $99.44, $98.99, $100.31, $99.09, $98.59
        # CAT: $51.47, $49.77, $50.07, $48.58, $49.46
        # MSFT: $150.11, $148.85, $150.38, $149.40, $149.71
        # AAPL $100, CAT $50, MSFT $150

################################################################

#%% Exercise 8
#generate an array of simulated monthly returns (60 obs), with means 1-5 and std 1-5, 25 total assets

# In this exercise you will practice using matrices and generating random numbers.
#1. Use a nested loop to generate a matrix of simulated monthly returns with means 1 to 5 and standard deviation 1 to 5 for each. 
    #a. 25 total assets, 60 returns for each
    #b. Have each column be an asset, and rows be the return observations (this will result in a 60x25 matrix).
    #c. Each asset has a different combination of mean/standard deviation for monthly returns (e.g. the first 5 assets will have means of 1, and standard deviation of 1 to 5, the next 5 assets will have means of 2, etc.)
    #d. We will assume IID, so each draw is unique and not dependent on the previous draws.
#2. Find the covariance matrix and store the result in a variable, using np.cov(matrix).
#3. Find the inverse of the covariance matrix, if possible, and verify the inverse is correct (Remember that A^(-1) A=I).

#Challenge: Verify that the covariance matrix is positive definite.
#Hint: The Cholesky Decomposition A=LL' only holds for positive definite matrices.