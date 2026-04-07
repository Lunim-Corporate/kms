def extract_rich_text(block: dict) -> str:
    block_type = block.get("type")
    block_data = block.get(block_type, {})
    rich_text = block_data.get("rich_text", [])
    return "".join(part.get("plain_text", "") for part in rich_text)


def blocks_to_text(blocks: list[dict]) -> str:
    lines = []

    for block in blocks:
        text = extract_rich_text(block).strip()
        if text:
            lines.append(text)

    return "\n".join(lines)