from faker import Faker
from authentication.models import User
from media.models import Media
from django.contrib.auth.hashers import make_password

fake = Faker()

def seed_teachers():
    for _ in range(3):
        teacher = User.objects.create(
            username=fake.user_name(),
            name=fake.name(),
            email=fake.email(),
            password=make_password("strongpassword123"), 
            role="teacher",
            education_level="Masters",  
            profile_picture=seed_teacher_media(),  
            status="verified"
        )

def seed_teacher_media():
    media = Media.objects.create(
        file_path=fake.image_url(),
        file_type="image",
        uploaded_by=None  
    )
    return media.file_path 
