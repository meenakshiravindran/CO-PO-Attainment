from .models import Student, QuestionCO, StudentAnswer, COAttainment

def calculate_co_attainment(student_id):
    student = Student.objects.get(student_id=student_id)
    question_cos = QuestionCO.objects.filter(questionpattern__assessmentpattern__course__programme=student.program)
    co_attainments = {}

    for question_co in question_cos:
        if question_co.co_number not in co_attainments:
            co_attainments[question_co.co_number] = {'total_marks_obtained': 0, 'total_marks_possible': 0}
        
        student_answer = StudentAnswer.objects.filter(student=student, question_co=question_co).first()
        if student_answer:
            co_attainments[question_co.co_number]['total_marks_obtained'] += student_answer.marks_obtained
            co_attainments[question_co.co_number]['total_marks_possible'] += question_co.question_pattern.marks_per_question

    # Save the results in COAttainment model
    for co_number, data in co_attainments.items():
        COAttainment.objects.update_or_create(
            student=student,
            co_number=co_number,
            defaults={
                'total_marks_obtained': data['total_marks_obtained'],
                'total_marks_possible': data['total_marks_possible']
            }
        )
