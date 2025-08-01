from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="lecturer",
            name="status",
        ),
        migrations.AddField(
            model_name="lecturer",
            name="lecturer_type",
            field=models.CharField(
                choices=[
                    ("Junior Lecturer", "Junior Lecturer"),
                    ("Lecturer", "Lecturer"),
                    ("Senior Lecturer", "Senior Lecturer"),
                    ("Associate Professor", "Associate Professor"),
                    ("Professor", "Professor"),
                ],
                default="Lecturer",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="lecturer",
            name="title",
            field=models.CharField(
                choices=[("Mr", "Mr"), ("Ms", "Ms"), ("Dr", "Dr"), ("Prof", "Prof")],
                default="Mr",
                max_length=100,
            ),
        ),
    ]
