-- Database initialization for Lao Python Learning Platform
-- Loaded into Supabase Postgres by migrate_to_supabase.py.
--
-- IMPORTANT: lesson text is dollar-quoted ($$...$$) and must contain REAL newlines.
-- A '\n' inside a plain '...' string is stored by Postgres as a literal backslash-n,
-- which collapses each lesson into one line and stops markdown rendering.

CREATE TABLE IF NOT EXISTS lessons (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    content_markdown TEXT NOT NULL,
    example_code TEXT,
    exercises_markdown TEXT,
    exercise_solutions TEXT,
    "order" INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Exercises were added after the first deploy, so the table above may already
-- exist without them.
ALTER TABLE lessons ADD COLUMN IF NOT EXISTS exercises_markdown TEXT;
ALTER TABLE lessons ADD COLUMN IF NOT EXISTS exercise_solutions TEXT;

-- Insert 5 lessons in Lao
INSERT INTO lessons (title, slug, content_markdown, example_code, "order") VALUES
(
    $$1. ພື້ນຖານ Python$$,
    $$lesson-1-basics$$,
    $$## ພື້ນຖານ Python

Python ແມ່ນພາສາການປະຕິບັດຄຸນສຸດ ງ່າຍໃດ້ເພີ່ມຄວາມອ່ານໄດ້ ແລະ ຮຽນຮ້ອງຂໍ

### ການຕິດຕັ້ງ Python

1. ໄປໃນ https://python.org/downloads
2. ດາວໂຫຼດລະຫັດຕິດຕັ້ງ (installer)
3. **ສຳຄັນ:** ລືມທີ່ກົດທີ່ກຸ່ມ `Add Python to PATH`
4. ກົດ Install

### ການຂຽນໂຄດ

```python
# ພິມຂໍ້ຄວາມ
print("ສະບາຍດີ! ລົດ Python")

# ຕົວແປ (Variables)
name = "ສົມຈິດ"
age = 15
height = 1.65

# ປະກາດຂໍ້ມູນ
print(name)        # str
print(age)         # int
print(height)      # float
```

### ການຮັບຂໍ້ມູນຈາກຜູ້ໃຊ້

```python
name = input("ຊື່ອາຍຸ່ນໃດ? ")
print(f"ສະບາຍດີ {name}!")
```$$,
    $$# ຕົວຢ່າງພື້ນຖານ
print("ສະບາຍດີ! ລົດ Python")

name = "ນັກຮຽນ"
age = 16
print(f"ຊື່: {name}, ອາຍຸ: {age}")$$,
    1
),
(
    $$2. ເງື່ອນໄຂ (Conditions)$$,
    $$lesson-2-conditions$$,
    $$## ເງື່ອນໄຂ (if / elif / else)

ໃຊ້ເພື່ອເລືອກລາຍການຕາມເງື່ອນໄຂ

### if ໂດຍດຽວກັບ

```python
score = 85

if score >= 50:
    print("ຜ່ານ")
else:
    print("ບໍ່ຜ່ານ")
```

### if - elif - else

```python
score = int(input("ຄະແນນ: "))

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

print(f"ແຜ່ນ: {grade}")
```

### ເງື່ອນໄຂພາຍໃນ (Nested)

```python
age = 20
has_id = True

if age >= 18:
    if has_id:
        print("ເຂົ້າໄດ້")
    else:
        print("ຕ້ອງມີບັນທຶກ")
else:
    print("ອາຍຸບໍ່ພຽງ")
```

### ປະຈຳລະອຸດເງື່ອນໄຂ (Logical Operators)

```python
age = 20
is_student = True
is_teacher = False
is_banned = False

# and - ຕ້ອງເງື່ອນໄຂທັງສອງ
if age >= 18 and is_student:
    print("OK")

# or - ສາມາດເງື່ອນໄຂຂອງອື່ນອື່ນ
if is_student or is_teacher:
    print("ລຸດລາຄາ")

# not - ປະຕິບັດເງື່ອນໄຂ
if not is_banned:
    print("ເຂົ້າໄດ້")
```$$,
    $$# ເງື່ອນໄຂຕົວຢ່າງ
score = 75

if score >= 80:
    print("ການສຳເລັດ")
elif score >= 50:
    print("ຜ່ານ")
else:
    print("ບໍ່ຜ່ານ")

# ຕົວຢ່າງເງື່ອນໄຂພາຍໃນ
age = 20
if age >= 18:
    print("ເປັນຜູ້ສຸດ")
    if age >= 60:
        print("ຜູ້ສຸດອາຍຸສູງ")$$,
    2
),
(
    $$3. ລຸປ (Loops)$$,
    $$lesson-3-loops$$,
    $$## ລຸປ (for / while)

ໃຊ້ເພື່ອຕອບການສິ້ນສຸດສາມາດ

### for loop

```python
# ວົງລະບຸຈຳນວນ
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

# ການກໍານົດລາຍການ
fruits = ["ໝາກມັງ", "ໝາກກໍ", "ໝາກທຸງ"]
for fruit in fruits:
    print(f"ຂ້ອຍມັກກິນ {fruit}")
```

### range() ລາຍລະອຽດ

```python
range(5)        # 0, 1, 2, 3, 4
range(1, 6)     # 1, 2, 3, 4, 5
range(1, 10, 2) # 1, 3, 5, 7, 9 (ກັບ 2)
range(10, 0, -1) # 10, 9, ..., 1 (ກັບໝົດ)
```

### while loop

```python
count = 1
while count <= 5:
    print(count)
    count += 1  # ບໍ່ຕ້ອງການ count = count + 1
```

### break / continue

```python
# break - ອອກຈາກ loop
for i in range(10):
    if i == 5:
        break
    print(i)  # 0-4

# continue - ຂໍ້ລົບລຸປດຽວກັບ
for i in range(5):
    if i == 2:
        continue
    print(i)  # 0, 1, 3, 4
```

### ລຸປພາຍໃນ (Nested loops)

```python
# ການຄູ່ສູງ
for i in range(1, 4):
    for j in range(1, 4):
        print(f"{i} x {j} = {i*j}")
    print("---")
```$$,
    $$# ລຸປຕົວຢ່າງ
for i in range(1, 6):
    print(f"ລຸປຄັ້ງທີ {i}")

# while ຕົວຢ່າງ
count = 10
while count > 0:
    print(count)
    count -= 1
print("ສັນສຽງ!")$$,
    3
),
(
    $$4. ລິສ (Lists)$$,
    $$lesson-4-lists$$,
    $$## ລິສ (Lists)

ຈຳນວນຂໍ້ມູນຫຼາຍຂໍ້ມູນໃນທາງເທົ່ານັ້ນ

### ການສ້າງ List

```python
# ວັນທີ່
empty = []
numbers = [1, 2, 3, 4, 5]
names = ["ສົມຈິດ", "ສຸກສັນ", "ດາວ"]
mixed = [1, "ສະບາຍ", 3.14, True]
```

### ເຂົ້າເຖິງຂໍ້ມູນ (Indexing)

```python
fruits = ["ໝາກມັງ", "ໝາກກໍ", "ໝາກທຸງ"]

print(fruits[0])   # ໝາກມັງ (ເລກ 0)
print(fruits[1])   # ໝາກກໍ
print(fruits[-1])  # ໝາກທຸງ (ສຸດທ້າຍ)
```

### ແກ້ໄຂ ແລະ ເພີ່ມຂໍ້ມູນ

```python
fruits = ["ໝາກມັງ", "ໝາກກໍ", "ໝາກທຸງ"]

fruits[0] = "ໝາກເຜັດ"  # ແກ້ໄຂ
fruits.append("ໝາກພາຍ")  # ເພີ່ມຕົວເສດ
fruits.insert(1, "ໝາກອິນ")  # ເພີ່ມທີ່ຕຳແໜ່ງ
```

### ລົບຂໍ້ມູນ

```python
fruits = ["ໝາກມັງ", "ໝາກກໍ", "ໝາກທຸງ"]

fruits.remove("ໝາກກໍ")  # ລົບຕາມຄ່າ
popped = fruits.pop()   # ລົບຕົວສຸດທ້າຍ ແລະ ສົ່ງຄືນ
```

### ການຕັດລິສ (Slicing)

```python
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

print(numbers[2:5])   # [2, 3, 4]
print(numbers[:3])    # [0, 1, 2]
print(numbers[-3:])   # [7, 8, 9]
print(numbers[::2])   # [0, 2, 4, 6, 8] (ກັບ 2)
```

### List Methods ທີ່ສຳຄັນ

```python
fruits = ["ໝາກມັງ", "ໝາກກໍ", "ໝາກທຸງ", "ໝາກມັງ"]

print(len(fruits))                # 4   ຈຳນວນຕົວ
print(fruits.count("ໝາກມັງ"))          # 2   ນັບຈຳນວນ
print(fruits.index("ໝາກກໍ"))          # 1   ຕຳແໜ່ງ

fruits.sort()
print(fruits)

fruits.reverse()
print(fruits)
```$$,
    $$# ລິສຕົວຢ່າງ
students = ["ສົມຈິດ", "ສຸກສັນ", "ດາວ"]

# ເພີ່ມນັກຮຽນໃໝ່
students.append("ນິດ")

# ສະແດງທັງໝົດ
for i, name in enumerate(students, 1):
    print(f"{i}. {name}")

# ຈຳນວນ
print(f"ລວມ: {len(students)} ຄົນ")$$,
    4
),
(
    $$5. ຟັງຊັນ (Functions)$$,
    $$lesson-5-functions$$,
    $$## ຟັງຊັນ (Functions)

ກຸ້ງໂຄດທີ່ນຳໃຊ້ສາມາດ ແລະ ຈັດການງານໄດ້ເຂົ້າໄປ

### ການສ້າງຟັງຊັນ

```python
# ບໍ່ມີປະມານ
def greet():
    print("ສະບາຍດີ!")

greet()  # ເອົາໃຊ້

# ມີປະມານ
def greet_name(name):
    print(f"ສະບາຍດີ {name}!")

greet_name("ສົມຈິດ")

# ມີຄ່າສົ່ງຄືນ (return)
def add(a, b):
    return a + b

result = add(5, 3)
print(result)  # 8
```

### ປະມານມີຄ່າເລີຍງານ (Default Parameters)

```python
def greet(name, greeting="ສະບາຍດີ"):
    print(f"{greeting} {name}!")

greet("ສົມຈິດ")           # ສະບາຍດີ ສົມຈິດ!
greet("ສຸກສັນ", "ສະບາຍດີຕອນເຊົ້າ")  # ສະບາຍດີຕອນເຊົ້າ ສຸກສັນ!
```

### ຟັງຊັນສົ່ງຄືນຫຼາຍຄ່າ (Multiple Return)

```python
def calculate(a, b):
    return a + b, a - b, a * b, a / b

sum_, diff, prod, quot = calculate(10, 2)
print(sum_, diff, prod, quot)
```

### Variable Scope

```python
global_var = "ກົດ"  # global

def my_func():
    local_var = "ພິເສດ"  # local
    print(global_var)  # ເຂົ້າໄດ້
    print(local_var)   # ເຂົາໄດ້

my_func()
print(global_var)  # ເຂົ້າໄດ້
# print(local_var)  # ❌ Error!
```

### Lambda Functions (ອຸ່ນຍາກ)

```python
# ຟັງຊັນອຸ່ນຍາກ
square = lambda x: x * x
print(square(5))  # 25

# ກັບ map/filter
numbers = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x*x, numbers))
evens = list(filter(lambda x: x%2==0, numbers))
```$$,
    $$# ຟັງຊັນຕົວຢ່າງ
def greet(name):
    return f"ສະບາຍດີ {name}!"

print(greet("ນັກຮຽນ"))

# ຟັງຊັນຄິດຄວາມກວດ
def rectangle_area(width, height):
    return width * height

print(f"ພະນາທີ: {rectangle_area(5, 3)}")$$,
    5
)
ON CONFLICT (slug) DO UPDATE SET
    title = EXCLUDED.title,
    content_markdown = EXCLUDED.content_markdown,
    example_code = EXCLUDED.example_code,
    "order" = EXCLUDED."order";

-- Lessons 6-8: ວັດຈະນານຸກົມ, ຄຳເວົ້າ ແລະ ໄຟລ໌. ໜ້າເຫຼົ່ານີ້ແປງຄຽງຄູ່
-- ກັບ init_db_en.sql ແຕ່ລະຫົວຂໍ້, ແລະ ມີບົດຝຶກຫັດ + ຄຳຕອບຢູ່ໃນ INSERT ດຽວກັນ.
-- ບໍ່ສະແດງຖັນ lang ເພາະ init_db.sql ເຮັດວຽກກ່ອນ migrate_multilingual.sql.

INSERT INTO lessons (title, slug, content_markdown, example_code, "order",
                     exercises_markdown, exercise_solutions) VALUES
(
    $$6. ວັດຈະນານຸກົມ (Dictionaries)$$,
    $$lesson-6-dictionaries$$,
    $$## ວັດຈະນານຸກົມ (Dictionaries)

ລິສເກັບຂໍ້ມູນຕາມລຳດັບ, ເຮົາເອີ້ນໃຊ້ມັນຕາມຕຳແໜ່ງ. ວັດຈະນານຸກົມເກັບເປັນຄູ່:
ກະແຈ (key) ຄູ່ກັບຄ່າ (value), ເອີ້ນໃຊ້ຕາມຊື່.

### ການສ້າງວັດຈະນານຸກົມ

```python
student = {"ຊື່": "ສົມຈິດ", "ອາຍຸ": 17, "ໂຮງຮຽນ": "ລາວ-ອັງກິດ"}

empty = {}                            # ວັດຈະນານຸກົມຫວ່າງ
marks = {"ຄະນິດ": 78, "ລາວ": 91, "ອັງກິດ": 65}
```

ກະແຈມັກເປັນຄຳເວົ້າ. ສ່ວນຄ່າຈະເປັນແບບໃດກໍໄດ້: ຕົວເລກ, ຄຳເວົ້າ, ລິສ
ຫຼື ວັດຈະນານຸກົມອີກຕົວໜຶ່ງ.

### ອ່ານຄ່າ (Reading Values)

```python
student = {"ຊື່": "ສົມຈິດ", "ອາຍຸ": 17}

print(student["ຊື່"])                 # ສົມຈິດ
print(student.get("ອາຍຸ"))            # 17
print(student.get("ຊັ້ນ"))             # None  (ບໍ່ມີ, ແຕ່ບໍ່ຜິດພາດ)
print(student.get("ຊັ້ນ", "ຍັງບໍ່ມີ"))  # ຍັງບໍ່ມີ  (ເຮົາກຳນົດຄ່ານີ້ເອງ)
```

ຖ້າໃສ່ [ ] ກັບກະແຈທີ່ບໍ່ມີ, Python ຈະໃຫ້ KeyError. ແຕ່ .get() ຈະສົ່ງຄືນ None
ຫຼື ຄ່າເລີ່ມຕົ້ນທີ່ເຮົາໃສ່ໄປເປັນປະມານອັນທີສອງ.

### ແກ້ໄຂ ແລະ ເພີ່ມຄ່າ

```python
student = {"ຊື່": "ສົມຈິດ", "ອາຍຸ": 17}

student["ອາຍຸ"] = 18                  # ກະແຈມີຢູ່ແລ້ວ, ຄ່າຈະປ່ຽນ
student["ເມືອງ"] = "ວຽງຈັນ"           # ກະແຈໃໝ່, ຈະເພີ່ມເຂົ້າໄປ

print(student)
```

### ລົບຂໍ້ມູນ

```python
student = {"ຊື່": "ສົມຈິດ", "ອາຍຸ": 17, "ເມືອງ": "ວຽງຈັນ"}

del student["ເມືອງ"]                  # ລົບຄູ່ນັ້ນໄປ
age = student.pop("ອາຍຸ")             # ລົບ ແລະ ສົ່ງຄ່າຄືນມາ

print(student)
print(age)
```

### ໝູນຜ່ານວັດຈະນານຸກົມ (Looping)

```python
student = {"ຊື່": "ສົມຈິດ", "ອາຍຸ": 17, "ເມືອງ": "ວຽງຈັນ"}

for key in student:                   # ໝູນແລ້ວໄດ້ກະແຈ
    print(key, "->", student[key])

for key, value in student.items():    # items() ໄດ້ທັງກະແຈ ແລະ ຄ່າ
    print(f"{key}: {value}")
```

### ກວດສອບກະແຈ

```python
student = {"ຊື່": "ສົມຈິດ", "ອາຍຸ": 17}

if "ຊັ້ນ" in student:
    print(student["ຊັ້ນ"])
else:
    print("ຍັງບໍ່ທັນບັນທຶກຊັ້ນ")
```

`in` ກັບວັດຈະນານຸກົມຈະເບິ່ງແຕ່ ກະແຈ, ບໍ່ໄດ້ເບິ່ງຄ່າ.$$
,
    $$# ຄະແນນ ແລະ ຄ່າສະເລ່ຍ
marks = {"ຄະນິດ": 78, "ລາວ": 91, "ອັງກິດ": 65}

for subject, mark in marks.items():
    print(f"{subject}: {mark}")

total = 0
for mark in marks.values():
    total = total + mark

print(f"ສະເລ່ຍ: {total / len(marks):.1f}")$$
,
    6,
    $$1. ສ້າງວັດຈະນານຸກົມກ່ຽວກັບຕົວເຈົ້າເອງຢ່າງໜ້ອຍ 3 ຄູ່ (ຊື່, ອາຍຸ, ອາຫານທີ່ມັກ)
ແລ້ວພິມທຸກຄູ່ດ້ວຍ `for` ໝູນຜ່ານ `.items()`.

2. ບັນທຶກຄະແນນ 4 ວິຊາລົງໃນວັດຈະນານຸກົມ, ແລ້ວພິມວິຊາທີ່ໄດ້ຄະແນນສູງສຸດພ້ອມຄະແນນ.

3. ນັບວ່າແຕ່ລະຄຳເກີດຂຶ້ນຈັກຄັ້ງໃນລິສນີ້:
`["ໝາກມັງ", "ໝາກກໍ", "ໝາກມັງ", "ໝາກແອັບ", "ໝາກກໍ", "ໝາກມັງ"]`.
ສ່ວນທີ່ຍາກທີ່ສຸດແມ່ນ `counts[word] = counts.get(word, 0) + 1`.

4. ຖາມຊື່ວິຊາດ້ວຍ `input()` ແລ້ວພິມຄະແນນຂອງວິຊານັ້ນ. ຖ້າບໍ່ມີວິຊານັ້ນ, ພິມຂໍ້ຄວາມ
ແທນ ຢ່າໃຫ້ໂປຣແກຣມຜິດພາດ. ພິມຊື່ວິຊາລົງໃນຊ່ອງ **Input** ກ່ອນກົດ Run.$$
,
    $$**1.**

```python
me = {"ຊື່": "ສົມຈິດ", "ອາຍຸ": 17, "ອາຫານ": "ເຂົ້າໜົມຈີນ"}

for key, value in me.items():
    print(f"{key}: {value}")
```

**2.**

```python
marks = {"ຄະນິດ": 78, "ລາວ": 91, "ອັງກິດ": 65, "ປະຫວັດ": 84}

best_subject = ""
best_mark = -1

for subject, mark in marks.items():
    if mark > best_mark:
        best_mark = mark
        best_subject = subject

print(f"ສູງສຸດ: {best_subject} {best_mark}")
```

**3.**

```python
words = ["ໝາກມັງ", "ໝາກກໍ", "ໝາກມັງ", "ໝາກແອັບ", "ໝາກກໍ", "ໝາກມັງ"]

counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1

for word, count in counts.items():
    print(f"{word}: {count}")
```

**4.**

```python
marks = {"ຄະນິດ": 78, "ລາວ": 91, "ອັງກິດ": 65}

subject = input("ຊື່ວິຊາ: ")

if subject in marks:
    print(f"{subject}: {marks[subject]}")
else:
    print(f"ຂ້ອຍບໍ່ມີຄະແນນຂອງ {subject}")
```

ພິມ `ລາວ` ໃນຊ່ອງ Input, ແລ້ວລອງວິຊາທີ່ບໍ່ມີຢູ່.$$
),
(
    $$7. ຄຳເວົ້າ (Strings)$$,
    $$lesson-7-strings$$,
    $$## ຄຳເວົ້າ (Strings)

ຄຳເວົ້າແມ່ນລຳດັບຂອງຕົວອັກສອນ, ດັ່ງນັ້ນສິ່ງທີ່ຮຽນມາກ່ຽວກັບລິສໃຊ້ໄດ້ກັບຄຳເວົ້າ
ດ້ວຍ: ຕຳແໜ່ງ, ການຕັດ ແລະ ການໝູນ.

### Quotation Marks ແລະ Escape

```python
s1 = 'ເຂົາເວົ້າວ່າ "ສະບາຍດີ"'
s2 = "ມັນເວົ້າວ່າ 'ໄດ້'"
path = "C:\\Users\\somchit"

print(s1)
print(s2)
print(path)
```

ເສັ້ນຕັດໜຶ່ງ `\\` ໝາຍຄວາມວ່າຕົວໜັງສືຖັດມາເປັນສ່ວນຂອງລະຫັດ, ບໍ່ແມ່ນຂໍ້ຄວາມ: `\\` ໃຫ້
ເສັ້ນຕັດໜຶ່ງແທ້, `\n` ໃຫ້ແຖວໃໝ່ ແລະ `\t` ໃຫ້ tab.

### ຄວາມຍາວ, ຕຳແໜ່ງ ແລະ ຕົວໃຫຍ່/ຕົວນ້ອຍ

```python
name = "somchit"

print(len(name))          # 7      ຈຳນວນຕົວອັກສອນ
print(name[0])            # s      ຕົວທຳອິດ
print(name[-1])           # t      ຕົວສຸດທ້າຍ
print(name.upper())       # SOMCHIT
print(name.title())       # Somchit
```

ຄຳເວົ້າບໍ່ປ່ຽນແປງໃນບ່ອນເກົ່າ. `name.upper()` ສົ່ງຄືນຄຳເວົ້າ **ໃໝ່**,
ສ່ວນ `name` ຍັງຄືເກົ່າ.

### ທຳຄວາມສະອາດຂໍ້ຄວາມ

```python
messy = "   somchit   "

print(messy.strip())      # ທັງສອງຂ້າງ
print(messy.lstrip())     # ຂ້າງຊ້າຍ
print(messy.rstrip())     # ຂ້າງຂວາ
print(len(messy), len(messy.strip()))
```

ໃຊ້ `.strip()` ກັບທຸກຢ່າງທີ່ອ່ານມາຈາກໄຟລ໌ ຫຼື ຈາກ `input()`.

### ຊອກຫາ ແລະ ແທນທີ່

```python
sentence = "Learn Python in Lao"

print(sentence.find("Python"))        # 6       ຕຳແໜ່ງ, ຖ້າບໍ່ມີໄດ້ -1
print(sentence.count("a"))            # 2       ນັບຈຳນວນຄັ້ງ
print(sentence.replace("Python", "Java"))
print(sentence.startswith("Learn"))   # True
print(sentence.endswith("Lao"))       # True
print("Python" in sentence)           # True
```

### ການຕັດຄຳເວົ້າ (Slicing)

```python
word = "Vientiane"

print(word[0:4])          # Vien
print(word[:4])           # Vien
print(word[-4:])          # iane
print(word[::-1])         # enaitneiV  (ອ່ານຍ້ອນຫຼັງ)
```

ຕົວຢ່າງນີ້ໃຊ້ຄຳພາສາອັງກິດ, ເພາະຕົວສະຫຼະລາວເປັນມາຕຣາທີ່ຢູ່ເທິງ/ເຊິ່ງຕົວອັກສອນ.
ການຕັດຕາມຕຳແໜ່ງອາດແຍກມັນອອກຈາກຕົວພະຍັນຊະນະໄດ້.

### ແຍກ ແລະ ຊື່ອມ (Split and Join)

```python
line = "somchit,17,Math"
parts = line.split(",")

print(parts)              # ['somchit', '17', 'Math']
print(parts[1])           # 17

names = ["Somchit", "Suksan", "Dao"]
print(", ".join(names))   # Somchit, Suksan, Dao
```

`split` ແປງຄຳເວົ້າເປັນລິສ, `join` ປ່ຽນລິສເປັນຄຳເວົ້າ.

### ຕົວເລກໃນ f-String

```python
mark = 78.567

print(f"ຄະແນນ: {mark:.2f}")     # 2 ຕຳແໜ່ງທົດສະນິຍົມ
print(f"|{mark:>8.2f}|")        # ເຕີມຊ່ອງຫວ່າງໃຫ້ຄົບ 8 ຕົວ, ຈັດຝັ່ງຂວາ
print(f"{1234567:,}")           # 1,234,567$$
,
    $$# ຈັດຊື່ທີ່ບໍ່ສະອາດໃຫ້ຖືກຕ້ອງ
full_name = "  somchit phommachan  "

name = full_name.strip()
first, last = name.split()

print(f"ຊື່: {first.title()} {last.title()}")
print(f"ຕົວຫຍໍ້: {first[0].upper()}{last[0].upper()}")
print(f"ຈຳນວນຕົວອັກສອນ: {len(first) + len(last)}")$$
,
    7,
    $$1. ຖາມຊື່ ແລະ ນາມສະກຸນດ້ວຍ `input()`, ແລ້ວພິມມັນເປັນຕົວໃຫຍ່ຕົວນ້ອຍປະສົມ (title),
ຕົວໃຫຍ່ທັງໝົດ, ບອກຈຳນວນຕົວອັກສອນ ແລະ ຈຳນວນຄຳ. ພິມ `somchit phommachan` ໃນຊ່ອງ **Input**.

2. ຖາມຄຳສັບໜຶ່ງຄຳ ແລ້ວນັບສະຫຼະ (`a e i o u`). ຈື່ໄວ້ວ່າ `in` ໃຊ້ໄດ້ກັບຄຳເວົ້າ:
`if letter in "aeiou":`.

3. ປ່ຽນວັນທີ `2026-11-06` ໃຫ້ເປັນ `06/11/2026` ດ້ວຍ `.split()` ແລະ `.join()`.

4. ຖາມຄຳສັບໜຶ່ງຄຳ ແລ້ວພິມວ່າມັນອ່ານຍ້ອນຫຼັງແລ້ວຄືເກົ່າຫຼືບໍ່ (palindrome) ດ້ວຍ
ການຕັດຄຳເວົ້າ. ລອງ `madam` ແລະ `python` ໃນຊ່ອງ **Input**.$$
,
    $$**1.**

```python
full = input("ຊື່ຂອງເຈົ້າ: ").strip()
words = full.split()

print(full.title())
print(full.upper())
print(f"ຈຳນວນຕົວອັກສອນ: {len(full)}")
print(f"ຈຳນວນຄຳ: {len(words)}")
```

**2.**

```python
word = input("ຄຳສັບ: ").lower()
vowels = 0

for letter in word:
    if letter in "aeiou":
        vowels = vowels + 1

print(f"{word} ມີສະຫຼະ {vowels} ຕົວ")
```

**3.**

```python
date = "2026-11-06"
year, month, day = date.split("-")

print("/".join([day, month, year]))
```

**4.**

```python
word = input("ຄຳສັບ: ").lower()

if word == word[::-1]:
    print(f"{word} ອ່ານຍ້ອນຫຼັງຄືເກົ່າ")
else:
    print(f"{word} ອ່ານຍ້ອນຫຼັງບໍ່ຄືເກົ່າ")
```
$$
),
(
    $$8. ໄຟລ໌ (Files)$$,
    $$lesson-8-files$$,
    $$## ໄຟລ໌ (Files)

ໂປຣແກຣມລືມທຸກຢ່າງເມື່ອມັນຢຸດ. ໄຟລ໌ເກັບຂໍ້ມູນໄວ້ໃຫ້ເຮົາໃຊ້ໃນຄັ້ງຕໍ່ໄປ.

ໃນ ຫ້ອງທົດລອງ (Playground), ໄຟລ໌ທີ່ຂຽນຈະຢູ່ໃນເຄື່ອງເຊີບເວີ, ບໍ່ແມ່ນໃນ
ຄອມພິວເຕີຂອງເຈົ້າ ແລະ ມັນອາດຫາຍໄປ. ດັ່ງນັ້ນທຸກຕົວຢ່າງຂ້າງລຸ່ມນີ້ສ້າງໄຟລ໌ຂອງ
ຕົວມັນເອງກ່ອນ, ເພື່ອມັນຈະໃຊ້ໄດ້ສະເໝີ.

### ໂໝດ (Modes)

| ໂໝດ | `open()` ເຮັດຫຍັງ |
| --- | --- |
| `"r"` | ອ່ານ (ເປັນຄ່າເລີ່ມຕົ້ນ); ຜິດພາດຖ້າໄຟລ໌ບໍ່ມີ |
| `"w"` | ຂຽນ; ສ້າງໄຟລ໌ ແລະ **ລຶບ** ຂໍ້ມູນເກົ່າທັງໝົດ |
| `"a"` | ເພີ່ມທ້າຍ; ເກັບຂໍ້ມູນເກົ່າໄວ້ |
| `"x"` | ສ້າງໃໝ່; ຜິດພາດຖ້າໄຟລ໌ມີຢູ່ແລ້ວ |

### ຂຽນໄຟລ໌

```python
with open("names.txt", "w") as f:
    f.write("Somchit\n")
    f.write("Suksan\n")
    f.write("Dao\n")
```

`f.write()` ບໍ່ **ເພີ່ມ** ແຖວໃໝ່ໃຫ້, ເຮົາຕ້ອງຂຽນ `\n` ເອງ. `with` ຈະປິດໄຟລ໌ໃຫ້
ອັດຕະໂນມັດ, ເຖິງມີຂໍ້ຜິດພາດເກີດຂຶ້ນກໍຕາມ.

### ອ່ານໄຟລ໌ທັງໝົດ

```python
with open("names.txt", "w") as f:      # ສ້າງໄຟລ໌ກ່ອນ
    f.write("Somchit\nSuksan\nDao\n")

with open("names.txt", "r") as f:
    content = f.read()

print(content)
```

### ອ່ານເທື່ອລະແຖວ

```python
with open("names.txt", "w") as f:
    f.write("Somchit\nSuksan\nDao\n")

with open("names.txt") as f:            # "r" ເປັນຄ່າເລີ່ມຕົ້ນ
    for line in f:
        print(line.strip())             # strip() ລຶບ \n ອອກ
```

### ແປງໄຟລ໌ເປັນຕົວເລກ

```python
with open("marks.txt", "w") as f:
    f.write("78\n91\n65\n")

with open("marks.txt") as f:
    lines = f.read().splitlines()       # ['78', '91', '65']

marks = []
for line in lines:
    marks.append(int(line))

print(marks)
print(sum(marks) / len(marks))
```

### ເມື່ອໄຟລ໌ບໍ່ມີ

```python
try:
    with open("nothing.txt") as f:
        print(f.read())
except FileNotFoundError:
    print("ຍັງບໍ່ມີໄຟລ໌ນີ້")
```

`"w"` ສ້າງໄຟລ໌ຂຶ້ນໃໝ່, ດັ່ງນັ້ນຈະບໍ່ພົບຂໍ້ຜິດພາດນີ້. ເຮົາຈະພົບມັນຕອນອ່ານ.$$
,
    $$# ບັນທຶກາຍເຫດ ແລ້ວສະແດງເປັນເລກລຳດັບ
with open("notes.txt", "w") as f:
    f.write("ຊື້ເຂົ້າ\n")
    f.write("ທົບທວນລຸປ\n")
    f.write("ໂທຫາດາວ\n")

with open("notes.txt") as f:
    notes = f.read().splitlines()

for i, note in enumerate(notes, 1):
    print(f"{i}. {note}")

print(f"ລວມ: {len(notes)} ເທື່ອ")$$
,
    8,
    $$1. ຂຽນຊື່ ແລະ ອາຍຸຂອງເຈົ້າລົງໃນ `me.txt` ສອງແຖວ, ແລ້ວເປີດໄຟລ໌ອ່ານຄືນ
ແລະພິມຂໍ້ມູນທັງໝົດ.

2. ຂຽນຕົວເລກ 5 ຕົວລົງໃນ `numbers.txt`, ໜຶ່ງຕົວຕໍ່ໜຶ່ງແຖວ. ອ່ານມັນຄືນ, ປ່ຽນເປັນ
ຕົວເລກ ແລະພິມຜົນບວກ ແລະ ຄ່າສະເລ່ຍ.

3. ສ້າງໄຟລ໌ທີ່ມີສອງແຖວ, ເປີດມັນອີກຄັ້ງດ້ວຍໂໝດ `"a"` ເພື່ອເພີ່ມແຖວທີສາມ, ແລ້ວພິມ
ທັງໝົດ. ຖ້າໃຊ້ໂໝດ `"w"` ຈະເກີດຫຍັງຂຶ້ນ?

4. ຖາມໝາຍເຫດໜຶ່ງບັນທຶກດ້ວຍ `input()` ແລ້ວເພີ່ມມັນເຂົ້າໄຟລ໌, ຫຼັງຈາກນັ້ນພິມ
ໝາຍເຫດທຸກອັນພ້ອມເລກລຳດັບ. ພິມໝາຍເຫດລົງໃນຊ່ອງ **Input** ກ່ອນກົດ Run.$$
,
    $$**1.**

```python
with open("me.txt", "w") as f:
    f.write("ສົມຈິດ\n")
    f.write("17\n")

with open("me.txt") as f:
    print(f.read())
```

**2.**

```python
with open("numbers.txt", "w") as f:
    for n in [10, 20, 30, 40, 50]:
        f.write(f"{n}\n")

with open("numbers.txt") as f:
    numbers = []
    for line in f:
        numbers.append(int(line.strip()))

total = sum(numbers)
print(f"ຜົນບວກ: {total}")
print(f"ຄ່າສະເລ່ຍ: {total / len(numbers)}")
```

**3.**

```python
with open("list.txt", "w") as f:
    f.write("rice\n")
    f.write("fish\n")

with open("list.txt", "a") as f:
    f.write("chilli\n")

with open("list.txt") as f:
    print(f.read())
```

ຖ້າໃຊ້ໂໝດ `"w"` ສອງແຖວທຳອິດຈະຖືກລຶບຫາຍໄປ.

**4.**

```python
note = input("ໝາຍເຫດຂອງເຈົ້າ: ")

with open("notes.txt", "w") as f:
    f.write("ຊື້ເຂົ້າ\n")

with open("notes.txt", "a") as f:
    f.write(note + "\n")

with open("notes.txt") as f:
    for i, line in enumerate(f, 1):
        print(f"{i}. {line.strip()}")
```
$$
)
ON CONFLICT (slug) DO UPDATE SET
    title = EXCLUDED.title,
    content_markdown = EXCLUDED.content_markdown,
    example_code = EXCLUDED.example_code,
    "order" = EXCLUDED."order",
    exercises_markdown = EXCLUDED.exercises_markdown,
    exercise_solutions = EXCLUDED.exercise_solutions;
