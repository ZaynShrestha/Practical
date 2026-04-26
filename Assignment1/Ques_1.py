# 1. Write a Python program that takes a student’s marks as input and 
# prints the grade based on the following criteria:

#90 and above → A
# 80 to 89 → B
# 70 to 79 → C
# 60 to 69 → D
# Below 60 → Fail


marks = int(input("Enter the students marks :   "))

if (marks >=90):
    print("Grade A")

elif (marks >=80 and marks <89):
    print("Grade B")

elif (marks >=70 and marks <79):
    print("Grade C")

elif (marks >=60 and marks <69):
    print("Grade D")

else:
    grade = ("60")
    print ("NO Grade Fail")
