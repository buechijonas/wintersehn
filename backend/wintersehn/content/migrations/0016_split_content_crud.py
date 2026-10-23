from django.db import migrations

NEW_PERMISSIONS = [
    ("view_admin", "Can view the admin panel"),
    ("add_about", "Can create Über mich entries"),
    ("view_about", "Can view Über mich"),
    ("change_about", "Can update Über mich"),
    ("delete_about", "Can delete Über mich entries"),
    ("add_ethos", "Can create Ethos entries"),
    ("view_ethos", "Can view Ethos"),
    ("change_ethos", "Can update Ethos"),
    ("delete_ethos", "Can delete Ethos entries"),
    ("add_cv", "Can create Lebenslauf entries"),
    ("view_cv", "Can view Lebenslauf"),
    ("change_cv", "Can update Lebenslauf"),
    ("delete_cv", "Can delete Lebenslauf entries"),
    ("add_countries", "Can create Länder entries"),
    ("view_countries", "Can view Länder"),
    ("change_countries", "Can update Länder"),
    ("delete_countries", "Can delete Länder entries"),
    ("add_media", "Can create Medien entries"),
    ("view_media", "Can view Medien (Arbeit)"),
    ("change_media", "Can update Medien (Arbeit)"),
    ("delete_media", "Can delete Medien entries"),
    ("add_permission", "Can create permission assignments"),
    ("change_permission", "Can update permission assignments"),
    ("delete_permission", "Can delete permission assignments"),
    ("add_role", "Can create roles"),
    ("change_role", "Can update roles"),
    ("view_role", "Can view roles"),
    ("delete_role", "Can delete roles"),
]

# Content editing used to be gated by the single generic
# "change_sitecontent" permission for every content key. About/Ethos/CV/
# Countries/Media now have their own dedicated CRUD permissions, so any
# role that could edit content before needs those granted explicitly to
# not lose write access.
CONTENT_CRUD_KEYS = ["about", "ethos", "cv", "countries", "media"]


def migrate_group_permissions(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")

    content_type = ContentType.objects.get(app_label="content", model="sitecontent")

    new_permissions_by_codename = {}
    for codename, name in NEW_PERMISSIONS:
        permission, _ = Permission.objects.get_or_create(
            content_type=content_type, codename=codename, defaults={"name": name}
        )
        new_permissions_by_codename[codename] = permission

    editor_groups = Group.objects.filter(
        permissions__content_type=content_type,
        permissions__codename="change_sitecontent",
    ).distinct()

    for group in editor_groups:
        for key in CONTENT_CRUD_KEYS:
            for verb in ("add", "change", "delete"):
                group.permissions.add(new_permissions_by_codename[f"{verb}_{key}"])


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0015_split_manage_permissions"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="sitecontent",
            options={"permissions": NEW_PERMISSIONS},
        ),
        migrations.RunPython(migrate_group_permissions, noop),
    ]
