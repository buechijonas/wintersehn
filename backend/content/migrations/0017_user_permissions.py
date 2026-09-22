from django.db import migrations

PERMISSIONS = [
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
    ("change_user", "Can update user verification"),
    ("assign_user", "Can assign user roles"),
    ("delete_user", "Can delete users"),
]

# User management (verify, assign role, delete) used to be gated by
# "change_role". It now has its own permissions, so roles that could manage
# users before get them granted explicitly to not lose access.
USER_PERMISSIONS = ["change_user", "assign_user", "delete_user"]


def migrate_group_permissions(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")

    content_type = ContentType.objects.get(app_label="content", model="sitecontent")

    names = dict(PERMISSIONS)
    user_permissions = [
        Permission.objects.get_or_create(
            content_type=content_type, codename=codename, defaults={"name": names[codename]}
        )[0]
        for codename in USER_PERMISSIONS
    ]

    role_managers = Group.objects.filter(
        permissions__content_type=content_type,
        permissions__codename="change_role",
    ).distinct()

    for group in role_managers:
        group.permissions.add(*user_permissions)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0016_split_content_crud"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="sitecontent",
            options={"permissions": PERMISSIONS},
        ),
        migrations.RunPython(migrate_group_permissions, noop),
    ]
