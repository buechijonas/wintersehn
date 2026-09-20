from django.db import migrations

NEW_PERMISSIONS = [
    ("view_about", "Can view Über mich"),
    ("view_ethos", "Can view Ethos"),
    ("view_cv", "Can view Lebenslauf"),
    ("view_countries", "Can view Länder"),
    ("view_media", "Can view Medien (Arbeit)"),
    ("view_admin", "Can view the admin panel"),
    ("add_permission", "Can create permission assignments"),
    ("change_permission", "Can update permission assignments"),
    ("delete_permission", "Can delete permission assignments"),
    ("add_role", "Can create roles"),
    ("change_role", "Can update roles"),
    ("view_role", "Can view roles"),
    ("delete_role", "Can delete roles"),
]

# Roles that had "manage_permissions"/"manage_roles" get the full set of
# their replacement permissions, so nobody silently loses admin access.
REPLACEMENTS = {
    "manage_permissions": ["add_permission", "change_permission", "delete_permission"],
    "manage_roles": ["add_role", "change_role", "view_role", "delete_role"],
}


def migrate_group_permissions(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")

    content_type = ContentType.objects.get(app_label="content", model="sitecontent")

    # AlterModelOptions only updates migration state; the actual replacement
    # Permission rows aren't created until the post_migrate signal fires
    # (after this whole migration finishes), so they're created explicitly
    # here to be assignable to groups within this same migration.
    new_permissions_by_codename = {}
    for codename, name in NEW_PERMISSIONS:
        permission, _ = Permission.objects.get_or_create(
            content_type=content_type, codename=codename, defaults={"name": name}
        )
        new_permissions_by_codename[codename] = permission

    old_codenames = list(REPLACEMENTS.keys())
    affected_groups = Group.objects.filter(
        permissions__content_type=content_type,
        permissions__codename__in=old_codenames,
    ).distinct()

    for group in affected_groups:
        held = group.permissions.filter(
            content_type=content_type, codename__in=old_codenames
        ).values_list("codename", flat=True)
        for old_codename in held:
            for new_codename in REPLACEMENTS[old_codename]:
                group.permissions.add(new_permissions_by_codename[new_codename])

    Permission.objects.filter(
        content_type=content_type, codename__in=old_codenames
    ).delete()


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0014_seed_article"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="sitecontent",
            options={"permissions": NEW_PERMISSIONS},
        ),
        migrations.RunPython(migrate_group_permissions, noop),
    ]
