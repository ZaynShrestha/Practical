# 3. Create a function that accepts a list of numbers and returns the 
# largest number without using Python’s built-in max() function.

def find_largest(numbers):
    largest = numbers[0]

    for num in numbers:
        if num > largest:
            largest = num

    return largest

nums = [10, 60, 55, 67, 89, 34, 99, 200, 1536]

print("Largest number:", find_largest(nums))