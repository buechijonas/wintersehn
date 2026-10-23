from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("monolith", "0008_encrypt_existing_data"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="addiction",
            constraint=models.UniqueConstraint(
                fields=("dossier", "kind_hash"), name="unique_addiction"
            ),
        ),
        migrations.AddConstraint(
            model_name="stance",
            constraint=models.UniqueConstraint(
                fields=("dossier", "topic", "tag_hash"), name="unique_stance"
            ),
        ),
    ]
