from django.db import models

# 1. Student Information Table
class Student(models.Model):
    student_id = models.CharField(max_length=10, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    program = models.ForeignKey('Programme', on_delete=models.CASCADE)
    enrollment_year = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.student_id})'

# 2. Programme DB
class Programme(models.Model):
    programme_id = models.IntegerField(primary_key=True) 
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# 3. Courses
class Course(models.Model):
    course_id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    credits = models.PositiveIntegerField()
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# 4. Assessment Pattern
class AssessmentPattern(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    assessment_type = models.CharField(max_length=50, help_text="e.g., Internal, Final, Assignment")
    total_marks = models.PositiveIntegerField(help_text="Total marks for this assessment")

    def __str__(self):
        return f'{self.assessment_type} - {self.course.name}'

# 5. Question Pattern for Each Assessment
class QuestionPattern(models.Model):
    assessment_pattern = models.ForeignKey(AssessmentPattern, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=50, help_text="e.g., 1-mark, 2-mark, 3-mark")
    total_questions = models.PositiveIntegerField(help_text="Total number of questions of this type")
    questions_to_answer = models.PositiveIntegerField(help_text="Number of questions to answer")
    marks_per_question = models.PositiveIntegerField(help_text="Marks for each question of this type")

    def __str__(self):
        return f'{self.question_type} - {self.assessment_pattern.course.name}'

# 6. Question Number and the Respective CO it is From
class QuestionCO(models.Model):
    question_pattern = models.ForeignKey(QuestionPattern, on_delete=models.CASCADE)
    question_number = models.PositiveIntegerField()
    co_number = models.CharField(max_length=10, help_text="Course Outcome number")

    def __str__(self):
        return f'Q{self.question_number} - CO{self.co_number} ({self.question_pattern.assessment_pattern.course.name})'

# 7. Student's Answers to Questions
class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    question_co = models.ForeignKey(QuestionCO, on_delete=models.CASCADE)
    marks_obtained = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.student} - {self.question_co}'

# 8. CO Attainment
class COAttainment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    co_number = models.CharField(max_length=10)
    total_marks_obtained = models.PositiveIntegerField()
    total_marks_possible = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.student} - CO{self.co_number}'

