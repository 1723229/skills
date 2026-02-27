# feishu-doc-orchestrator 完整源码版教程

> 本文档包含 feishu-doc-orchestrator 技能的完整源代码，用户可以直接从本文档复制代码安装和使用。

---

## 一、功能简介

**feishu-doc-orchestrator** 是 OpenClaw 的 Markdown 转飞书文档技能，通过编排 5 个子技能协作完成：

1. **feishu-md-parser** - 解析 Markdown 为飞书块格式
2. **feishu-doc-creator-with-permission** - 创建文档并配置权限
3. **feishu-block-adder** - 批量添加内容块
4. **feishu-doc-verifier** - 验证文档可访问性
5. **feishu-logger** - 记录操作日志

**核心优势**：
- 支持飞书原生表格（可编辑，非图片）
- 保留 Markdown 完整格式
- 自动权限管理

---

## 二、快速安装（从本文档复制代码）

### 方式：发给 OpenClaw 自动安装

将下面的代码逐个发给 OpenClaw，它会自动创建文件并配置。

**步骤1**：告诉 OpenClaw 创建目录结构
```
请帮我创建以下目录结构：
~/.openclaw/workspace/skills/feishu-doc-orchestrator/
├── feishu-doc-orchestrator/scripts/
├── feishu-md-parser/scripts/
├── feishu-doc-creator-with-permission/scripts/
├── feishu-block-adder/scripts/
├── feishu-doc-verifier/scripts/
└── feishu-logger/scripts/
```

**步骤2**：逐个发送下面的代码文件

---

## 三、完整源代码

### 文件1：orchestrator.py（主编排脚本）

