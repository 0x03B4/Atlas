from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0008_lecturer_estimated_student_count_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="module",
            name="semester",
            field=models.IntegerField(
                choices=[(1, "Semester 1"), (2, "Semester 2")], default=1
            ),
        ),
    ]
