from django.db import migrations, models


def copy_dossiers(apps, schema_editor):
    Event = apps.get_model("monolith", "Event")
    for event in Event.objects.all():
        event.dossiers.add(event.dossier_id)


def copy_dossier(apps, schema_editor):
    Event = apps.get_model("monolith", "Event")
    for event in Event.objects.all():
        event.dossier_id = (
            event.dossiers.order_by("pk").values_list("pk", flat=True).first()
        )
        event.save(update_fields=["dossier"])


class Migration(migrations.Migration):

    dependencies = [
        ("monolith", "0018_chat_image_set_null"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="dossier",
            field=models.ForeignKey(
                null=True,
                on_delete=models.CASCADE,
                related_name="+",
                to="monolith.dossier",
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="dossiers",
            field=models.ManyToManyField(related_name="events", to="monolith.dossier"),
        ),
        migrations.RunPython(copy_dossiers, copy_dossier),
        migrations.RemoveField(model_name="event", name="dossier"),
    ]
