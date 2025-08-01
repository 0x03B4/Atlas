from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_remove_lecturer_status_lecturer_lecturer_type_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="student",
            name="completed_modules",
            field=models.ManyToManyField(blank=True, to="core.module"),
        ),
    ]
