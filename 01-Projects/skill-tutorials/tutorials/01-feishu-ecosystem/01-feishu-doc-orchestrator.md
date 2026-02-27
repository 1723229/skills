# feishu-doc-orchestrator - 飞书文档创建编排技能

> 将 Markdown 文件转换为飞书文档，编排多个子技能协作完成，支持25种飞书文档块类型。

---

## 概述

### 功能简介

`feishu-doc-orchestrator` 是一个完整的飞书文档创建解决方案，通过编排多个子技能，实现从 Markdown 到飞书文档的自动化转换。该技能支持25种飞书文档块类型，包含完整的权限管理功能。

### 适用场景

- **知识沉淀**: 将 Markdown 笔记转换为飞书知识库文档
- **内容发布**: 自动化生成技术文档、产品文档
- **协作共享**: 一键创建带权限的共享文档
- **批量处理**: 大量 Markdown 文件的批量转换

### 依赖要求

- **Python版本**: 3.8+
- **依赖包**: requests, python-dotenv
- **外部服务**: 飞书开放平台 API

---

## 安装配置

### 环境要求

```bash
# 检查 Python 版本
python3 --version  # >= 3.8

# 检查 pip
pip3 --version
```

### 安装步骤

1. **复制技能文件**

```bash
cp -r skills/feishu-doc-orchestrator ~/.openclaw/workspace/skills/
```

2. **安装依赖**

```bash
pip3 install requests python-dotenv
```

3. **配置飞书应用**

方式一：使用配置脚本
```bash
python3 ~/.openclaw/workspace/skills/feishu-doc-orchestrator/scripts/setup_config.py
```

方式二：手动创建配置文件 `~/.openclaw/.claude/feishu-config.env`：

```ini
FEISHU_APP_ID=cli_xxxxxxxx
FEISHU_APP_SECRET=xxxxxxxx
FEISHU_AUTO_COLLABORATOR_ID=ou_xxx
FEISHU_DEFAULT_FOLDER=folder_xxx
```

4. **验证配置**

```bash
python3 ~/.openclaw/workspace/skills/feishu-doc-orchestrator/scripts/check_config.py
```

---

## 快速开始

### 最小可用示例

在 OpenClaw 对话中直接调用：
```
请帮我将 docs/example.md 转换为飞书文档
```

### 常用命令

```bash
# 测试所有25种块类型
python3 scripts/test_all_25_blocks.py

# 创建简单文档
python3 scripts/create_simple.py
```

---

## 详细用法

### 支持的25种块类型

| 类别 | 块类型 |
|------|--------|
| 基础文本 | text, heading1-9, quote_container |
| 列表 | bullet, ordered, todo, task |
| 特殊块 | code, quote, callout, divider, image |
| AI块 | ai_template |
| 高级块 | bitable, grid, sheet, table, board |

### 技能架构

```
feishu-doc-orchestrator/        # 主技能
├── feishu-md-parser/           # Markdown解析
├── feishu-doc-creator-with-permission/  # 创建+权限
├── feishu-block-adder/         # 批量添加
├── feishu-doc-verifier/        # 文档验证
└── feishu-logger/              # 日志记录
```

---

## 示例代码

### 基础示例

```python
from skills.feishu_doc_orchestrator.scripts.orchestrator import create_doc_from_markdown

result = create_doc_from_markdown(
    markdown_path="docs/guide.md",
    title="用户指南",
    folder_token="folder_xxx"
)

print(f"文档已创建: {result['doc_url']}")
```

### 完整工作流

```python
import glob

for md_file in glob.glob("docs/*.md"):
    result = create_doc_from_markdown(
        markdown_path=md_file,
        title=md_file.replace(".md", ""),
        folder_token="folder_xxx"
    )
```

---

## 故障排除

| 错误码 | 含义 | 解决方案 |
|--------|------|----------|
| 10003 | 应用未授权 | 在飞书开放平台启用权限 |
| 230002 | 无权限访问 | 确认应用有文档操作权限 |

---

## 参考链接

- **源码路径**: `skills/feishu-doc-orchestrator/`
- **SKILL.md**: `skills/feishu-doc-orchestrator/SKILL.md`
- **相关技能**: feishu-wiki-orchestrator

---

*文档生成时间: 2026-02-27*
