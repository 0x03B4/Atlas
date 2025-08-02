from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_alter_lecturer_expertise_areas_learningoutcome"),
    ]

    operations = [
        migrations.AlterField(
            model_name="qualification",
            name="format",
            field=models.CharField(
                choices=[("Contact", "Contact"), ("Distance", "Distance")],
                default="Contact",
                max_length=10,
            ),
        ),
    ]
