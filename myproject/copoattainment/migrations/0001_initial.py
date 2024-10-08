# Generated by Django 5.1 on 2024-08-20 07:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('credits', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Programme',
            fields=[
                ('programme_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='AssessmentPattern',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assessment_type', models.CharField(help_text='e.g., Midterm, Final, Assignment', max_length=50)),
                ('total_marks', models.PositiveIntegerField(help_text='Total marks for this assessment')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='copoattainment.course')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='programme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='copoattainment.programme'),
        ),
        migrations.CreateModel(
            name='QuestionPattern',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_type', models.CharField(help_text='e.g., 1-mark, 2-mark, 3-mark', max_length=50)),
                ('total_questions', models.PositiveIntegerField(help_text='Total number of questions of this type')),
                ('questions_to_answer', models.PositiveIntegerField(help_text='Number of questions to answer')),
                ('marks_per_question', models.PositiveIntegerField(help_text='Marks for each question of this type')),
                ('assessment_pattern', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='copoattainment.assessmentpattern')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionCO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_number', models.PositiveIntegerField()),
                ('co_number', models.CharField(help_text='Course Outcome number', max_length=10)),
                ('question_pattern', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='copoattainment.questionpattern')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('enrollment_year', models.PositiveIntegerField()),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='copoattainment.programme')),
            ],
        ),
        migrations.CreateModel(
            name='COAttainment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('co_number', models.CharField(max_length=10)),
                ('total_marks_obtained', models.PositiveIntegerField()),
                ('total_marks_possible', models.PositiveIntegerField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='copoattainment.student')),
            ],
        ),
        migrations.CreateModel(
            name='StudentAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks_obtained', models.PositiveIntegerField()),
                ('question_co', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='copoattainment.questionco')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='copoattainment.student')),
            ],
        ),
    ]
