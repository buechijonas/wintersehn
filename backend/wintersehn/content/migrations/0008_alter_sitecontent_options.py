from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0007_seed_about"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="sitecontent",
            options={
                "permissions": [
                    ("view_about", "Can view Über mich"),
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
