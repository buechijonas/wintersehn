from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0005_seed_countries"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="sitecontent",
            options={
                "permissions": [
                    ("view_ethos", "Can view Ethos"),
                    ("view_cv", "Can view Lebenslauf"),
                    ("view_countries", "Can view Länder"),
                    ("view_media", "Can view Medien (Arbeit)"),
                    ("view_admin", "Can view the admin panel"),
                    ("manage_permissions", "Can manage role permissions"),
                    ("manage_roles", "Can add, rename and delete roles"),
                ]
            },
        ),
    ]
