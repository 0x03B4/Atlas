import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="AcademicRule",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("file", models.FileField(upload_to="academic_rules/")),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Lecturer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("title", models.CharField(max_length=100)),
                ("bio", models.TextField()),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(max_length=20)),
                ("office", models.CharField(max_length=100)),
                ("consultation_hours", models.CharField(max_length=100)),
                ("employee_id", models.CharField(max_length=20)),
                ("status", models.CharField(max_length=20)),
                ("joined_year", models.IntegerField()),
                ("expertise_areas", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Qualification",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("duration_years", models.IntegerField()),
                ("total_credits", models.IntegerField()),
                ("total_modules", models.IntegerField()),
                ("format", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Module",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("code", models.CharField(max_length=20)),
                ("description", models.TextField()),
                ("credits", models.IntegerField()),
                ("year", models.IntegerField()),
                ("semester", models.IntegerField()),
                (
                    "corequisites",
                    models.ManyToManyField(
                        blank=True, related_name="corequisite_for", to="core.module"
                    ),
                ),
                ("lecturers", models.ManyToManyField(to="core.lecturer")),
                (
                    "prerequisites",
                    models.ManyToManyField(
                        blank=True, related_name="prerequisite_for", to="core.module"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="QualificationModule",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "module_type",
                    models.CharField(
                        choices=[
                            ("Core", "Core"),
                            ("Auxiliary", "Auxiliary"),
                            ("Elective", "Elective"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "module",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.module"
                    ),
                ),
                (
                    "qualification",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.qualification",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("student_number", models.CharField(max_length=20)),
                ("current_year", models.IntegerField(blank=True, null=True)),
                ("current_semester", models.IntegerField(blank=True, null=True)),
                (
                    "qualification",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="core.qualification",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
