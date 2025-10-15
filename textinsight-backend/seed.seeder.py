import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "textinsight.settings") 
django.setup()  

from seeders.students_seeder import seed_students
from seeders.teachers_seeder import seed_teachers
from seeders.classes_seeder import seed_classes
from seeders.assignment_seeder import seed_assignments

def run_seeders():
    print("Seeding students...")
    seed_students()
    
    print("Seeding teachers...")
    seed_teachers()
    
    print("Seeding classes...")
    seed_classes()
    
    print("Seeding assignments...")
    seed_assignments()

    print("Seeding complete.")

if __name__ == "__main__":
    run_seeders()
