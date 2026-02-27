# feishu-doc-orchestrator - 飞书文档创建编排技能（深度教程）

> 将 Markdown 文件转换为飞书文档的完整解决方案，通过编排5个子技能协作完成，支持25种飞书文档块类型，包含完整的权限管理和验证机制。

---

## 一、概述

### 1.1 功能简介

**feishu-doc-orchestrator** 是一个企业级的 Markdown 到飞书文档转换解决方案。与简单的文件上传工具不同，它采用**编排模式**（Orchestration Pattern），将文档创建流程分解为5个独立的子技能，通过文件传递数据，实现：

- **高可靠性**：每个步骤独立执行，失败可单独重试
- **可观测性**：每个步骤都有明确的输入输出和日志
- **可扩展性**：子技能可独立升级替换，不影响整体流程
- **权限完整性**：创建文档的同时自动配置权限，无需后续手动操作

**核心技术原理**：
1. 使用 **AST（抽象语法树）** 解析 Markdown，而非简单的正则替换
2. 通过 **子进程编排** 实现技能解耦，每个子技能可独立测试
3. 采用 **文件传递** 替代内存传递，支持大文件处理且可审计
4. 内置 **权限原子操作**，确保文档创建和权限配置的一致性

### 1.2 适用场景

| 场景 | 具体示例 | 解决的问题 |
|------|----------|------------|
| **知识库建设** | 将项目 Wiki 从 Markdown 迁移到飞书知识库 | 格式转换、权限批量设置、版本追溯 |
| **自动化文档** | CI/CD 流程自动生成 API 文档到飞书 | 零人工干预、格式统一、即时同步 |
| **内容发布** | 将博客文章批量发布到飞书 | 保留格式、图片迁移、权限管理 |
| **团队协作** | 技术方案评审文档共享 | 精细化权限控制、评论协作、版本管理 |

### 1.3 不适用场景

- **实时协作编辑**：飞书文档本身支持更好，此技能专注于**初始化创建**
- **超大规模文档**（>10MB）：建议拆分或直接使用飞书 API
- **复杂交互式文档**：不支持 JavaScript、嵌入式应用等动态内容

### 1.4 依赖要求

