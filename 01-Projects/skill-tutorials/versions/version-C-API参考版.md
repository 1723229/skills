# feishu-doc-orchestrator API Reference

## Module: `feishu_doc_orchestrator`

**Source**: `skills/feishu-doc-orchestrator/`  
**Version**: 1.0.0  
**Python**: >= 3.8

---

## Quick Reference

```python
from skills.feishu_doc_orchestrator.scripts.orchestrator import create_doc_from_markdown

result = create_doc_from_markdown(
    markdown_path="path/to/file.md",
    title="Document Title",
    folder_token="folder_xxx"  # optional
)
# Returns: {"doc_url": str, "doc_token": str, "block_count": int}
```

---

## Functions

### `create_doc_from_markdown()`

Create a Feishu document from Markdown file.

**Signature:**
```python
def create_doc_from_markdown(
    markdown_path: str,
    title: str,
    folder_token: Optional[str] = None,
    add_permissions: Optional[List[str]] = None
) -> Dict[str, Any]
```

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `markdown_path` | `str` | ✓ | - | Path to Markdown file |
| `title` | `str` | ✓ | - | Document title |
| `folder_token` | `str` | ✗ | `None` | Target folder token |
| `add_permissions` | `List[str]` | ✗ | `None` | List of collaborator IDs |

**Returns:**

| Key | Type | Description |
|-----|------|-------------|
| `doc_url` | `str` | Full URL to the created document |
| `doc_token` | `str` | Document token (ID) |
| `block_count` | `int` | Number of blocks added |
| `status` | `str` | `"success"` or `"error"` |

**Raises:**

| Exception | Condition |
|-----------|-----------|
| `FileNotFoundError` | Markdown file does not exist |
| `ConfigurationError` | Missing or invalid config |
| `APIError` | Feishu API returned error |

**Example:**

```python
try:
    result = create_doc_from_markdown(
        markdown_path="docs/api.md",
        title="API Documentation",
        folder_token="folder_abc123",
        add_permissions=["ou_user1", "ou_user2"]
    )
    print(f"Created: {result['doc_url']}")
except ConfigurationError as e:
    print(f"Config error: {e}")
```

---

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `FEISHU_APP_ID` | ✓ | Feishu application ID |
| `FEISHU_APP_SECRET` | ✓ | Feishu application secret |
| `FEISHU_DEFAULT_FOLDER` | ✗ | Default folder token |
| `FEISHU_AUTO_COLLABORATOR_ID` | ✗ | Auto-add collaborator |

### Config File Location

```
~/.openclaw/.claude/feishu-config.env
```

**Format:**
```ini
FEISHU_APP_ID=cli_xxxxxxxx
FEISHU_APP_SECRET=xxxxxxxx
```

---

## Supported Block Types

### Text Blocks (11)

| Type | Markdown | Notes |
|------|----------|-------|
| `text` | Plain text | - |
| `heading1` | `# Title` | Level 1 |
| `heading2` | `## Title` | Level 2 |
| ... | ... | Levels 1-9 |
| `quote_container` | `> quote` | Blockquote |

### List Blocks (4)

| Type | Markdown | Example |
|------|----------|---------|
| `bullet` | `- item` | Unordered |
| `ordered` | `1. item` | Numbered |
| `todo` | `- [ ] task` | Checkbox |
| `task` | Special | Task list |

### Special Blocks (5)

| Type | Markdown | Description |
|------|----------|-------------|
| `code` | ` ```code` | Code block |
| `quote` | `>! note` | Callout |
| `callout` | `::: tip` | Alert box |
| `divider` | `---` | Horizontal rule |
| `image` | `![alt](url)` | Image |

### Advanced Blocks (5)

| Type | Support | Notes |
|------|---------|-------|
| `table` | Basic | Simple tables |
| `bitable` | Limited | Requires template |
| `grid` | No | Not supported |
| `sheet` | No | Not supported |
| `board` | No | Not supported |

---

## Sub-modules

### `feishu-md-parser`

Parse Markdown to Feishu block format.

```python
from skills.feishu_md_parser.scripts.md_parser import parse_markdown

blocks = parse_markdown("path/to/file.md")
```

### `feishu-doc-creator-with-permission`

Create document with permission management.

```python
from skills.feishu_doc_creator_with_permission.scripts.doc_creator_with_permission import create_doc

doc = create_doc(title="Title", folder_token="folder_xxx")
add_permission(doc["token"], user_id="ou_xxx")
```

---

## Error Codes

| Code | HTTP | Description |
|------|------|-------------|
| `10003` | 403 | Insufficient permissions |
| `10005` | 401 | Access token expired |
| `230001` | 404 | Document not found |
| `230002` | 403 | No permission to access |
| `230003` | 400 | Unsupported block type |

---

## CLI Usage

### Scripts

```bash
# Test all block types
python3 scripts/test_all_25_blocks.py

# Create simple document
python3 scripts/create_simple.py --input file.md --title "Title"

# Check configuration
python3 scripts/check_config.py
```

### Command Options

```bash
python3 scripts/orchestrator.py [OPTIONS] <markdown-file> <title>

Options:
  --folder-token TEXT    Target folder token
  --collaborator TEXT    Add collaborator (repeatable)
  --verbose             Enable debug logging
  --dry-run             Simulate without creating
```

---

## Related Modules

- [`feishu-wiki-orchestrator`](wiki-orchestrator.md) - Wiki version
- [`feishu-doc-creator`](doc-creator.md) - Simplified version
- [`document-hub`](document-hub.md) - Document processing hub

---

*适用于：需要快速查阅API的技术用户*
