import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import monolith.fields
from monolith.crypto import blind_digest


def fill_library(apps, schema_editor):
    ChatImage = apps.get_model("monolith", "ChatImage")
    ChatParticipant = apps.get_model("monolith", "ChatParticipant")
    ChatMessage = apps.get_model("monolith", "ChatMessage")
    kept = {}
    for number, image in enumerate(ChatImage.objects.order_by("created_at", "id"), 1):
        digest = blind_digest(bytes(image.data))
        original = kept.setdefault(digest, image)
        if original != image:
            ChatParticipant.objects.filter(avatar=image).update(avatar=original)
            ChatMessage.objects.filter(image=image).update(image=original)
            image.delete()
            continue
        image.digest = digest
        image.name = f"Bild {number}"
        image.save(update_fields=["digest", "name"])


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("monolith", "0015_chat_side"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel("Attachment", "ChatImage"),
        migrations.AddField(
            model_name="chatimage",
            name="name",
            field=monolith.fields.EncryptedCharField(default="", max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="chatimage",
            name="digest",
            field=models.CharField(default="", editable=False, max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="chatimage",
            name="created_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RunPython(fill_library, migrations.RunPython.noop, atomic=True),
        migrations.RemoveField(model_name="chatimage", name="reference"),
        migrations.AlterField(
            model_name="chatimage",
            name="digest",
            field=models.CharField(editable=False, max_length=64, unique=True),
        ),
        migrations.AlterModelOptions(
            name="chatimage", options={"ordering": ["-created_at", "-id"]}
        ),
        migrations.AlterField(
            model_name="chatparticipant",
            name="avatar",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="avatars",
                to="monolith.chatimage",
            ),
        ),
        migrations.AlterField(
            model_name="chatmessage",
            name="image",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="messages",
                to="monolith.chatimage",
            ),
        ),
    ]
