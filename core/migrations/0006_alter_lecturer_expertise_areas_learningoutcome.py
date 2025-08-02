import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_lecturer_short_bio_alter_lecturer_bio"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lecturer",
            name="expertise_areas",
            field=models.TextField(
                help_text="Comma-separated list of expertise areas."
            ),
        ),
        migrations.CreateModel(
            name="LearningOutcome",
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
                ("description", models.TextField()),
                (
                    "module",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="learning_outcomes",
                        to="core.module",
                    ),
                ),
            ],
            options={
                "ordering": ["id"],
            },
        ),
    ]