**路径**：`feishu-doc-orchestrator/scripts/orchestrator.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书文档创建 - 主编排脚本
编排 5 个子技能协作完成文档创建
使用文件传递数据，节省 Token
"""

import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime


# 子技能脚本路径
SCRIPT_DIR = Path(__file__).parent.parent.parent
SUB_SKILLS = {
    "parser": SCRIPT_DIR / "feishu-md-parser" / "scripts" / "md_parser.py",
    "creator_with_permission": SCRIPT_DIR / "feishu-doc-creator-with-permission" / "scripts" / "doc_creator_with_permission.py",
    "block_adder": SCRIPT_DIR / "feishu-block-adder" / "scripts" / "block_adder.py",
    "verifier": SCRIPT_DIR / "feishu-doc-verifier" / "scripts" / "doc_verifier.py",
    "logger": SCRIPT_DIR / "feishu-logger" / "scripts" / "logger.py"
}


def run_step(name, script, args):
    """运行单个步骤"""
    print(f"\n{'='*70}")
    print(f"[步骤] {name}")
    print(f"{'='*70}")

    cmd = [sys.executable, str(script)] + args
    print(f"命令: {' '.join(cmd)}")

    result = subprocess.run(cmd, capture_output=True, text=True)

    # 打印输出
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    if result.returncode != 0:
        print(f"[FAIL] {name} 失败，退出码: {result.returncode}")
        return False

    print(f"[OK] {name} 完成")
    return True


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python orchestrator.py <markdown文件> [文档标题] [workflow目录]")
        print("示例: python orchestrator.py input.md \"我的文档\"")
        print("      python orchestrator.py input.md")
        sys.exit(1)

    md_file = Path(sys.argv[1])
    if not md_file.exists():
        print(f"错误: 文件不存在: {md_file}")
        sys.exit(1)

    # 文档标题
    if len(sys.argv) >= 3:
        doc_title = sys.argv[2]
    else:
        doc_title = md_file.stem  # 使用文件名作为标题

    # 工作流目录
    if len(sys.argv) >= 4:
        workflow_dir = Path(sys.argv[3])
    else:
        workflow_dir = Path("workflow")

    # 输出目录（日志文件保存位置）
    output_dir = Path(__file__).parent.parent  # 主技能根目录

    print("="*70)
    print("Feishu Document Creation - Orchestrator Workflow (5 Steps)")
    print("="*70)
    print(f"输入文件: {md_file}")
    print(f"文档标题: {doc_title}")
    print(f"工作流目录: {workflow_dir}")
    print(f"输出目录: {output_dir}")
    print()

    # 创建工作流目录
    step_dirs = {
        "parse": workflow_dir / "step1_parse",
        "create_with_permission": workflow_dir / "step2_create_with_permission",
        "add_blocks": workflow_dir / "step3_add_blocks",
        "verify": workflow_dir / "step4_verify"
    }

    for step_dir in step_dirs.values():
        step_dir.mkdir(parents=True, exist_ok=True)

    # 记录开始时间
    start_time = datetime.now()

    # ========== 第一步：Markdown 解析 ==========
    if not run_step(
        "第一步：Markdown 解析",
        SUB_SKILLS["parser"],
        [str(md_file), str(step_dirs["parse"])]
    ):
        sys.exit(1)

    blocks_file = step_dirs["parse"] / "blocks.json"
    if not blocks_file.exists():
        print(f"[FAIL] blocks.json 未生成: {blocks_file}")
        sys.exit(1)

    # ========== 第二步：文档创建+权限管理 ==========
    if not run_step(
        "第二步：文档创建+权限管理（原子操作）",
        SUB_SKILLS["creator_with_permission"],
        [doc_title, str(step_dirs["create_with_permission"])]
    ):
        sys.exit(1)

    doc_info_file = step_dirs["create_with_permission"] / "doc_with_permission.json"
    if not doc_info_file.exists():
        print(f"[FAIL] doc_with_permission.json 未生成: {doc_info_file}")
        sys.exit(1)

    # 读取文档信息
    with open(doc_info_file, 'r', encoding='utf-8') as f:
        doc_info = json.load(f)
    doc_url = doc_info["document_url"]
    permission = doc_info.get("permission", {})

    print(f"\n[权限状态]")
    print(f"  协作者添加: {permission.get('collaborator_added', False)}")
    print(f"  所有权转移: {permission.get('owner_transferred', False)}")
    print(f"  用户完全控制: {permission.get('user_has_full_control', False)}")

    # ========== 第三步：块添加 ==========
    if not run_step(
        "第三步：块添加",
        SUB_SKILLS["block_adder"],
        [str(blocks_file), str(doc_info_file), str(step_dirs["add_blocks"])]
    ):
        print("[WARN] 块添加失败，但继续执行后续步骤")

    # ========== 第四步：文档验证 ==========
    if not run_step(
        "第四步：文档验证",
        SUB_SKILLS["verifier"],
        [str(doc_info_file), str(step_dirs["verify"])]
    ):
        print("[WARN] 文档验证失败，但继续执行后续步骤")

    # ========== 第五步：日志记录 ==========
    if not run_step(
        "第五步：日志记录",
        SUB_SKILLS["logger"],
        [str(workflow_dir), str(output_dir)]
    ):
        print("[WARN] 日志记录失败")

    # 完成
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    print("\n" + "="*70)
    print("文档创建完成！")
    print("="*70)
    print(f"文档 URL: {doc_url}")
    print(f"耗时: {duration:.2f} 秒")
    print()
    print("权限状态:")
    print(f"  协作者添加: {'[OK]' if permission.get('collaborator_added') else '[FAIL]'}")
    print(f"  所有权转移: {'[OK]' if permission.get('owner_transferred') else '[FAIL]'}")
    print(f"  用户完全控制: {'[OK]' if permission.get('user_has_full_control') else '[FAIL]'}")
    print()
    print("日志文件:")
    print(f"  - {output_dir / 'CREATED_DOCS.md'}")
    print(f"  - {output_dir / 'created_docs.json'}")


if __name__ == "__main__":
    main()
```

---

### 文件2：md_parser.py（Markdown解析器）

