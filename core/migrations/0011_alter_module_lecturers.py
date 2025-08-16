from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0010_alter_lecturer_consultation_hours_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="module",
            name="lecturers",
            field=models.ManyToManyField(
                blank=True, related_name="modules", to="core.lecturer"
            ),
        ),
    ]
