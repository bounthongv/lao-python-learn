-- English lessons for Lao Python Learning Platform
--
-- These are the reference version of the five Lao lessons: same sections, same
-- code samples, plain English. Read a section here to know what the Lao text is
-- supposed to say.
--
-- IMPORTANT: lesson text is dollar-quoted ($$...$$) and must contain REAL newlines.
-- A '\n' inside a plain '...' string is stored by Postgres as a literal backslash-n,
-- which collapses each lesson into one line and stops markdown rendering.
--
-- This file needs the lang column, so it runs AFTER migrate_multilingual.sql.

INSERT INTO lessons (title, slug, content_markdown, example_code, "order", lang) VALUES
(
    $$1. Python Basics$$,
    $$lesson-1-basics-en$$,
    $$## Python Basics

Python is a programming language that is easy to read. Its code looks close to
plain English, so it is a good first language to learn.

### Installing Python

1. Go to https://python.org/downloads
2. Download the installer
3. **Important:** tick the box "Add Python to PATH"
4. Click Install

### Writing Code

```python
# Show a message on the screen
print("Hello! I am learning Python")

# Variables: boxes that hold values
name = "Somchit"
age = 15
height = 1.65

# The data type of each variable
print(name)        # str   (text)
print(age)         # int   (whole number)
print(height)      # float (number with a decimal point)
```

### Getting Input from the User

```python
name = input("What is your name? ")
print(f"Hello, {name}!")
```$$,
    $$# Basic example
print("Hello! I am learning Python")

name = "Student"
age = 16
print(f"Name: {name}, Age: {age}")$$,
    1,
    $$en$$
),
(
    $$2. Conditions$$,
    $$lesson-2-conditions-en$$,
    $$## Conditions (if / elif / else)

A condition lets the program choose what to do, depending on a test that is
either True or False.

### A Single if / else

```python
score = 85

if score >= 50:
    print("Pass")
else:
    print("Fail")
```

### if - elif - else

Use elif when there are more than two possible results. The tests are checked
from top to bottom, and only the first one that is True runs.

```python
score = int(input("Enter your score: "))

if score >= 80:
    grade = "A"
elif score >= 70:
    grade = "B"
elif score >= 60:
    grade = "C"
elif score >= 50:
    grade = "D"
else:
    grade = "F"

print(f"Grade: {grade}")
```

### Nested Conditions

A condition can be placed inside another condition.

```python
age = 20
has_id = True

if age >= 18:
    if has_id:
        print("Allowed in")
    else:
        print("Bring your ID card")
else:
    print("You are too young")
```

### Combining Conditions (Logical Operators)

```python
age = 20
is_student = True
is_teacher = False
is_banned = False

# and - both sides must be True
if age >= 18 and is_student:
    print("OK")

# or - at least one side must be True
if is_student or is_teacher:
    print("Discount")

# not - reverses True into False
if not is_banned:
    print("Allowed in")
```$$,
    $$# Condition example
score = 75

if score >= 80:
    print("Excellent")
elif score >= 50:
    print("Pass")
else:
    print("Fail")

# Nested condition example
age = 20
if age >= 18:
    print("Adult")
    if age >= 60:
        print("Senior citizen")$$,
    2,
    $$en$$
),
(
    $$3. Loops$$,
    $$lesson-3-loops-en$$,
    $$## Loops (for / while)

A loop repeats a block of code, so you do not have to write it again and again.

### for Loop

```python
# Repeat using a counter
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

# Repeat over the items of a list
fruits = ["mango", "orange", "pineapple"]
for fruit in fruits:
    print(f"I like eating {fruit}")
```

### range() in Detail

range(start, stop) counts from start up to, but not including, stop.

```python
range(5)         # 0, 1, 2, 3, 4
range(1, 6)      # 1, 2, 3, 4, 5
range(1, 10, 2)  # 1, 3, 5, 7, 9 (step of 2)
range(10, 0, -1) # 10, 9, ..., 1 (counting down)
```

### while Loop

A while loop keeps going as long as its condition is True. Something inside the
loop must change the condition, otherwise it never stops.

```python
count = 1
while count <= 5:
    print(count)
    count += 1  # same as count = count + 1
```

### break and continue

```python
# break - leave the loop completely
for i in range(10):
    if i == 5:
        break
    print(i)  # 0-4

# continue - skip this round and move on to the next one
for i in range(5):
    if i == 2:
        continue
    print(i)  # 0, 1, 3, 4
```

### Nested Loops

A loop inside another loop. The inner loop runs fully for every single round of
the outer loop.

```python
# Multiplication table
for i in range(1, 4):
    for j in range(1, 4):
        print(f"{i} x {j} = {i*j}")
    print("---")
```$$,
    $$# Loop example
for i in range(1, 6):
    print(f"Round {i}")

# while example
count = 10
while count > 0:
    print(count)
    count -= 1
print("Finished!")$$,
    3,
    $$en$$
),
(
    $$4. Lists$$,
    $$lesson-4-lists-en$$,
    $$## Lists

A list keeps many values inside one variable, in a fixed order.

### Creating a List

```python
# Square brackets, with values separated by commas
empty = []
numbers = [1, 2, 3, 4, 5]
names = ["Somchit", "Suksan", "Dao"]
mixed = [1, "hello", 3.14, True]
```

### Accessing Items (Indexing)

The first item is at position 0, not 1. A negative position counts from the end.

```python
fruits = ["mango", "orange", "pineapple"]

print(fruits[0])   # mango (position 0)
print(fruits[1])   # orange
print(fruits[-1])  # pineapple (the last item)
```

### Changing and Adding Items

```python
fruits = ["mango", "orange", "pineapple"]

fruits[0] = "chilli"        # change one item
fruits.append("guava")      # add at the end
fruits.insert(1, "apple")   # insert at position 1
```

### Removing Items

```python
fruits = ["mango", "orange", "pineapple"]

fruits.remove("orange")   # remove by value
popped = fruits.pop()     # remove the last item and hand it back
```

### Slicing a List

Slicing takes part of a list and gives you a new list.

```python
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

print(numbers[2:5])   # [2, 3, 4]
print(numbers[:3])    # [0, 1, 2]
print(numbers[-3:])   # [7, 8, 9]
print(numbers[::2])   # [0, 2, 4, 6, 8] (every second item)
```

### Important List Methods

```python
fruits = ["mango", "orange", "pineapple", "mango"]

print(len(fruits))                # 4  how many items
print(fruits.count("mango"))      # 2  how many times that value appears
print(fruits.index("orange"))     # 1  first position of that value

fruits.sort()
print(fruits)

fruits.reverse()
print(fruits)
```$$,
    $$# List example
students = ["Somchit", "Suksan", "Dao"]

# Add a new student
students.append("Nid")

# Show all of them, numbered from 1
for i, name in enumerate(students, 1):
    print(f"{i}. {name}")

# How many in total?
print(f"Total: {len(students)} students")$$,
    4,
    $$en$$
),
(
    $$5. Functions$$,
    $$lesson-5-functions-en$$,
    $$## Functions

A function is a named block of code. You write it once and call it as many
times as you need.

### Creating a Function

```python
# No parameter
def greet():
    print("Hello!")

greet()  # call the function

# With a parameter
def greet_name(name):
    print(f"Hello, {name}!")

greet_name("Somchit")

# With a return value
def add(a, b):
    return a + b

result = add(5, 3)
print(result)  # 8
```

### Default Parameters

A parameter can carry a default value, which is used when the caller gives
nothing for it.

```python
def greet(name, greeting="Hello"):
    print(f"{greeting}, {name}!")

greet("Somchit")                 # Hello, Somchit!
greet("Suksan", "Good morning")  # Good morning, Suksan!
```

### Returning More Than One Value

```python
def calculate(a, b):
    return a + b, a - b, a * b, a / b

sum_, diff, prod, quot = calculate(10, 2)
print(sum_, diff, prod, quot)  # 12 8 20 5.0
```

### Variable Scope

A variable created inside a function only exists inside that function.

```python
global_var = "I am available everywhere"

def my_func():
    local_var = "I only exist inside my_func"
    print(global_var)  # OK
    print(local_var)   # OK

my_func()
print(global_var)      # OK
# print(local_var)     # Error: local_var is not defined
```

### Lambda Functions

A lambda is a small, unnamed function written on a single line.

```python
# Same as: def square(x): return x * x
square = lambda x: x * x
print(square(5))  # 25

# Handy with map() and filter()
numbers = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x*x, numbers))
evens = list(filter(lambda x: x%2==0, numbers))
print(squares)  # [1, 4, 9, 16, 25]
print(evens)    # [2, 4]
```$$,
    $$# Function example
def greet(name):
    return f"Hello, {name}!"

print(greet("Student"))

# Area of a rectangle
def rectangle_area(width, height):
    return width * height

print(f"Area: {rectangle_area(5, 3)}")$$,
    5,
    $$en$$
)
ON CONFLICT (slug) DO UPDATE SET
    title = EXCLUDED.title,
    content_markdown = EXCLUDED.content_markdown,
    example_code = EXCLUDED.example_code,
    "order" = EXCLUDED."order",
    lang = EXCLUDED.lang;

