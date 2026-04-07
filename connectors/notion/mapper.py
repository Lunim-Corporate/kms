from connectors.notion.parser import (
    parse_title,
    parse_rich_text,
    parse_select,
    parse_status,
)


def map_database_row_to_document(row: dict) -> dict:
    properties = row.get("properties", {})

    title = parse_title(properties.get("Title", {}))
    description = parse_rich_text(properties.get("Description", {}))
    content_type = parse_select(properties.get("Content Type", {}))
    priority = parse_select(properties.get("Priority", {}))
    source = parse_select(properties.get("Source", {}))
    status = parse_status(properties.get("Status", {}))

    return {
        "source": "notion",
        "source_id": row.get("id"),
        "title": title,
        "content": description,
        "created_at": row.get("created_time"),
        "updated_at": row.get("last_edited_time"),
        "url": row.get("url"),
        "metadata": {
            "content_type": content_type,
            "priority": priority,
            "source_label": source,
            "status": status,
            "parent": row.get("parent"),
        },
    }