from django.db import migrations, models


def mirror_links(apps, schema_editor):
    Link = apps.get_model("monolith", "EventReference").links.through
    pairs = set(
        Link.objects.values_list("from_eventreference_id", "to_eventreference_id")
    )
    Link.objects.bulk_create(
        Link(from_eventreference_id=target, to_eventreference_id=source)
        for source, target in pairs
        if (target, source) not in pairs
    )


class Migration(migrations.Migration):

    dependencies = [
        ("monolith", "0016_chat_image_library"),
    ]

    operations = [
        migrations.AlterField(
            model_name="eventreference",
            name="links",
            field=models.ManyToManyField(blank=True, to="monolith.eventreference"),
        ),
        migrations.RunPython(mirror_links, migrations.RunPython.noop),
    ]
