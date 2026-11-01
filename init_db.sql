-- Database initialization for Lao Python Learning Platform
-- Run this on Railway PostgreSQL after provisioning

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
    '1. ພື້ນຖານ Python',
    'lesson-1-basics',
    '## ພື້ນຖານ Python\n\nPython ແມ່ນພາສາການປະຕິບັດຄຸນສຸດ ງ່າຍໃດ້ເພີ່ມຄວາມອ່ານໄດ້ ແລະ ຮຽນຮ້ອງຂໍ\n\n### ການຕິດຕັ້ງ Python\n\n1. ໄປໃນ https://python.org/downloads\n2. ດາວໂຫຼດລະຫັດຕິດຕັ້ງ (installer)\n3. **ສໍາຄັນ:** ລືມທີ່ກົດທີ່ກຸ່ມ `Add Python to PATH`\n4. ກົດ Install\n\n### ການຂຽນໂຄດຕໍ່ໆ\n\n```python\n# ພິມຂໍ້ຄວາມ\nprint(\"ສະບາຍດີ! ລົດ Python\")\n\n# ຕົວແປງ (Variables)\nname = \"ສົມຈິດ\"\nage = 15\nheight = 1.65\n\n# ປະກາດຂໍ້ມູນ\nprint(name)        # str\nprint(age)         # int\nprint(height)      # float\n```\n\n### ການຮັບຂໍ້ມູນຈາກຜູ້ໃຊ້\n\n```python\nname = input(\"ຊື່ອາຍຸ່ນໃດ? \")\nprint(f\"ສະບາຍດີ {name}!\")\n```',
    '# ຕົວຢ່າງພື້ນຖານ\nprint(\"ສະບາຍດີ! ລົດ Python\")\n\nname = \"ນັກຮຽນ\"\nage = 16\nprint(f\"ຊື່: {name}, ອາຍຸ: {age}\")',
    1
),
(
    '2. ເງື່ອນໄຂ (Conditions)',
    'lesson-2-conditions',
    '## ເງື່ອນໄຂ (if / elif / else)\n\nໃຊ້ເພື່ອເລືອກລາຍການຕາມເງື່ອນໄຂ\n\n### if ໂດຍດຽວກັບ\n\n```python\nscore = 85\n\nif score >= 50:\n    print(\"ຜ່ານ\")\nelse:\n    print(\"ບໍ່ຜ່ານ\")\n```\n\n### if - elif - else\n\n```python\nscore = int(input(\"ຄະແນນ: \"))\n\nif score >= 80:\n    grade = \"A\"\nelif score >= 70:\n    grade = \"B\"\nelif score >= 60:\n    grade = \"C\"\nelif score >= 50:\n    grade = \"D\"\nelse:\n    grade = \"F\"\n\nprint(f\"ແຜ່ນ: {grade}\")\n```\n\n### ເງື່ອນໄຂພາຍໃນ (Nested)\n\n```python\nage = 20\nhas_id = True\n\nif age >= 18:\n    if has_id:\n        print(\"ເຂົ້າໄດ້\")\n    else:\n        print(\"ຕ້ອງມີບັນທຶກ\")\nelse:\n    print(\"ອາຍຸບໍ່ພຽງ\")\n```\n\n### ປະຈຳລະອຸດເງື່ອນໄຂ (Logical Operators)\n\n```python\n# and - ຕ້ອງເງື່ອນໄຂທັງສອງ\nif age >= 18 and has_id:\n    print(\"OK\")\n\n# or - ສາມາດເງື່ອນໄຂຂອງອື່ນອື່ນ\nif is_student or is_teacher:\n    print(\"ລຸດລາຄາ\")\n\n# not - ປະຕິບັດເງື່ອນໄຂ\nif not is_banned:\n    print(\"ເຂົ້າໄດ້\")\n```',
    '# ເງື່ອນໄຂຕົວຢ່າງ\nscore = 75\n\nif score >= 80:\n    print(\"ການສຳເລັດ\")\nelif score >= 50:\n    print(\"ຜ່ານ\")\nelse:\n    print(\"ບໍ່ຜ່ານ\")\n\n# ຕົວຢ່າງເງື່ອນໄຂພາຍໃນ\nage = 20\nif age >= 18:\n    print(\"ເປັນຜູ້ສຸດ\")\n    if age >= 60:\n        print(\"ຜູ້ສຸດອາຍຸສູງ\")',
    2
),
(
    '3. ລູກສອນ (Loops)',
    'lesson-3-loops',
    '## ລູກສອນ (for / while)\n\nໃຊ້ເພື່ອຕອບການສິ້ນສຸດສາມາດ\n\n### for loop\n\n```python\n# ວົງລະບຸຈຳນວນ\nfor i in range(5):\n    print(i)  # 0, 1, 2, 3, 4\n\n# ການກໍານົດລາຍການ\nfruits = [\"ໝາກມັງ\", \"ໝາກກໍ\", \"ໝາກທຸງ\"]\nfor fruit in fruits:\n    print(f\"ຂ້ອຍມັກກິນ {fruit}\")\n```\n\n### range() ລາຍລະອຽດ\n\n```python\nrange(5)        # 0, 1, 2, 3, 4\nrange(1, 6)     # 1, 2, 3, 4, 5\nrange(1, 10, 2) # 1, 3, 5, 7, 9 (ກັບ 2)\nrange(10, 0, -1) # 10, 9, ..., 1 (ກັບໝົດ)\n```\n\n### while loop\n\n```python\ncount = 1\nwhile count <= 5:\n    print(count)\n    count += 1  # ບໍ່ຕ້ອງການ count = count + 1\n```\n\n### break / continue\n\n```python\n# break - ອອກຈາກ loop\nfor i in range(10):\n    if i == 5:\n        break\n    print(i)  # 0-4\n\n# continue - ຂໍ້ລົບລູກສອນດຽວກັບ\nfor i in range(5):\n    if i == 2:\n        continue\n    print(i)  # 0, 1, 3, 4\n```\n\n### ລູກສອນພາຍໃນ (Nested loops)\n\n```python\n# ການຄູ່ສູງ\nfor i in range(1, 4):\n    for j in range(1, 4):\n        print(f\"{i} x {j} = {i*j}\")\n    print(\"---\")\n```',
    '# ລູກສອນຕົວຢ່າງ\nfor i in range(1, 6):\n    print(f\"ລູກສອນຄັ້ງທີ {i}\")\n\n# while ຕົວຢ່າງ\ncount = 10\nwhile count > 0:\n    print(count)\n    count -= 1\nprint(\"ສັນສຽງ!\")',
    3
),
(
    '4. ລິສັດ (Lists)',
    'lesson-4-lists',
    '## ລິສັດ (Lists)\n\nຈຳນວນຂໍ້ມູນຫຼາຍຂໍ້ມູນໃນທາງເທົ່ານັ້ນ\n\n### ການສ້າງ List\n\n```python\n# ວັນທີ່\nempty = []\nnumbers = [1, 2, 3, 4, 5]\nnames = [\"ສົມຈິດ\", \"ສຸກສັນ\", \"ດາວ\"]\nmixed = [1, \"ສະບາຍ\", 3.14, True]\n```\n\n### ເຂົ້າເຖິງຂໍ້ມູນ (Indexing)\n\n```python\nfruits = [\"ໝາກມັງ\", \"ໝາກກໍ\", \"ໝາກທຸງ\"]\n\nprint(fruits[0])   # ໝາກມັງ (ເລກ 0)\nprint(fruits[1])   # ໝາກກໍ\nprint(fruits[-1])  # ໝາກທຸງ (ສຸດທ້າຍ)\n```\n\n### ແກ້ໄຂ ແລະ ເພີ່ມຂໍ້ມູນ\n\n```python\nfruits[0] = \"ໝາກເຜັດ\"  # ແກ້ໄຂ\nfruits.append(\"ໝາກພາຍ\")  # ເພີ່ມຕົວເສດ\nfruits.insert(1, \"ໝາກອິນ\")  # ເພີ່ມທີ່ຕຳແໜ່ງ\n```\n\n### ລົບຂໍ້ມູນ\n\n```python\nfruits.remove(\"ໝາກກໍ\")  # ລົບຕາມຄ່າ\npopped = fruits.pop()   # ລົບຕົວສຸດທ້າຍ ແລະ ສົ່ງຄືນ\n```\n\n### ການຕັດລິສັດ (Slicing)\n\n```python\nnumbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]\n\nprint(numbers[2:5])   # [2, 3, 4]\nprint(numbers[:3])    # [0, 1, 2]\nprint(numbers[-3:])   # [7, 8, 9]\nprint(numbers[::2])   # [0, 2, 4, 6, 8] (ກັບ 2)\n```\n\n### List Methods ທີ່ສໍາຄັນ\n\n```python\nlen(fruits)        # ຈຳນວນຕົວ\nfruits.sort()      # ຈັດລັບ\nfruits.reverse()   # ກັບລົບ\nfruits.count(x)    # ນັບຈຳນວນ x\nfruits.index(x)    # ຫາຕຳແໜ່ງ x\n```',
    '# ລິສັດຕົວຢ່າງ\nstudents = [\"ສົມຈິດ\", \"ສຸກສັນ\", \"ດາວ\"]\n\n# ເພີ່ມນັກຮຽນໃໝ່\nstudents.append(\"ນິດ\")\n\n# ສະແດງທັງໝົດ\nfor i, name in enumerate(students, 1):\n    print(f\"{i}. {name}\")\n\n# ຈຳນວນ\nprint(f\"ລວມ: {len(students)} ຄົນ\")',
    4
),
(
    '5. ຟັງຊັນ (Functions)',
    'lesson-5-functions',
    '## ຟັງຊັນ (Functions)\n\nກຸ້ງໂຄດທີ່ນຳໃຊ້ສາມາດ ແລະ ຈັດການງານໄດ້ເຂົ້າໄປ\n\n### ການສ້າງຟັງຊັນ\n\n```python\n# ບໍ່ມີປະມານ\ndef greet():\n    print(\"ສະບາຍດີ!\")\n\ngreet()  # ເອົາໃຊ້\n\n# ມີປະມານ\ndef greet_name(name):\n    print(f\"ສະບາຍດີ {name}!\")\n\ngreet_name(\"ສົມຈິດ\")\n\n# ມີຄ່າສົ່ງຄືນ (return)\ndef add(a, b):\n    return a + b\n\nresult = add(5, 3)\nprint(result)  # 8\n```\n\n### ປະມານມີຄ່າເລີຍງານ (Default Parameters)\n\n```python\ndef greet(name, greeting=\"ສະບາຍດີ\"):\n    print(f\"{greeting} {name}!\")\n\ngreet(\"ສົມຈິດ\")           # ສະບາຍດີ ສົມຈິດ!\ngreet(\"ສຸກສັນ\", \"ສະບາຍດີຕອນເຊົ້າ\")  # ສະບາຍດີຕອນເຊົ້າ ສຸກສັນ!\n```\n\n### ຟັງຊັນສົ່ງຄືນຫຼາຍຄ່າ (Multiple Return)\n\n```python\ndef calculate(a, b):\n    return a + b, a - b, a * b, a / b\n\nsum_, diff, prod, quot = calculate(10, 2)\nprint(sum_, diff, prod, quot)\n```\n\n### Variable Scope\n\n```python\nglobal_var = \"ກົດ\"  # global\n\ndef my_func():\n    local_var = \"ພິເສດ\"  # local\n    print(global_var)  # ເຂົ້າໄດ້\n    print(local_var)   # ເຂົາໄດ້\n\nmy_func()\nprint(global_var)  # ເຂົ້າໄດ້\n# print(local_var)  # ❌ Error!\n```\n\n### Lambda Functions (ອຸ່ນຍາກ)\n\n```python\n# ຟັງຊັນອຸ່ນຍາກ\nsquare = lambda x: x * x\nprint(square(5))  # 25\n\n# ກັບ map/filter\nnumbers = [1, 2, 3, 4, 5]\nsquares = list(map(lambda x: x*x, numbers))\nevens = list(filter(lambda x: x%2==0, numbers))\n```',
    '# ຟັງຊັນຕົວຢ່າງ\ndef greet(name):\n    return f\"ສະບາຍດີ {name}!\"\n\nprint(greet(\"ນັກຮຽນ\"))\n\n# ຟັງຊັນຄິດຄວາມກວດ\ndef rectangle_area(width, height):\n    return width * height\n\nprint(f\"ພະນາທີ: {rectangle_area(5, 3)}\")',
    5
)
ON CONFLICT (slug) DO NOTHING;