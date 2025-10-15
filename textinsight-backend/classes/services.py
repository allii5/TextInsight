from repositories.user_repository import UserRepository
from repositories.class_repository import ClassStudentsRepository, ClassRepository
from django.db import transaction
from datetime import datetime
from services.email_service import EmailService



class ClassService:
    def __init__(self):
        self.user_repo = UserRepository()
        self.class_repo = ClassRepository()
        self.class_students_repo = ClassStudentsRepository()

    @transaction.atomic
    def create_class_with_students(self, class_name, teacher_id, selected_usernames, csv_usernames):
        errors = []

        # Combine Manual and CSV Usernames
        combined_usernames = list(set(selected_usernames + csv_usernames))

        if len(combined_usernames) < 7:
            errors.append("A class must have at least 7 students.")
        if len(combined_usernames) > 50:
            combined_usernames = combined_usernames[:50]  # Limit to 50 students

        existing_usernames = self.user_repo.get_existing_usernames(combined_usernames)
        invalid_usernames = list(set(combined_usernames) - set(existing_usernames))

        if invalid_usernames:
            errors.append(f"The following usernames are invalid: {', '.join(invalid_usernames)}")

        if errors:
            return {"status": "error", "errors": errors}

        teacher = self.user_repo.get_by_id(teacher_id)
        if not teacher:
            return {"status": "error", "errors": ["Teacher not found."]}
        
        # Generate Class Code
        last_class_code = self.class_repo.get_last_class_code()
        new_class_code = self._generate_next_class_code(last_class_code)


        new_class = self.class_repo.create({
            "class_name": class_name,
            "class_code": new_class_code,
            "teacher_name": teacher.name,
            "teacher": teacher,
            "student_limit": 50,
            "student_count": len(existing_usernames),
        })

        self.class_students_repo.add_students_to_class(new_class.id, existing_usernames)

        self.user_repo.increment_class_count(teacher_id)
        self.user_repo.increment_class_count_for_students(existing_usernames)

        # Notify teacher about class creation
        EmailService.notify_teacher_class_created(
            teacher_email=teacher.email,
            teacher_name=teacher.name,
            class_name=class_name,
            class_code=new_class.class_code,
            student_count=len(existing_usernames)
        )

        # Notify students about being added to the class
        for student_username in existing_usernames:
            student = self.user_repo.get_by_username(student_username)
            EmailService.notify_student_added_to_class(
                student_email=student.email,
                student_name=student.name,
                class_name=class_name,
                teacher_name=teacher.name
            )

        return {
            "status": "success",
            "message": f"Class '{class_name}' created successfully with {len(existing_usernames)} students.",
            "invalid_usernames": invalid_usernames
        }

    def _generate_next_class_code(self, last_class_code):
        """
        Generate the next class code based on the last class code.
        """
        if not last_class_code:
            return "A000"  # Start with "A000" if no class codes exist

        prefix = last_class_code[0]
        number = int(last_class_code[1:])

        if number < 999:
            number += 1
        else:
            prefix = chr(ord(prefix) + 1)
            number = 0

        return f"{prefix}{number:03d}"
    
    @transaction.atomic
    def update_class(self, class_id, class_name, added_usernames, teacher_id):
        errors = []

        # Step 1: Validate Class ID and Teacher
        class_obj = self.class_repo.findById(class_id)
        if not class_obj:
            errors.append("Class not found.")
            return {"status": "error", "errors": errors}
        
        if class_obj.teacher.id != teacher_id:
            errors.append("You are not the teacher of this class.")
            return {"status": "error", "errors": errors}

        # Step 2: Update Class Name
        if class_name:
            class_obj.class_name = class_name
            class_obj.save()

        # Step 3: Validate and Add Students
        if added_usernames:
            existing_usernames = self.user_repo.get_existing_usernames(added_usernames)
            invalid_usernames = list(set(added_usernames) - set(existing_usernames))

            if invalid_usernames:
                errors.append(f"Invalid usernames: {', '.join(invalid_usernames)}")

            valid_usernames = [username for username in existing_usernames if not self.class_students_repo.is_student_in_class(class_id, username)]

            total_count = class_obj.student_count+len(valid_usernames)

            if total_count <= 50: 
                # Add valid students to the class, ensuring no duplicates
                self.class_students_repo.add_students_to_class(class_id, valid_usernames)
                self.user_repo.increment_class_count_for_students(valid_usernames)
                class_obj.student_count = total_count
                class_obj.save()

            else: 

                can_add = 50 - class_obj.student_count
                valid_usernames = valid_usernames[:can_add]
                class_obj.student_count = 50
                class_obj.save()

            # Notify students that they've been added to the class
            for student_username in valid_usernames:
                student = self.user_repo.get_by_username(student_username)
                EmailService.notify_student_added_to_class(
                    student_email=student.email,
                    student_name=student.name,
                    class_name=class_obj.class_name,
                    teacher_name=class_obj.teacher.name
                )

        if errors:
            return {"status": "error", "errors": errors}

        return {"status": "success", "message": "Class updated successfully."}
    
    def fetch_teacher_classes(self, teacher_id):
        """
        Fetches classes created by the teacher and returns the required data.
        """
        classes = self.class_repo.get_teacher_classes(teacher_id)
        return [
            {
                "id": cls.id,
                "class_name": cls.class_name,
                "class_code": cls.class_code,
                "student_count": cls.student_count,
                "student_limit": cls.student_limit,
            }
            for cls in classes
        ]
    
    def search_students_in_class(self, class_id, search_query=None):
        """
        Fetch students in a class with optional search by username or name.
        """
        return self.class_students_repo.get_students_in_class(class_id, search_query)
    
    def search_students(self, search_query=None):
        """
        Search for students by username or name.
        """
        return self.user_repo.search_students(search_query)