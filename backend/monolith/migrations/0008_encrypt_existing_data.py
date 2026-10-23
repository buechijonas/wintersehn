from django.db import migrations

from monolith.crypto import blind_index, decrypt, encrypt

ENCRYPTED = {
    "monolith_dossier": [
        "birthdate",
        "street",
        "postal_code",
        "nationality",
        "ethnicity",
    ],
    "monolith_event": ["title", "text"],
    "monolith_stance": ["tag"],
    "monolith_addiction": ["kind", "frequency"],
}

HASHED = {
    "monolith_stance": ["tag"],
    "monolith_addiction": ["kind"],
}


def rewrite(cursor, table, columns, transform, hashed):
    cursor.execute(f"SELECT id, {', '.join(columns)} FROM {table}")
    for pk, *values in cursor.fetchall():
        row = dict(zip(columns, values))
        updates = {
            column: transform(value)
            for column, value in row.items()
            if value is not None
        }
        updates |= {f"{column}_hash": blind_index(row[column]) for column in hashed}
        assignments = ", ".join(f"{column} = %s" for column in updates)
        cursor.execute(
            f"UPDATE {table} SET {assignments} WHERE id = %s", [*updates.values(), pk]
        )


def encrypt_rows(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        for table, columns in ENCRYPTED.items():
            rewrite(cursor, table, columns, encrypt, HASHED.get(table, []))


def decrypt_rows(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        for table, columns in ENCRYPTED.items():
            rewrite(cursor, table, columns, decrypt, [])


class Migration(migrations.Migration):

    dependencies = [
        ("monolith", "0007_encrypt_sensitive_data"),
    ]

    operations = [
        migrations.RunPython(encrypt_rows, decrypt_rows),
    ]
