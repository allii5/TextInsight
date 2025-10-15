from faker import Faker
from authentication.models import User
from media.models import Media
from django.contrib.auth.hashers import make_password

fake = Faker()

def seed_students():
    for _ in range(50):
        student = User.objects.create(
            username=fake.user_name(),
            name=fake.name(),
            email=fake.email(),
            password=make_password("strongpassword123"),  
            role="student",
            profile_picture=seed_student_media(),  
            status="verified"
        )

def seed_student_media():
    media = Media.objects.create(
        file_path=fake.image_url(),
        file_type="image",
        uploaded_by=None  
    )
    return media.file_path  
