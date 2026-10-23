from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_userprofile"),
    ]

    operations = [
        # Backfill existing profiles as verified (grandfathered in), then flip the
        # go-forward default to False so only new signups need verification.
        migrations.AddField(
            model_name="userprofile",
            name="verified",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="verified",
            field=models.BooleanField(default=False),
        ),
    ]