-- Exercises for the English lessons. Each lesson has three to four tasks and a
-- matching solution, shown in the "Try it" and "Solution" panels under the lesson.
-- Anything that reads input() says what to type in the Input box.

UPDATE lessons SET
exercises_markdown = $$1. Use an f-string to print one sentence about yourself: your name, your age and your favourite food.

2. Ask for a name with `input()` and print `Hello, <name>!`. Type the name in the **Input** box above the Run button before you press Run.

3. Ask for two whole numbers and print their sum. Remember that `input()` always hands back *text*, so turn it into a number with `int()` first.$$
,
exercise_solutions = $$**1.**

```python
name = "Dao"
age = 15
food = "sticky rice"
print(f"My name is {name}, I am {age} years old and I like {food}.")
```

**2.**

```python
name = input("What is your name? ")
print(f"Hello, {name}!")
```

Type `Somchit` in the Input box.

**3.**

```python
a = int(input("First number: "))
b = int(input("Second number: "))
print(f"{a} + {b} = {a + b}")
```

Type `5` and `3` in the Input box, one per line.$$
WHERE slug = 'lesson-1-basics-en';

UPDATE lessons SET
exercises_markdown = $$1. Ask for a number and print `positive`, `negative` or `zero`.

2. Ask for an age and print `child` (under 13), `teenager` (13 to 19) or `adult`. Use one `if / elif / else` chain, not three separate `if` statements.

