from django.db import migrations

LEGAL_KEYS = ["impressum", "privacy", "cookies", "terms", "disclaimer"]
ADDRESS_PLACEHOLDER = "[[address]]"


def item_markdown(item):
    line = f"- **{item['listtitle']}**"
    return f"{line}\n  - {item['texttitle']}" if item.get("texttitle") else line


def section_markdown(section):
    parts = [
        f"## {section['title']}" if section.get("title") else "",
        f"### {section['subtitle']}" if section.get("subtitle") else "",
        section.get("text", ""),
        "\n".join(item_markdown(item) for item in section.get("items", [])),
        ADDRESS_PLACEHOLDER if section.get("address") else "",
    ]
    return "\n\n".join(part for part in parts if part)


def sections_markdown(sections):
    return "\n\n".join(section_markdown(section) for section in sections)


def without(data, key):
    return {field: value for field, value in data.items() if field != key}


def with_body(data):
    if "sections" not in data:
        return data
    return {**without(data, "sections"), "body": sections_markdown(data["sections"])}


def to_markdown(apps, schema_editor):
    SiteContent = apps.get_model("content", "SiteContent")
    for content in SiteContent.objects.filter(key__in=LEGAL_KEYS):
        content.data = with_body(content.data)
        content.save(update_fields=["data"])
    for content in SiteContent.objects.filter(key="article"):
        content.data = [with_body(post) for post in content.data]
        content.save(update_fields=["data"])


def to_sections(apps, schema_editor):
    SiteContent = apps.get_model("content", "SiteContent")
    for content in SiteContent.objects.filter(key__in=LEGAL_KEYS):
        content.data = {
            **without(content.data, "body"),
            "sections": [{"text": content.data.get("body", "")}],
        }
        content.save(update_fields=["data"])
    for content in SiteContent.objects.filter(key="article"):
        content.data = [
            {**without(post, "body"), "sections": [{"text": post.get("body", "")}]}
            for post in content.data
        ]
        content.save(update_fields=["data"])


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0025_seed_engineering"),
    ]

    operations = [
        migrations.RunPython(to_markdown, to_sections),
    ]