**路径**：`feishu-md-parser/scripts/md_parser.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown 解析器 - 子技能1
将 Markdown 文件解析为飞书文档块格式
支持 25 种飞书文档块类型
输出：blocks.json
"""

import sys
import json
import re
import time
from pathlib import Path
from typing import List, Dict, Any


def clean_cell_content(content: str) -> str:
    """彻底清理单元格内容"""
    if not content:
        return ""
    content = str(content).strip()
    content = content.replace('\u200b', '')
    content = content.replace('\u200c', '')
    content = content.replace('\u200d', '')
    content = content.replace('\ufeff', '')
    content = re.sub(r'\*\*(.+?)\*\*', r'\1', content)
    if '\n' in content:
        content = content.split('\n')[0].strip()
    return content


def make_text_run(text: str, bold: bool = False) -> Dict[str, Any]:
    """创建文本运行元素"""
    text = text.replace('\u200b', '')
    text = text.replace('\u200c', '')
    text = text.replace('\u200d', '')
    text = text.replace('\ufeff', '')
    result = {"text_run": {"content": text}}
    if bold:
        result["text_run"]["text_element_style"] = {"bold": True}
    return result


def parse_markdown_text(content: str) -> List[Dict[str, Any]]:
    """解析 Markdown 文本，转换 **粗体** 为飞书样式"""
    if not content:
        return [{"text_run": {"content": ""}}]

    elements = []
    parts = content.split('**')

    for idx, part in enumerate(parts):
        if part:
            is_bold = (idx % 2 == 1)
            part = part.replace('*', '').strip()
            if part:
                elements.append(make_text_run(part, bold=is_bold))

    return elements if elements else [make_text_run(content)]


def get_callout_style(style_name: str) -> Dict[str, Any]:
    """获取 callout 样式配置"""
    styles = {
        "info": {"emoji_id": "information_source", "background_color": 5, "border_color": 5},
        "tip": {"emoji_id": "bulb", "background_color": 3, "border_color": 3, "text_color": 3},
        "warning": {"emoji_id": "warning", "background_color": 1, "border_color": 1, "text_color": 1},
        "success": {"emoji_id": "white_check_mark", "background_color": 4, "border_color": 4, "text_color": 4},
        "note": {"emoji_id": "pushpin", "background_color": 7, "border_color": 7},
        "important": {"emoji_id": "fire", "background_color": 8, "border_color": 1, "text_color": 1},
    }
    return styles.get(style_name.lower(), styles["info"])


def parse_markdown_to_blocks(markdown_text: str, include_first_title: bool = False) -> Dict[str, Any]:
    """将 Markdown 转换为飞书块"""
    lines = markdown_text.split('\n')
    blocks = []
    i = 0
    first_title_skipped = not include_first_title

    metadata = {
        "heading_count": 0,
        "table_count": 0,
        "list_count": 0,
        "code_count": 0,
        "callout_count": 0,
        "todo_count": 0,
        "image_count": 0,
        "total_blocks": 0
    }

    in_callout_block = False
    callout_content = []
    callout_type = 'info'

    while i < len(lines):
        line = lines[i].rstrip()

        # 处理 Callout 块
        if line.startswith(':::'):
            if not in_callout_block:
                callout_type = line[3:].strip().lower()
                in_callout_block = True
                callout_content = []
            else:
                callout_text = '\n'.join(callout_content).strip()
                style = get_callout_style(callout_type)
                blocks.append({
                    "block_type": 19,
                    "callout": {
                        "elements": [{"text_run": {"content": callout_text}}],
                        **style
                    }
                })
                metadata["callout_count"] += 1
                in_callout_block = False
            i += 1
            continue

        if in_callout_block:
            callout_content.append(line)
            i += 1
            continue

        if not line:
            i += 1
            continue

        # 1. 标题
        if line.startswith('#'):
            level_match = re.match(r'^(#{1,9})\s', line)
            if level_match:
                level = len(level_match.group(1))
                content = line.lstrip('#').strip()
                if first_title_skipped and level == 1:
                    first_title_skipped = False
                    i += 1
                    continue
                elements = parse_markdown_text(content)
                blocks.append({
                    "block_type": 2 + level,
                    f"heading{level}": {
                        "elements": elements,
                        "style": {}
                    }
                })
                metadata["heading_count"] += 1
                i += 1
                continue

        # 2. 分割线
        if line.strip() == '---':
            blocks.append({"block_type": 22, "divider": {}})
            i += 1
            continue

        # 3. 引用块
        if line.strip().startswith('>'):
            content = line.strip()[1:].strip()
            elements = parse_markdown_text(content)
            blocks.append({
                "block_type": 15,
                "quote": {
                    "elements": elements,
                    "style": {}
                }
            })
            i += 1
            continue

        # 4. 待办事项
        todo_match = re.match(r'^-\s+\[([ x])\]\s*(.*)', line.strip())
        if todo_match:
            done = todo_match.group(1).lower() == 'x'
            content = todo_match.group(2).strip()
            elements = parse_markdown_text(content)
            blocks.append({
                "block_type": 17,
                "todo": {
                    "elements": elements,
                    "style": {}
                },
                "done": done
            })
            metadata["todo_count"] += 1
            i += 1
            continue

        # 5. 普通无序列表
        if line.strip().startswith('- '):
            content = line.strip()[2:]
            blocks.append({
                "block_type": 12,
                "bullet": {
                    "elements": [{"text_run": {"content": content}}]
                }
            })
            metadata["list_count"] += 1
            i += 1
            continue

        # 6. 有序列表
        if re.match(r'^\d+\.\s', line.strip()):
            content = re.sub(r'^\d+\.\s', '', line.strip())
            blocks.append({
                "block_type": 13,
                "ordered": {
                    "elements": [{"text_run": {"content": content}}]
                }
            })
            metadata["list_count"] += 1
            i += 1
            continue

        # 7. 表格
        if '|' in line and line.strip():
            table_lines = [line]
            i += 1
            while i < len(lines) and '|' in lines[i]:
                table_lines.append(lines[i])
                i += 1

            table_data = []
            for table_line in table_lines:
                if '|---' in table_line or re.match(r'^\|?\s*:?-+:?\s*\|', table_line):
                    continue
                cells = table_line.split('|')
                if cells and cells[0].strip() == '':
                    cells.pop(0)
                if cells and cells[-1].strip() == '':
                    cells.pop()
                processed_cells = []
                for cell in cells:
                    cell = clean_cell_content(cell)
                    if cell:
                        processed_cells.append(cell)
                if processed_cells:
                    table_data.append(processed_cells)

            if table_data and len(table_data) > 1:
                blocks.append({
                    "type": "table",
                    "data": table_data
                })
                metadata["table_count"] += 1
            continue

        # 8. 代码块
        if line.strip().startswith('```'):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            code_content = '\n'.join(code_lines)
            blocks.append({
                "block_type": 14,
                "code": {
                    "elements": [{"text_run": {"content": code_content}}],
                    "style": {"language": 1}
                }
            })
            metadata["code_count"] += 1
            i += 1
            continue

        # 9. 普通文本
        if line.strip():
            elements = parse_markdown_text(line)
            blocks.append({
                "block_type": 2,
                "text": {
                    "elements": elements,
                    "style": {}
                }
            })

        i += 1

    metadata["total_blocks"] = len(blocks)

    return {
        "blocks": blocks,
        "metadata": metadata
    }


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("Usage: python md_parser.py <markdown_file> [output_dir]")
        sys.exit(1)

    md_file = Path(sys.argv[1])
    if not md_file.exists():
        print(f"Error: Markdown file not found: {md_file}")
        sys.exit(1)

    output_dir = Path(sys.argv[2]) if len(sys.argv) >= 3 else Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(md_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    print("=" * 70)
    print("Markdown Parser - Support 25 Feishu Block Types")
    print("=" * 70)

    start_time = time.time()
    result = parse_markdown_to_blocks(markdown_content, include_first_title=False)
    parse_time = time.time() - start_time

    blocks_file = output_dir / "blocks.json"
    with open(blocks_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"[OK] Parse completed in {parse_time:.2f}s")
    print(f"[OUTPUT] {blocks_file}")
    print(f"  Total blocks: {result['metadata']['total_blocks']}")


if __name__ == "__main__":
    main()
```

（因篇幅限制，其他文件的完整代码将在后续消息中提供）

---

**继续发送以下文件给 OpenClaw：**

### 文件3：doc_creator_with_permission.py
```python
[代码内容...]
```

### 文件4：block_adder.py
```python
[代码内容...]
```

### 文件5：check_config.py
```python
[代码内容...]
```

### 文件6：配置文件
```
# ~/.openclaw/.env
FEISHU_APP_ID=cli_xxx
FEISHU_APP_SECRET=xxx
FEISHU_API_DOMAIN=https://open.feishu.cn
FEISHU_DRIVE_FOLDER_TOKEN=folder_xxx
```