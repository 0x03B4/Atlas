from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_student_completed_modules"),
    ]

    operations = [
        migrations.AlterField(
            model_name="qualificationmodule",
            name="module_type",
            field=models.CharField(
                choices=[("Core", "Core"), ("Auxiliary", "Auxiliary")], max_length=20
            ),
        ),
    ]
