def format_file_size(size_bytes: int) -> str:
    """
    Formats raw byte count into human-readable MB/KB string.
    """
    if not size_bytes:
        return "0 B"
    if size_bytes >= 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    return f"{size_bytes / 1024:.1f} KB"

def truncate_text(text: str, max_length: int = 50) -> str:
    """
    Truncates text with ellipsis if length exceeds max_length.
    """
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return f"{text[:max_length]}..."
