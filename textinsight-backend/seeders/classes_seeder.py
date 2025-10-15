import random
from faker import Faker
from classes.models import Class, ClassStudents
from authentication.models import User

fake = Faker()

def seed_classes():
    teachers = User.objects.filter(role="teacher")  
    students = User.objects.filter(role="student") 

    for _ in range(4):
        teacher = random.choice(teachers)  
        new_class = Class.objects.create(
            class_name=fake.word().capitalize() + " Class",
            class_code=fake.unique.word().upper(),
            teacher_name=teacher.name,
            teacher=teacher,  
            student_limit=50,
            student_count=0,
        )
        enroll_students_in_class(new_class, students) 

def enroll_students_in_class(new_class, students):
    num_students = random.randint(5, 50)  
    enrolled_students = random.sample(list(students), num_students)

    for student in enrolled_students:
        ClassStudents.objects.create(
            class_id=new_class,  
            student_id=student  
        )
    
    new_class.student_count = num_students  
    new_class.save()

    print(f"Enrolled {num_students} students in {new_class.class_name}")
