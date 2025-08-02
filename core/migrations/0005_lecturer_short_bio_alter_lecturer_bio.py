from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_alter_qualificationmodule_module_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="lecturer",
            name="short_bio",
            field=models.TextField(
                blank=True, help_text="A brief summary for the profile header."
            ),
        ),
        migrations.AlterField(
            model_name="lecturer",
            name="bio",
            field=models.TextField(
                help_text="The full biography for the main content area."
            ),
        ),
    ]
