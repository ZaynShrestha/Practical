# 4. Write a Python program that reads a text file and counts the total 
# number of words in it. Handle the case where the file does not exist 
# using exception handling.
 
filename = input("Enter the file name: ")

try:
     with open(filename, 'r') as file:
        content = file.read()

        words = content.split()
        print("Total number of words:", len(words))

except FileNotFoundError:

    print("Error: File does not exist.")

except Exception as e:
    
    print("An error occurred:", e)