3. A bus ticket costs 20000 LAK. Children under 12 and students of any age travel for half price. Ask for the age, then ask if the person is a student (`yes` or `no`), and print the price. Use `or`.$$
,
exercise_solutions = $$**1.**

```python
n = int(input("Number: "))

if n > 0:
    print("positive")
elif n < 0:
    print("negative")
else:
    print("zero")
```

**2.**

```python
age = int(input("Age: "))

if age < 13:
    print("child")
elif age <= 19:
    print("teenager")
else:
    print("adult")
```

**3.**

```python
age = int(input("Age: "))
student = input("Are you a student? (yes/no) ")

if age < 12 or student == "yes":
    print("Price: 10000 LAK")
else:
    print("Price: 20000 LAK")
```

Try `age = 20` and `yes` in the Input box: the answer is 10000 LAK.$$
WHERE slug = 'lesson-2-conditions-en';

UPDATE lessons SET
exercises_markdown = $$1. Print the 7 times table, from `7 x 1` to `7 x 10`, one line each.

2. Add up every number from 1 to 100 inside a loop and print the total. Check that you get 5050.

3. Print the odd numbers counting down from 21 to 1 using one `range()` call, then print `Done!`.

4. Print a square of stars, 5 rows by 5 columns, using a loop inside a loop.$$
,
exercise_solutions = $$**1.**

```python
for i in range(1, 11):
    print(f"7 x {i} = {7 * i}")
```

**2.**

```python
total = 0
for i in range(1, 101):
    total += i
print(total)  # 5050
```

**3.**

```python
for i in range(21, 0, -2):
    print(i)
print("Done!")
```

**4.**

```python
for row in range(5):
    for col in range(5):
        print("*", end="")
    print()
```

`end=""` stops `print()` from moving to a new line after every star.$$
WHERE slug = 'lesson-3-loops-en';

UPDATE lessons SET
exercises_markdown = $$1. Make a list of five city or district names. Print the second one and the last one.

2. Add a name to the end of your list, remove one by name, then print the whole list and how many items it holds.

3. Print every name in your list with its position, counting from 1 instead of 0.

4. Start from `numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]` and print the middle four items, then print every third item.$$
,
exercise_solutions = $$**1.**

```python
cities = ["Vientiane", "Luang Prabang", "Pakse", "Thakhek", "Savannakhet"]

print(cities[1])   # Luang Prabang
print(cities[-1])  # Savannakhet
```

**2.**

```python
cities = ["Vientiane", "Luang Prabang", "Pakse", "Thakhek", "Savannakhet"]

cities.append("Xam Neua")
cities.remove("Pakse")

print(cities)
print(len(cities))  # 5
```

**3.**

```python
cities = ["Vientiane", "Luang Prabang", "Pakse", "Thakhek", "Savannakhet"]

for i, city in enumerate(cities, 1):
    print(f"{i}. {city}")
```

**4.**

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

print(numbers[3:7])   # [4, 5, 6, 7]
print(numbers[::3])   # [1, 4, 7, 10]
```$$
WHERE slug = 'lesson-4-lists-en';

UPDATE lessons SET
exercises_markdown = $$1. Write a function `rectangle_area(width, height)` that returns the area. Call it three times with different numbers and print each result.

2. Write a function `is_even(n)` that returns `True` or `False`. Use it inside a loop to print the even numbers from 1 to 20.

3. Write `greet(name, language="Lao")` that prints a greeting. Call it once with only a name and once with both arguments.

4. Write a function that takes a list of numbers and returns the largest one, without using `max()`.$$
,
exercise_solutions = $$**1.**

```python
def rectangle_area(width, height):
    return width * height

print(rectangle_area(5, 3))
print(rectangle_area(2, 2))
print(rectangle_area(10, 4))
```

**2.**

```python
def is_even(n):
    return n % 2 == 0

for i in range(1, 21):
    if is_even(i):
        print(i, end=" ")
```

**3.**

```python
def greet(name, language="Lao"):
    if language == "Lao":
        print(f"Sabaidee, {name}!")
    else:
        print(f"Hello, {name}!")

greet("Somchit")
greet("Somchit", "English")
```

**4.**

```python
def biggest(numbers):
    best = numbers[0]
    for n in numbers:
        if n > best:
            best = n
    return best

print(biggest([3, 9, 1, 7, 5]))  # 9
```$$
WHERE slug = 'lesson-5-functions-en';
