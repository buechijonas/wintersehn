from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_userprofile_govex_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="govex_sub",
            field=models.CharField(blank=True, max_length=64, null=True, unique=True),
        ),
    ]
