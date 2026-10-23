from django.db import migrations


def add_consent_field(apps, schema_editor):
    SiteContent = apps.get_model("content", "SiteContent")
    cookies = SiteContent.objects.filter(key="cookies").first()
    if cookies is None:
        return
    cookies.data = {**cookies.data, "consentField": "cookies"}
    cookies.save(update_fields=["data"])


def remove_consent_field(apps, schema_editor):
    SiteContent = apps.get_model("content", "SiteContent")
    cookies = SiteContent.objects.filter(key="cookies").first()
    if cookies is None:
        return
    cookies.data = {k: v for k, v in cookies.data.items() if k != "consentField"}
    cookies.save(update_fields=["data"])


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0018_remove_delete_user_permission"),
    ]

    operations = [
        migrations.RunPython(add_consent_field, remove_consent_field),
    ]
