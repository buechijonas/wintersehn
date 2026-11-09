from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lumon", "0003_mediafile"),
    ]

    operations = [
        migrations.RemoveConstraint(model_name="title", name="lumon_unique_title"),
        migrations.RemoveConstraint(
            model_name="mediafile", name="lumon_unique_media_file"
        ),
        migrations.RenameField(
            model_name="title", old_name="tmdb_id", new_name="catalog_id"
        ),
        migrations.RenameField(
            model_name="upload", old_name="tmdb_id", new_name="catalog_id"
        ),
        migrations.RenameField(
            model_name="mediafile", old_name="tmdb_id", new_name="catalog_id"
        ),
        migrations.RemoveField(model_name="title", name="poster_path"),
        migrations.AddField(
            model_name="title",
            name="poster",
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterModelOptions(
            name="mediafile",
            options={"ordering": ["catalog_id", "season", "episode"]},
        ),
        migrations.AddConstraint(
            model_name="title",
            constraint=models.UniqueConstraint(
                fields=("catalog_id", "media_type"), name="lumon_unique_title"
            ),
        ),
        migrations.AddConstraint(
            model_name="mediafile",
            constraint=models.UniqueConstraint(
                fields=("media_type", "catalog_id", "season", "episode"),
                name="lumon_unique_media_file",
                nulls_distinct=False,
            ),
        ),
    ]
