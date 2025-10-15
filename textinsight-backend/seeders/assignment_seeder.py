from faker import Faker
import random
from essay.models import Assignment
from classes.models import Class

fake = Faker()

def seed_assignments():
    classes = Class.objects.all()  
    for _ in range(5):
        assigned_class = random.choice(classes)  
        Assignment.objects.create(
            title=fake.sentence(nb_words=6),
            description=fake.text(),
            class_id=assigned_class,  
            expected_keywords=fake.words(nb=25),  
            due_date=fake.date_this_year(),
            created_at=fake.date_this_year()
        )
