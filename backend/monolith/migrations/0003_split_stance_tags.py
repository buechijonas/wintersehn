import django.utils.timezone
from django.db import migrations, models


def split_tags(apps, schema_editor):
    Stance = apps.get_model("monolith", "Stance")
    topics = list(Stance.objects.filter(tag=""))
    Stance.objects.bulk_create(
        Stance(dossier_id=stance.dossier_id, topic=stance.topic, tag=tag)
        for stance in topics
        for tag in stance.tags
    )
    Stance.objects.filter(tag="").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("monolith", "0002_addiction"),
    ]

    operations = [
        migrations.RemoveConstraint(model_name="stance", name="unique_stance"),
        migrations.AddField(
            model_name="stance",
            name="tag",
            field=models.CharField(default="", max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="stance",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.RunPython(split_tags, migrations.RunPython.noop),
    ]
