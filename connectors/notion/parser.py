def extract_plain_text(items: list[dict]) -> str:
    if not items:
        return ""
    return "".join(item.get("plain_text", "") for item in items)


def parse_title(prop: dict) -> str:
    return extract_plain_text(prop.get("title", []))


def parse_rich_text(prop: dict) -> str:
    return extract_plain_text(prop.get("rich_text", []))


def parse_select(prop: dict) -> str:
    select = prop.get("select")
    return select.get("name", "") if select else ""


def parse_status(prop: dict) -> str:
    status = prop.get("status")
    return status.get("name", "") if status else ""