from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0009_alter_module_semester"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lecturer",
            name="consultation_hours",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name="lecturer",
            name="email",
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name="lecturer",
            name="employee_id",
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name="lecturer",
            name="estimated_student_count",
            field=models.PositiveIntegerField(
                default=100, help_text="Estimated number of students taught."
            ),
        ),
        migrations.AlterField(
            model_name="lecturer",
            name="office",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name="lecturer",
            name="phone",
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name="module",
            name="code",
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name="module",
            name="credits",
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name="module",
            name="lecturers",
            field=models.ManyToManyField(related_name="modules", to="core.lecturer"),
        ),
        migrations.AlterField(
            model_name="module",
            name="semester",
            field=models.PositiveIntegerField(
                choices=[(1, "Semester 1"), (2, "Semester 2")], default=1
            ),
        ),
        migrations.AlterField(
            model_name="module",
            name="year",
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name="qualification",
            name="duration_years",
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name="qualification",
            name="total_credits",
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name="qualification",
            name="total_modules",
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name="student",
            name="current_semester",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="student",
            name="current_year",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="student",
            name="student_number",
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