| 依赖项 | 版本/要求 | 获取方式 | 必要性 |
|--------|-----------|----------|--------|
| Python | >= 3.8 | [官网](https://python.org) | 必需 |
| requests | >= 2.25.0 | `pip install requests` | 必需 |
| python-dotenv | >= 0.19.0 | `pip install python-dotenv` | 必需 |
| 飞书应用 | 企业自建应用 | [开放平台](https://open.feishu.cn) | 必需 |
| 云盘文件夹 | folder_token | 飞书云盘 → 文件夹 → 分享 | 必需 |

---

## 二、安装配置

### 2.1 环境检查

**步骤1：检查 Python 版本**

```bash
$ python3 --version
Python 3.9.7  # 输出需 >= 3.8
```

**如果版本过低**，升级方法：
- **macOS**: `brew install python@3.9`
- **Ubuntu**: `sudo apt update && sudo apt install python3.9`
- **Windows**: 从 [python.org](https://python.org) 下载安装

**步骤2：检查 pip 版本**

```bash
$ pip3 --version
pip 21.0.1 from .../python3.9/site-packages/pip (python 3.9)
```

如果 pip 不可用，安装方法：
```bash
$ python3 -m ensurepip --upgrade
```

### 2.2 安装技能

**步骤1：复制技能文件**

```bash
# 创建技能目录
$ mkdir -p ~/.openclaw/workspace/skills/

# 复制主技能及所有子技能
cp -r skills/feishu-doc-orchestrator \
      ~/.openclaw/workspace/skills/

# 验证复制成功
$ ls ~/.openclaw/workspace/skills/feishu-doc-orchestrator/
feishu-md-parser/                    # 子技能1：Markdown解析
feishu-doc-creator-with-permission/  # 子技能2：创建+权限
feishu-block-adder/                  # 子技能3：块添加
feishu-doc-verifier/                 # 子技能4：验证
feishu-logger/                       # 子技能5：日志
SKILL.md
```

**步骤2：安装 Python 依赖**

```bash
$ pip3 install requests python-dotenv

# 验证安装
$ python3 -c "import requests; print(requests.__version__)"
2.28.1

$ python3 -c "import dotenv; print('dotenv OK')"
dotenv OK
```

**常见问题**：如果提示 `ModuleNotFoundError`，说明 pip 安装的包不在 PYTHONPATH 中：

```bash
# 检查 Python 和 pip 是否匹配
$ which python3
/usr/local/bin/python3

$ which pip3
/usr/local/bin/pip3

# 如果不一致，使用 python -m pip
$ python3 -m pip install requests python-dotenv
```

### 2.3 飞书应用配置

**步骤1：创建飞书应用**

1. 访问 [飞书开放平台](https://open.feishu.cn/app)
2. 点击「创建企业自建应用」
3. 填写应用信息：
   - **应用名称**：`文档助手`（可自定义）
   - **应用描述**：`Markdown 转飞书文档`
4. 记录 **App ID** 和 **App Secret**（后面会用到）

**步骤2：开启权限**

进入应用详情页 →「权限管理」，开启以下权限：

| 权限 | 权限代码 | 用途 |
|------|----------|------|
| 创建文档 | `docx:document:create` | 创建云盘文档 |
| 编辑文档 | `docx:document:write` | 添加文档内容 |
| 读取文档 | `docx:document:read` | 验证文档创建 |
| 管理协作者 | `docx:document:permission:member:manage` | 添加协作者 |
| 转移所有权 | `docx:document:permission:transfer` | 转移文档所有权 |
| 读取云盘 | `drive:drive:read` | 获取文件夹信息 |

**步骤3：发布应用**

进入「版本管理与发布」→「创建版本」：
- 版本号：1.0.0
- 更新说明：初始版本
- 点击「申请发布」

如果是企业管理员，直接通过；否则需要管理员审批。

**步骤4：获取云盘文件夹 Token**

1. 打开 [飞书云盘](https://drive.feishu.cn)
2. 创建或选择一个文件夹
3. 右键 →「分享」→「复制链接」
4. 从链接中提取 `folder_token`：
   ```
   https://drive.feishu.cn/file/folder/DYPXf8ZktlOCIXdmGq3cfjevn2F
                                        └────────────────────────── folder_token
   ```

### 2.4 配置文件详解

**创建配置文件**：

```bash
$ mkdir -p ~/.openclaw/.claude
$ cat > ~/.openclaw/.claude/feishu-config.env << 'EOF'
# =====================================
# 飞书文档创建技能配置
# =====================================

# 飞书开放平台 - 应用凭证（从应用详情页获取）
FEISHU_APP_ID=cli_xxxxxxxxxxxxxxxx
FEISHU_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 飞书 API 域名（国内版不需要改）
FEISHU_API_DOMAIN=https://open.feishu.cn

# 云盘文件夹 Token（文档将创建在此文件夹）
FEISHU_DRIVE_FOLDER_TOKEN=DYPXf8ZktlOCIXdmGq3cfjevn2F

# 可选：自动添加协作者（用户 Open ID）
# FEISHU_AUTO_COLLABORATOR_ID=ou_xxxxxxxxxxxxxxxx

# 可选：自动转移所有权给指定用户
# FEISHU_AUTO_TRANSFER_OWNER_ID=ou_xxxxxxxxxxxxxxxx
EOF
```

**配置项说明**：

| 配置项 | 必填 | 获取方式 | 说明 |
|--------|------|----------|------|
| `FEISHU_APP_ID` | ✓ | 应用详情页 → 凭证 | 应用唯一标识 |
| `FEISHU_APP_SECRET` | ✓ | 应用详情页 → 凭证 | 应用密钥，勿泄露 |
| `FEISHU_API_DOMAIN` | ✗ | 固定值 | 国内版用默认，国际版改 `open.larksuite.com` |
| `FEISHU_DRIVE_FOLDER_TOKEN` | ✓ | 云盘文件夹链接 | 文档创建位置 |
| `FEISHU_AUTO_COLLABORATOR_ID` | ✗ | 用户详情页 → Open ID | 自动添加的协作者 |
| `FEISHU_AUTO_TRANSFER_OWNER_ID` | ✗ | 用户详情页 → Open ID | 转移所有权的目标用户 |

**获取用户 Open ID**：
1. 飞书管理后台 → 组织架构 → 用户详情
2. 或飞书客户端 → 用户资料 → 点击头像获取链接中的 `ou_xxx`

### 2.5 验证配置

**步骤1：运行配置检查脚本**

```bash
$ cd ~/.openclaw/workspace/skills/feishu-doc-orchestrator
$ python3 feishu-doc-orchestrator/scripts/check_config.py

========================================
飞书文档创建技能 - 配置检查
========================================
✓ 配置文件存在: /Users/xxx/.openclaw/.claude/feishu-config.env
✓ FEISHU_APP_ID: cli_xxx... (长度正确)
✓ FEISHU_APP_SECRET: 已设置 (长度正确)
✓ 获取 tenant_access_token: 成功
✓ 飞书 API 连接: 正常

========================================
配置检查通过！可以开始使用。
========================================
```

**步骤2：测试创建简单文档**

```bash
$ python3 feishu-doc-orchestrator/scripts/create_simple.py

========================================
飞书文档创建 - 简单测试
========================================
文档标题: 测试文档-2026-02-27
✓ 文档创建成功！
📄 文档链接: https://xxx.feishu.cn/docx/xxxxxxxx

权限状态:
  协作者添加: [OK]
  所有权转移: [跳过]

========================================
```

**常见问题**：

| 错误信息 | 原因 | 解决方案 |
|----------|------|----------|
| "Config file not found" | 配置文件路径错误 | 检查 `~/.openclaw/.claude/feishu-config.env` 是否存在 |
| "Failed to get token" | App ID/Secret 错误 | 确认凭证正确，应用已发布 |
| "Permission denied" | 权限未开启 | 检查应用权限设置，确保开启了 docx:document:create 等权限 |
| "Folder not found" | folder_token 错误 | 确认文件夹存在，token 正确 |

---

## 三、核心概念

### 3.1 编排架构

```
┌─────────────────────────────────────────────────────────────┐
│                    Orchestrator (主技能)                     │
│                     协调5个子技能协作                          │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐   ┌──────────────────┐   ┌──────────────┐
│ Step 1       │   │ Step 2           │   │ Step 3       │
│ Markdown     │──▶│ 创建文档+权限     │──▶│ 添加内容块    │
│ 解析         │   │ (原子操作)       │   │              │
└──────────────┘   └──────────────────┘   └──────────────┘
                                                        │
                              ┌─────────────────────────┘
                              │
                              ▼
                  ┌──────────────────┐
                  │ Step 4           │
                  │ 文档验证         │
                  │ (Playwright)     │
                  └──────────────────┘
                              │
                              ▼
                  ┌──────────────────┐
                  │ Step 5           │
                  │ 日志记录         │
                  │ (Markdown+JSON)  │
                  └──────────────────┘
```

**设计原理**：
- **关注点分离**：每个子技能只负责一件事
- **失败隔离**：单个步骤失败不影响其他步骤重试
- **数据持久化**：中间结果保存到文件，可审计调试
- **无状态编排**：Orchestrator 不持有状态，通过文件传递

### 3.2 支持的25种块类型

**分类详解**：

| 类别 | 数量 | 块类型 | 示例 |
|------|------|--------|------|
| **文本** | 11 | text, heading1-9, quote_container | `# 标题`, `> 引用` |
| **列表** | 4 | bullet, ordered, todo, task | `- 项`, `1. 项`, `- [ ] 待办` |
| **特殊** | 5 | code, quote, callout, divider, image | ` ```code`, `::: tip`, `---` |
| **AI** | 1 | ai_template | 飞书AI模板块 |
| **高级** | 4 | table, bitable, grid, sheet | `| 表头 | 表头 |` |

**不支持的内容**：
- HTML 标签（会被转义）
- 复杂嵌套表格
- 数学公式（LaTeX）
- 视频嵌入

### 3.3 工作流程文件

执行后生成的文件结构：

```
workflow/
├── step1_parse/
│   ├── blocks.json           # 解析后的块数据
│   └── metadata.json         # Markdown元数据
├── step2_create_with_permission/
│   └── doc_with_permission.json  # 文档信息+权限状态
├── step3_add_blocks/
│   └── add_result.json       # 块添加结果统计
└── step4_verify/
    ├── verify_result.json    # 验证结果
    └── screenshot.png        # 文档截图

CREATED_DOCS.md               # 日志（人类可读）
created_docs.json            # 日志（机器可读）
```

---

## 四、快速开始

### 4.1 最小可用示例

**步骤1：准备 Markdown 文件**

```bash
$ cat > /tmp/demo.md << 'EOF'
# 项目简介

欢迎使用我们的项目！

## 功能特性

- ✨ **高性能**: 基于 Rust 核心，极致性能
- 🔒 **安全**: 企业级权限控制
- 📦 **易用**: 一行命令即可部署

## 快速开始

```bash
npm install my-project
npm run dev
```

## 配置说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| port | number | 3000 | 服务端口 |
| host | string | localhost | 绑定地址 |

::: tip 提示
生产环境建议修改默认配置，提高安全性。
:::
EOF
```

**步骤2：执行转换**

```bash
$ cd ~/.openclaw/workspace/skills/feishu-doc-orchestrator
$ python3 feishu-doc-orchestrator/scripts/orchestrator.py \
    /tmp/demo.md \
    "项目文档"

======================================================================
Feishu Document Creation - Orchestrator Workflow (5 Steps)
======================================================================
输入文件: /tmp/demo.md
文档标题: 项目文档
工作流目录: workflow
输出目录: /Users/xxx/.openclaw/workspace/skills/feishu-doc-orchestrator

======================================================================
[步骤] 第一步：Markdown 解析
======================================================================
命令: .../md_parser.py /tmp/demo.md workflow/step1_parse
✓ 解析成功！
   块数量: 8
   类型分布: heading1(1), text(2), bullet(3), code(1), table(1), callout(1)

======================================================================
[步骤] 第二步：文档创建+权限管理（原子操作）
======================================================================
✓ 文档创建成功！
   Document URL: https://xxx.feishu.cn/docx/Okbxd...
   Document Token: Okbxd...

[权限状态]
  协作者添加: True
  所有权转移: False
  用户完全控制: True

======================================================================
[步骤] 第三步：块添加
======================================================================
✓ 块添加完成
   成功: 8/8
   失败: 0

======================================================================
[步骤] 第四步：文档验证
======================================================================
✓ 文档验证通过
   可访问性: OK
   内容完整性: OK

======================================================================
[步骤] 第五步：日志记录
======================================================================
✓ 日志记录完成

======================================================================
文档创建完成！
======================================================================
文档 URL: https://xxx.feishu.cn/docx/Okbxd...
耗时: 3.45 秒
```

**步骤3：验证结果**

1. 点击输出的文档 URL
2. 检查内容是否完整（标题、列表、代码块、表格、提示框）
3. 检查权限设置（协作者是否正确添加）

### 4.2 命令行参数

```bash
python3 orchestrator.py <markdown文件> [文档标题] [工作流目录]

参数说明:
  markdown文件   必需  要转换的 Markdown 文件路径
  文档标题       可选  默认为文件名（不含扩展名）
  工作流目录     可选  默认为 workflow/

示例:
  python3 orchestrator.py docs/api.md "API文档"
  python3 orchestrator.py report.md "周报" /tmp/workflow
```

---

## 五、详细用法

### 5.1 Orchestrator 主程序

**文件路径**: `feishu-doc-orchestrator/scripts/orchestrator.py`

**核心函数**: `main()`

**完整调用流程**:

```python
import subprocess
from pathlib import Path

# 定义子技能路径
SCRIPT_DIR = Path("~/.openclaw/workspace/skills/feishu-doc-orchestrator")
SUB_SKILLS = {
    "parser": SCRIPT_DIR / "feishu-md-parser/scripts/md_parser.py",
    "creator": SCRIPT_DIR / "feishu-doc-creator-with-permission/scripts/doc_creator_with_permission.py",
    "block_adder": SCRIPT_DIR / "feishu-block-adder/scripts/block_adder.py",
    "verifier": SCRIPT_DIR / "feishu-doc-verifier/scripts/doc_verifier.py",
    "logger": SCRIPT_DIR / "feishu-logger/scripts/logger.py"
}

# 执行完整工作流
cmd = [
    "python3", str(SUB_SKILLS["parser"]),
    "input.md", "workflow/step1_parse"
]
result = subprocess.run(cmd, capture_output=True, text=True)
```

**输入参数**:

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `markdown_file` | str | ✓ | - | Markdown 文件路径 |
| `doc_title` | str | ✗ | 文件名 | 飞书文档标题 |
| `workflow_dir` | str | ✗ | "workflow" | 工作流中间文件目录 |

**输出结果**:

```json
{
  "document_url": "https://xxx.feishu.cn/docx/Okbxd...",
  "document_token": "Okbxd...",
  "block_count": 8,
  "duration_seconds": 3.45,
  "permission_status": {
    "collaborator_added": true,
    "owner_transferred": false,
    "user_has_full_control": true
  }
}
```

### 5.2 子技能详解

#### 5.2.1 Markdown 解析器 (feishu-md-parser)

**功能**: 将 Markdown 文件解析为飞书块格式

**输入**: Markdown 文件路径、输出目录

**输出**: `blocks.json`（块数据）、`metadata.json`（元数据）

**支持的 Markdown 语法**:

| Markdown | 飞书块类型 | 说明 |
|----------|-----------|------|
| `# 标题` | heading1-9 | 1-9级标题 |
| `**粗体**` | text + bold样式 | 自动解析内联样式 |
| `- 列表项` | bullet | 无序列表 |
| `1. 列表项` | ordered | 有序列表 |
| `- [ ] 待办` | todo | 待办列表 |
| ` ```code` | code | 代码块 |
| `> 引用` | quote_container | 引用容器 |
| `::: tip` | callout | 提示框（支持info/tip/warning/success/note） |
| `---` | divider | 分割线 |
| `| 表头 |` | table | 表格（支持表头、对齐） |
| `![alt](url)` | image | 图片（需可访问的URL） |

**Callout 样式映射**:

```markdown
::: info    → 蓝色信息框 (information_source)
::: tip     → 黄色提示框 (bulb)
::: warning → 红色警告框 (warning)
::: success → 绿色成功框 (white_check_mark)
::: note    → 灰色备注框 (pushpin)
```

#### 5.2.2 文档创建+权限管理 (feishu-doc-creator-with-permission)

**功能**: 创建飞书文档并配置权限（原子操作）

**核心 API 调用**:

```python
# 1. 创建文档
POST /open-apis/docx/v1/documents
{
  "title": "文档标题",
  "folder_token": "DYPXf8ZktlOCIXdmGq3cfjevn2F"
}

# 2. 添加协作者（可选）
POST /open-apis/docx/v1/documents/{document_id}/permissions/members
{
  "member_type": "openid",
  "member_id": "ou_xxx",
  "perm": "edit"
}

# 3. 转移所有权（可选）
POST /open-apis/docx/v1/documents/{document_id}/permissions/owner_transfer
{
  "owner_type": "openid",
  "owner_id": "ou_xxx"
}
```

**权限配置逻辑**:

1. 读取 `FEISHU_AUTO_COLLABORATOR_ID`，不为空则添加协作者
2. 读取 `FEISHU_AUTO_TRANSFER_OWNER_ID`，不为空则转移所有权
3. 协作者和所有权转移独立配置，可同时启用

#### 5.2.3 块添加器 (feishu-block-adder)

**功能**: 将解析后的块批量添加到飞书文档

**批量添加策略**:

- **普通块**（text, heading, bullet等）：批量添加，每批最多50个
- **表格块**（table）：单独处理，先创建表格结构再填充单元格
- **图片块**（image）：单独处理，支持 base64 和 URL 两种方式

**API 限制处理**:

```python
# 飞书 API 限制：每请求最多 50 个块
MAX_BLOCKS_PER_REQUEST = 50

# 超过限制时分批处理
blocks_batches = [
    all_blocks[i:i+MAX_BLOCKS_PER_REQUEST]
    for i in range(0, len(all_blocks), MAX_BLOCKS_PER_REQUEST)
]
```

**错误处理**:
- 单个块添加失败不影响其他块
- 失败块记录到 `add_result.json` 的 `failed_blocks` 列表
- 支持重试机制（指数退避）

#### 5.2.4 文档验证器 (feishu-doc-verifier)

**功能**: 验证文档可访问性和内容完整性

**验证项**:

| 验证项 | 方法 | 预期结果 |
|--------|------|----------|
| 文档可访问性 | HTTP HEAD 请求 | 返回 200 |
| 内容完整性 | 比对块数量 | 添加数 = 解析数 |
| 权限验证 | 检查协作者列表 | 配置的用户在列表中 |
| 截图验证 | Playwright（可选） | 生成文档截图 |

#### 5.2.5 日志记录器 (feishu-logger)

**功能**: 记录创建结果到日志文件

**输出文件**:

1. **CREATED_DOCS.md** - 人类可读的 Markdown 日志
2. **created_docs.json** - 机器可读的 JSON 日志

**日志内容**:
- 文档标题和 URL
- 创建时间
- 耗时统计
- 权限状态
- 块数量统计

---

## 六、示例代码

### 6.1 基础示例：单文档转换

```python
#!/usr/bin/env python3
"""
基础示例：将单个 Markdown 文件转换为飞书文档
"""
import subprocess
from pathlib import Path

def convert_single_document(md_path: str, title: str) -> str:
    """
    转换单个 Markdown 文件到飞书文档
    
    Args:
        md_path: Markdown 文件路径
        title: 文档标题
    
    Returns:
        飞书文档 URL
    """
    # 主技能路径
    orchestrator = Path.home() / ".openclaw/workspace/skills/feishu-doc-orchestrator"
    script = orchestrator / "feishu-doc-orchestrator/scripts/orchestrator.py"
    
    # 执行转换
    cmd = ["python3", str(script), md_path, title]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"转换失败: {result.stderr}")
    
    # 从输出中提取文档 URL
    for line in result.stdout.split("\n"):
        if "文档 URL:" in line:
            return line.split("文档 URL:")[1].strip()
    
    raise Exception("无法获取文档 URL")

# 使用示例
if __name__ == "__main__":
    try:
        url = convert_single_document(
            md_path="/tmp/demo.md",
            title="测试文档"
        )
        print(f"✅ 转换成功: {url}")
    except Exception as e:
        print(f"❌ 转换失败: {e}")
```

### 6.2 进阶示例：批量转换带进度

```python
#!/usr/bin/env python3
"""
进阶示例：批量转换 Markdown 文件，显示进度和统计
"""
import subprocess
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict

def batch_convert(
    md_files: List[str],
    output_dir: str = "batch_output"
) -> Dict:
    """
    批量转换 Markdown 文件
    
    Args:
        md_files: Markdown 文件路径列表
        output_dir: 输出目录
    
    Returns:
        转换统计信息
    """
    orchestrator = Path.home() / ".openclaw/workspace/skills/feishu-doc-orchestrator"
    script = orchestrator / "feishu-doc-orchestrator/scripts/orchestrator.py"
    
    results = {
        "total": len(md_files),
        "success": 0,
        "failed": 0,
        "documents": [],
        "start_time": datetime.now().isoformat()
    }
    
    for i, md_file in enumerate(md_files, 1):
        print(f"\n[{i}/{len(md_files)}] 处理: {md_file}")
        
        # 使用文件名作为标题
        title = Path(md_file).stem
        workflow_dir = f"{output_dir}/workflow_{i}"
        
        cmd = [
            "python3", str(script),
            md_file, title, workflow_dir
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            # 提取文档 URL
            doc_url = None
            for line in result.stdout.split("\n"):
                if "文档 URL:" in line:
                    doc_url = line.split("文档 URL:")[1].strip()
                    break
            
            results["documents"].append({
                "file": md_file,
                "title": title,
                "url": doc_url,
                "status": "success"
            })
            results["success"] += 1
            print(f"  ✅ 成功: {doc_url}")
        else:
            results["documents"].append({
                "file": md_file,
                "title": title,
                "error": result.stderr,
                "status": "failed"
            })
            results["failed"] += 1
            print(f"  ❌ 失败: {result.stderr[:100]}")
    
    results["end_time"] = datetime.now().isoformat()
    
    # 保存结果到文件
    with open(f"{output_dir}/batch_result.json", "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    return results

# 使用示例
if __name__ == "__main__":
    import glob
    
    # 获取所有 Markdown 文件
    md_files = glob.glob("docs/*.md")
    
    if not md_files:
        print("未找到 Markdown 文件")
    else:
        results = batch_convert(md_files)
        print(f"\n{'='*50}")
        print(f"批量转换完成")
        print(f"总计: {results['total']}")
        print(f"成功: {results['success']}")
        print(f"失败: {results['failed']}")
        print(f"结果已保存到: batch_output/batch_result.json")
```

### 6.3 完整工作流：CI/CD 集成

```python
#!/usr/bin/env python3
"""
完整工作流：CI/CD 自动化文档发布
适用于：GitLab CI / GitHub Actions / Jenkins
"""
import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

class FeishuDocPublisher:
    """飞书文档发布器 - 生产级实现"""
    
    def __init__(self):
        self.orchestrator = Path.home() / ".openclaw/workspace/skills/feishu-doc-orchestrator"
        self.script = self.orchestrator / "feishu-doc-orchestrator/scripts/orchestrator.py"
        self.check_config = self.orchestrator / "feishu-doc-orchestrator/scripts/check_config.py"
        
    def validate_environment(self) -> bool:
        """验证环境配置"""
        print("[1/4] 验证环境配置...")
        
        # 检查必需的环境变量
        required_vars = ["FEISHU_APP_ID", "FEISHU_APP_SECRET"]
        for var in required_vars:
            if not os.getenv(var):
                print(f"  ❌ 缺少环境变量: {var}")
                return False
        
        # 运行配置检查
        result = subprocess.run(
            ["python3", str(self.check_config)],
            capture_output=True, text=True
        )
        
        if result.returncode != 0:
            print(f"  ❌ 配置检查失败: {result.stderr}")
            return False
        
        print("  ✅ 环境配置验证通过")
        return True
    
    def publish_document(
        self,
        md_path: str,
        title: str,
        folder_token: str = None
    ) -> dict:
        """
        发布文档到飞书
        
        Args:
            md_path: Markdown 文件路径
            title: 文档标题
            folder_token: 可选，覆盖默认文件夹
        
        Returns:
            发布结果字典
        """
        print(f"[2/4] 发布文档: {title}")
        
        # 如果指定了 folder_token，临时修改配置
        if folder_token:
            self._set_folder_token(folder_token)
        
        try:
            cmd = ["python3", str(self.script), md_path, title]
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=120
            )
            
            if result.returncode != 0:
                return {
                    "success": False,
                    "error": result.stderr,
                    "stdout": result.stdout
                }
            
            # 解析输出
            doc_url = None
            duration = None
            for line in result.stdout.split("\n"):
                if "文档 URL:" in line:
                    doc_url = line.split("文档 URL:")[1].strip()
                if "耗时:" in line:
                    duration = line.split("耗时:")[1].strip()
            
            return {
                "success": True,
                "title": title,
                "url": doc_url,
                "duration": duration,
                "timestamp": datetime.now().isoformat()
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "转换超时（超过120秒）"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
        finally:
            # 恢复默认配置
            if folder_token:
                self._restore_folder_token()
    
    def _set_folder_token(self, token: str):
        """临时设置文件夹 token"""
        config_path = Path.home() / ".openclaw/.claude/feishu-config.env"
        self._original_config = config_path.read_text()
        
        new_config = self._original_config.replace(
            f"FEISHU_DRIVE_FOLDER_TOKEN=",
            f"FEISHU_DRIVE_FOLDER_TOKEN={token}  # TEMP"
        )
        config_path.write_text(new_config)
    
    def _restore_folder_token(self):
        """恢复原始配置"""
        config_path = Path.home() / ".openclaw/.claude/feishu-config.env"
        if hasattr(self, '_original_config'):
            config_path.write_text(self._original_config)
    
    def notify_team(self, result: dict, webhook_url: str = None):
        """通知团队（可选）"""
        if not webhook_url:
            return
        
        print("[3/4] 发送通知...")
        
        import requests
        
        if result["success"]:
            message = {
                "msg_type": "text",
                "content": {
                    "text": f"✅ 文档发布成功\n标题: {result['title']}\n链接: {result['url']}"
                }
            }
        else:
            message = {
                "msg_type": "text",
                "content": {
                    "text": f"❌ 文档发布失败\n标题: {result.get('title', 'Unknown')}\n错误: {result.get('error', 'Unknown error')}"
                }
            }
        
        try:
            requests.post(webhook_url, json=message, timeout=10)
            print("  ✅ 通知已发送")
        except Exception as e:
            print(f"  ⚠️ 通知发送失败: {e}")
    
    def save_report(self, result: dict, output_path: str = "publish_report.json"):
        """保存发布报告"""
        print("[4/4] 保存报告...")
        
        with open(output_path, "w") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"  ✅ 报告已保存: {output_path}")


def main():
    """主函数 - CI/CD 入口点"""
    # 从环境变量或命令行参数获取配置
    md_path = os.getenv("INPUT_MD_PATH") or sys.argv[1] if len(sys.argv) > 1 else None
    title = os.getenv("INPUT_TITLE") or sys.argv[2] if len(sys.argv) > 2 else None
    webhook = os.getenv("FEISHU_WEBHOOK_URL")
    
    if not md_path or not title:
        print("用法: python publish.py <md_path> <title>")
        print("或设置环境变量: INPUT_MD_PATH, INPUT_TITLE")
        sys.exit(1)
    
    # 创建发布器实例
    publisher = FeishuDocPublisher()
    
    # 验证环境
    if not publisher.validate_environment():
        sys.exit(1)
    
    # 发布文档
    result = publisher.publish_document(md_path, title)
    
    # 通知团队
    publisher.notify_team(result, webhook)
    
    # 保存报告
    publisher.save_report(result)
    
    # 输出结果供后续步骤使用
    if result["success"]:
        print(f"\n{'='*50}")
        print(f"✅ 发布成功")
        print(f"文档 URL: {result['url']}")
        print(f"{'='*50}")
        
        # GitHub Actions 输出
        if os.getenv("GITHUB_ACTIONS"):
            print(f"::set-output name=doc_url::{result['url']}")
        
        sys.exit(0)
    else:
        print(f"\n{'='*50}")
        print(f"❌ 发布失败")
        print(f"错误: {result['error']}")
        print(f"{'='*50}")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

**GitHub Actions 集成示例**:

```yaml
# .github/workflows/publish-docs.yml
name: Publish Docs to Feishu

on:
  push:
    branches: [ main ]
    paths:
      - 'docs/**'

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: pip install requests python-dotenv
      
      - name: Setup Feishu Config
        run: |
          mkdir -p ~/.openclaw/.claude
          cat > ~/.openclaw/.claude/feishu-config.env << EOF
          FEISHU_APP_ID=${{ secrets.FEISHU_APP_ID }}
          FEISHU_APP_SECRET=${{ secrets.FEISHU_APP_SECRET }}
          FEISHU_DRIVE_FOLDER_TOKEN=${{ secrets.FEISHU_FOLDER_TOKEN }}
          EOF
      
      - name: Publish to Feishu
        env:
          INPUT_MD_PATH: docs/api.md
          INPUT_TITLE: "API文档-${{ github.sha }}"
          FEISHU_WEBHOOK_URL: ${{ secrets.FEISHU_WEBHOOK }}
        run: python scripts/publish.py
```

---

## 七、最佳实践

### 7.1 性能优化

**1. 批量处理优化**

- 大量文档转换时，使用并行处理：

```python
from concurrent.futures import ProcessPoolExecutor

def convert_batch_parallel(md_files, max_workers=4):
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(convert_single, f) for f in md_files]
        results = [f.result() for f in futures]
    return results
```

**2. 图片优化**

- 使用飞书云盘托管图片，获取 `file_token`
- 避免使用外部 URL（可能因网络问题加载失败）
- 大图片先压缩再嵌入

**3. 工作流目录清理**

```bash
# 定期清理历史工作流文件
find workflow/ -type d -mtime +7 -exec rm -rf {} \;
```

### 7.2 安全注意事项

**1. 配置安全**

- ✅ 将 `feishu-config.env` 添加到 `.gitignore`
- ✅ 使用环境变量注入敏感信息（CI/CD场景）
- ❌ 不要将 App Secret 硬编码到代码中
- ❌ 不要将配置文件提交到公共仓库

**2. 权限最小化**

- 飞书应用只开启必需的权限
- 协作者只授予必要的权限（read/edit）
- 定期审计文档权限

**3. Token 轮换**

```bash
# 建议每 90 天轮换一次 App Secret
# 在飞书开放平台 → 应用详情 → 凭证管理 → 重置 Secret
```

### 7.3 与其他技能组合

**组合1：自动知识库更新**

```
Git 提交 → 触发 webhook → feishu-doc-orchestrator 创建文档 
→ feishu-wiki-orchestrator 移动到知识库 → 发送通知
```

**组合2：周报自动生成**

```
calendar 获取本周会议 → feishu-chat-extractor 提取讨论要点
→ long-form-writer 生成周报 → feishu-doc-orchestrator 创建文档
→ 发送到指定群组
```

---

## 八、故障排除

### 8.1 安装问题

**问题**: `ModuleNotFoundError: No module named 'requests'`

**诊断**:
```bash
# 检查 Python 和 pip 是否匹配
which python3
which pip3

# 查看 requests 安装位置
python3 -c "import requests; print(requests.__file__)"
```

**解决**:
```bash
# 方法1：使用 python -m pip
python3 -m pip install requests

# 方法2：重新安装 pip
python3 -m ensurepip --upgrade

# 方法3：使用虚拟环境
python3 -m venv venv
source venv/bin/activate
pip install requests python-dotenv
```

### 8.2 配置问题

**问题**: `Failed to get tenant_access_token`

**诊断**:
```bash
# 检查配置文件
ls -la ~/.openclaw/.claude/feishu-config.env

# 验证配置格式
cat ~/.openclaw/.claude/feishu-config.env | grep -E "^(FEISHU_APP_ID|FEISHU_APP_SECRET)="
```

**可能原因与解决**:

| 原因 | 检查方法 | 解决方案 |
|------|----------|----------|
| App ID 错误 | 长度应为 18 字符 | 从开放平台重新复制 |
| App Secret 错误 | 包含大小写字母和数字 | 重置 Secret 后更新配置 |
| 应用未发布 | 开放平台 → 版本管理 | 创建版本并申请发布 |
| 网络问题 | `curl https://open.feishu.cn` | 检查网络连接 |

### 8.3 运行时问题

**问题**: `Permission denied when creating document`

**诊断步骤**:
1. 检查应用权限：开放平台 → 权限管理
2. 确认开启了 `docx:document:create`
3. 检查 folder_token 是否正确
4. 确认应用有权限访问该文件夹

**问题**: `部分块添加失败`

**诊断**:
```bash
# 查看详细错误
cat workflow/step3_add_blocks/add_result.json

# 常见原因：
# 1. 表格行列不匹配
# 2. 图片 URL 不可访问
# 3. 块类型不支持
```

**问题**: `文档创建成功但无法访问`

**可能原因**:
1. 权限配置未生效 → 检查 `FEISHU_AUTO_COLLABORATOR_ID` 是否正确
2. 协作者不在同一企业 → 确认用户 Open ID 正确
3. 文档被移动到回收站 → 检查操作日志

### 8.4 调试技巧

**1. 开启详细日志**

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

**2. 检查中间文件**

```bash
# 查看解析结果
cat workflow/step1_parse/blocks.json | python3 -m json.tool

# 查看文档信息
cat workflow/step2_create_with_permission/doc_with_permission.json

# 查看块添加结果
cat workflow/step3_add_blocks/add_result.json
```

**3. 单独测试子技能**

```bash
# 只测试 Markdown 解析
python3 feishu-md-parser/scripts/md_parser.py input.md output_dir

# 只测试文档创建
python3 feishu-doc-creator-with-permission/scripts/doc_creator_with_permission.py "标题" output_dir
```

**4. 使用检查脚本**

```bash
# 全面检查配置和依赖
python3 feishu-doc-orchestrator/scripts/check_config.py

# 测试简单文档创建
python3 feishu-doc-orchestrator/scripts/create_simple.py
```

---

## 九、参考链接

### 9.1 源码路径

```
skills/feishu-doc-orchestrator/
├── feishu-doc-orchestrator/
│   ├── scripts/
│   │   ├── orchestrator.py           # 主编排脚本
│   │   ├── check_config.py           # 配置检查
│   │   ├── create_simple.py          # 简单测试
│   │   └── test_all_25_blocks.py     # 25种块测试
│   └── CREATED_DOCS.md               # 创建日志
├── feishu-md-parser/
│   └── scripts/md_parser.py          # Markdown解析
├── feishu-doc-creator-with-permission/
│   └── scripts/doc_creator_with_permission.py  # 创建+权限
├── feishu-block-adder/
│   └── scripts/block_adder.py        # 块添加
├── feishu-doc-verifier/
│   └── scripts/doc_verifier.py       # 文档验证
└── feishu-logger/
    └── scripts/logger.py             # 日志记录
```

### 9.2 相关技能

- **feishu-wiki-orchestrator**: 直接在知识库创建文档（非云盘）
- **feishu-doc-creator**: 简化版，只创建文档不管理权限
- **document-hub**: 文档处理中心，支持 Word/Excel/PDF 等格式

### 9.3 外部文档

- [飞书开放平台 - 文档 API](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/docx-v1/document/create)
- [飞书开放平台 - 权限管理](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/docx-v1/document-permission/member/create)
- [Markdown 语法参考](https://www.markdownguide.org/)
- [Python subprocess 文档](https://docs.python.org/3/library/subprocess.html)

---

## 附录：更新日志

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| v1.0 | 2026-02 | 初始版本，支持25种块类型 |

---

*文档版本: v1.0*  
*最后更新: 2026-02-27*  
*作者: 卓然*  
*维护: skill-tutorials 项目*