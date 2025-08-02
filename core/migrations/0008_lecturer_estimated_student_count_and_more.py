from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0007_alter_qualification_format"),
    ]

    operations = [
        migrations.AddField(
            model_name="lecturer",
            name="estimated_student_count",
            field=models.IntegerField(
                blank=True,
                default=100,
                help_text="Estimated number of students taught.",
            ),
        ),
        migrations.AddField(
            model_name="lecturer",
            name="highest_qualification",
            field=models.CharField(
                blank=True,
                choices=[
                    ("BSc", "BSc"),
                    ("Hons", "Hons"),
                    ("MSc", "MSc"),
                    ("PhD", "PhD"),
                ],
                default="MSc",
                max_length=10,
            ),
        ),
    ]
