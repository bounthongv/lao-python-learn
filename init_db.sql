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
    "order" INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

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
3. **ສໍາຄັນ:** ລືມທີ່ກົດທີ່ກຸ່ມ `Add Python to PATH`
4. ກົດ Install

### ການຂຽນໂຄດຕໍ່ໆ

```python
# ພິມຂໍ້ຄວາມ
print("ສະບາຍດີ! ລົດ Python")

# ຕົວແປງ (Variables)
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
# and - ຕ້ອງເງື່ອນໄຂທັງສອງ
if age >= 18 and has_id:
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
    $$3. ລູກສອນ (Loops)$$,
    $$lesson-3-loops$$,
    $$## ລູກສອນ (for / while)

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

# continue - ຂໍ້ລົບລູກສອນດຽວກັບ
for i in range(5):
    if i == 2:
        continue
    print(i)  # 0, 1, 3, 4
```

### ລູກສອນພາຍໃນ (Nested loops)

```python
# ການຄູ່ສູງ
for i in range(1, 4):
    for j in range(1, 4):
        print(f"{i} x {j} = {i*j}")
    print("---")
```$$,
    $$# ລູກສອນຕົວຢ່າງ
for i in range(1, 6):
    print(f"ລູກສອນຄັ້ງທີ {i}")

# while ຕົວຢ່າງ
count = 10
while count > 0:
    print(count)
    count -= 1
print("ສັນສຽງ!")$$,
    3
),
(
    $$4. ລິສັດ (Lists)$$,
    $$lesson-4-lists$$,
    $$## ລິສັດ (Lists)

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
fruits[0] = "ໝາກເຜັດ"  # ແກ້ໄຂ
fruits.append("ໝາກພາຍ")  # ເພີ່ມຕົວເສດ
fruits.insert(1, "ໝາກອິນ")  # ເພີ່ມທີ່ຕຳແໜ່ງ
```

### ລົບຂໍ້ມູນ

```python
fruits.remove("ໝາກກໍ")  # ລົບຕາມຄ່າ
popped = fruits.pop()   # ລົບຕົວສຸດທ້າຍ ແລະ ສົ່ງຄືນ
```

### ການຕັດລິສັດ (Slicing)

```python
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

print(numbers[2:5])   # [2, 3, 4]
print(numbers[:3])    # [0, 1, 2]
print(numbers[-3:])   # [7, 8, 9]
print(numbers[::2])   # [0, 2, 4, 6, 8] (ກັບ 2)
```

### List Methods ທີ່ສໍາຄັນ

```python
len(fruits)        # ຈຳນວນຕົວ
fruits.sort()      # ຈັດລັບ
fruits.reverse()   # ກັບລົບ
fruits.count(x)    # ນັບຈຳນວນ x
fruits.index(x)    # ຫາຕຳແໜ່ງ x
```$$,
    $$# ລິສັດຕົວຢ່າງ
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
