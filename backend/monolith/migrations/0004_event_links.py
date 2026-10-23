import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("monolith", "0003_split_stance_tags"),
    ]

    operations = [
        migrations.RemoveField(model_name="stance", name="tags"),
        migrations.RemoveField(model_name="stance", name="updated_at"),
        migrations.AlterModelOptions(
            name="stance",
            options={
                "ordering": ["created_at", "id"],
                "verbose_name_plural": "Stances",
            },
        ),
        migrations.AddConstraint(
            model_name="stance",
            constraint=models.UniqueConstraint(
                fields=("dossier", "topic", "tag"), name="unique_stance"
            ),
        ),
        migrations.AddField(
            model_name="stance",
            name="event",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="stances",
                to="monolith.event",
            ),
        ),
        migrations.AddField(
            model_name="addiction",
            name="event",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="addictions",
                to="monolith.event",
            ),
        ),
        migrations.AddField(
            model_name="relationship",
            name="event",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="relationships",
                to="monolith.event",
            ),
        ),
    ]
