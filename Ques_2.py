# 2. Write a program that asks the user to enter a number and prints its 
# multiplication table from 1 to 10 using a for loop.


num = int(input("Enter a number: "))

for i in range(1, 11):
    print(f"{num} x {i} = {num * i}")