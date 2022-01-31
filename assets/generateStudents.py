import random
import names

personalities = ['ISTJ', 'ISTP', 'ISFJ', 'ISFP',
                 'INFJ', 'INFP', 'INTJ', 'INTP',
                 'ESTP', 'ESTJ', 'ESFP', 'ESFJ',
                 'ENFP', 'ENFJ', 'ENTP', 'ENTJ',]

# nested list containing 300 of [personality type, full name]
student_personalities = []
for i in range(350):
    generated_student = [
        personalities[(random.randrange(1, 16))], names.get_full_name(gender='male')]
    if generated_student in student_personalities:
        i -= 1
    else:
        student_personalities.append(generated_student)

with open("assets/students.txt", 'w') as f:
    for i in student_personalities:
        print(i[0], i[1], file=f)
