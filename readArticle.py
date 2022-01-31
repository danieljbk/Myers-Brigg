f = open('assets/compatiblePersonalitiesArticle.txt', 'r')

numbers = []
for i in range(1, 17):
    numbers.append(str(i))

data = []

last = ''
for line in f:
    line = line.strip()
    if last in numbers:
        info = line.split('If you are ')[1].split(": ")
        data.append([info[0], info[1].split(", ")])
    last = line

open("assets/compatiblePersonalitiesNestedList.txt", 'w').write(f"{data}")
