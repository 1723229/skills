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

```markdown
| 场景 | 具体示例 | 解决的问题 |
|------|----------|------------|
| 知识库建设 | 将项目 Wiki 从 Markdown 迁移到飞书知识库 | 格式转换、权限批量设置、版本追溯 |
| 自动化文档 | CI/CD 流程自动生成 API 文档到飞书 | 零人工干预、格式统一、即时同步 |
| 内容发布 | 将博客文章批量发布到飞书 | 保留格式、图片迁移、权限管理 |
| 团队协作 | 技术方案评审文档共享 | 精细化权限控制、评论协作、版本管理 |
```

### 1.3 不适用场景

- **实时协作编辑**：飞书文档本身支持更好，此技能专注于**初始化创建**
- **超大规模文档**（>10MB）：建议拆分或直接使用飞书 API
- **复杂交互式文档**：不支持 JavaScript、嵌入式应用等动态内容

### 1.4 依赖要求

```markdown
| 依赖项 | 版本/要求 | 获取方式 | 必要性 |
|--------|-----------|----------|--------|
| Python | >= 3.8 | https://python.org | 必需 |
| requests | >= 2.25.0 | pip install requests | 必需 |
| python-dotenv | >= 0.19.0 | pip install python-dotenv | 必需 |
| 飞书应用 | 企业自建应用 | https://open.feishu.cn | 必需 |
| 云盘文件夹 | folder_token | 飞书云盘 → 文件夹 → 分享 | 必需 |
```

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
- **Windows**: 从 https://python.org 下载安装

**步骤2：检查 pip 版本**

```bash
$ pip3 --version
pip 21.0.1 from .../python3.9/site-packages/pip (python 3.9)
```

如果 pip 不可用：
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

**常见问题**：如果提示 `ModuleNotFoundError`：

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

1. 访问 https://open.feishu.cn/app
2. 点击「创建企业自建应用」
3. 填写应用信息：
   - **应用名称**：`文档助手`（可自定义）
   - **应用描述**：`Markdown 转飞书文档`
4. 记录 **App ID** 和 **App Secret**（后面会用到）

**步骤2：开启权限**

```markdown
| 权限 | 权限代码 | 用途 |
|------|----------|------|
| 创建文档 | docx:document:create | 创建云盘文档 |
| 编辑文档 | docx:document:write | 添加文档内容 |
| 读取文档 | docx:document:read | 验证文档创建 |
| 管理协作者 | docx:document:permission:member:manage | 添加协作者 |
| 转移所有权 | docx:document:permission:transfer | 转移文档所有权 |
| 读取云盘 | drive:drive:read | 获取文件夹信息 |
```

**步骤3：发布应用**

进入「版本管理与发布」→「创建版本」：
- 版本号：1.0.0
- 更新说明：初始版本
- 点击「申请发布」

如果是企业管理员，直接通过；否则需要管理员审批。

**步骤4：获取云盘文件夹 Token**

1. 打开 https://drive.feishu.cn（飞书云盘）
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

```markdown
| 配置项 | 必填 | 获取方式 | 说明 |
|--------|------|----------|------|
| FEISHU_APP_ID | ✓ | 应用详情页 → 凭证 | 应用唯一标识 |
| FEISHU_APP_SECRET | ✓ | 应用详情页 → 凭证 | 应用密钥，勿泄露 |
| FEISHU_API_DOMAIN | ✗ | 固定值 | 国内版用默认，国际版改 open.larksuite.com |
| FEISHU_DRIVE_FOLDER_TOKEN | ✓ | 云盘文件夹链接 | 文档创建位置 |
| FEISHU_AUTO_COLLABORATOR_ID | ✗ | 用户详情页 → Open ID | 自动添加的协作者 |
| FEISHU_AUTO_TRANSFER_OWNER_ID | ✗ | 用户详情页 → Open ID | 转移所有权的目标用户 |
```

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
文档标题: 测试文档-2026-02-28
✓ 文档创建成功！
📄 文档链接: https://xxx.feishu.cn/docx/xxxxxxxx

权限状态:
  协作者添加: [OK]
  所有权转移: [跳过]

========================================
```

**常见问题**：

```markdown
| 错误信息 | 原因 | 解决方案 |
|----------|------|----------|
| Config file not found | 配置文件路径错误 | 检查 ~/.openclaw/.claude/feishu-config.env 是否存在 |
| Failed to get token | App ID/Secret 错误 | 确认凭证正确，应用已发布 |
| Permission denied | 权限未开启 | 检查应用权限设置，确保开启了 docx:document:create 等权限 |
| Folder not found | folder_token 错误 | 确认文件夹存在，token 正确 |
```

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

```markdown
| 类别 | 数量 | 块类型 | 示例 |
|------|------|--------|------|
| 文本 | 11 | text, heading1-9, quote_container | # 标题, > 引用 |
| 列表 | 4 | bullet, ordered, todo, task | - 项, 1. 项, - [ ] 待办 |
| 特殊 | 5 | code, quote, callout, divider, image | ```code, ::: tip, --- |
| AI | 1 | ai_template | 飞书AI模板块 |
| 高级 | 4 | table, bitable, grid, sheet | | 表头 | 表头 | |
```

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

### 5.1 子技能详解

#### 子技能1：feishu-md-parser（Markdown解析器）

**功能**：将 Markdown 文件解析为飞书文档块格式（JSON）

**输入**：Markdown 文件路径、输出目录  
**输出**：`blocks.json`（块数据）、`metadata.json`（元数据）

**支持的 Markdown 语法**：

```markdown
| Markdown 语法 | 飞书块类型 | 说明 |
|--------------|-----------|------|
| # 标题 | heading1 | 1-9级标题支持 |
| **粗体** | text + bold样式 | 行内粗体 |
| - 列表项 | bullet | 无序列表 |
| 1. 列表项 | ordered | 有序列表 |
| - [ ] 待办 | todo | 待办列表 |
| ```code | code | 代码块，支持语法高亮 |
| > 引用 | quote_container | 引用块 |
| ::: tip | callout | 提示框，支持info/tip/warning等样式 |
| --- | divider | 分割线 |
| ![图片](url) | image | 图片（URL需可访问） |
```

**使用示例**：

```bash
python3 feishu-md-parser/scripts/md_parser.py \
    input.md \
    output_dir/
```

**输出示例**（blocks.json）：

```json
{
  "blocks": [
    {
      "block_type": "heading1",
      "heading1": {
        "elements": [{"text_run": {"content": "项目简介"}}]
      }
    },
    {
      "block_type": "text",
      "text": {
        "elements": [{"text_run": {"content": "欢迎使用"}}]
      }
    }
  ],
  "total_blocks": 8,
  "parse_time": "2026-02-28T01:00:00"
}
```

#### 子技能2：feishu-doc-creator-with-permission（创建+权限）

**功能**：创建飞书文档并自动配置权限

**输入**：文档标题、输出目录  
**输出**：`doc_with_permission.json`

**权限配置**：
- 自动添加协作者（如果配置了 `FEISHU_AUTO_COLLABORATOR_ID`）
- 自动转移所有权（如果配置了 `FEISHU_AUTO_TRANSFER_OWNER_ID`）

**使用示例**：

```bash
python3 feishu-doc-creator-with-permission/scripts/doc_creator_with_permission.py \
    "文档标题" \
    output_dir/
```

**输出示例**：

```json
{
  "document_id": "Okbxdbuseo6sGrxpugXcv13BnSc",
  "document_token": "Okbxdbuseo6sGrxpugXcv13BnSc",
  "document_url": "https://feishu.cn/docx/Okbxdbuseo6sGrxpugXcv13BnSc",
  "title": "文档标题",
  "create_time": "2026-02-28T01:00:00",
  "permission": {
    "collaborator_added": true,
    "owner_transferred": false,
    "user_has_full_control": true
  }
}
```

#### 子技能3：feishu-block-adder（块添加器）

**功能**：将解析后的块数据批量添加到飞书文档

**输入**：blocks.json、doc_with_permission.json、输出目录  
**输出**：`add_result.json`

**批量策略**：
- 默认分批添加，每批10个块（避免API限流）
- 支持失败重试（最多3次）
- 表格单独处理（先创建表格结构，再填充内容）

**使用示例**：

```bash
python3 feishu-block-adder/scripts/block_adder.py \
    blocks.json \
    doc_with_permission.json \
    output_dir/
```

#### 子技能4：feishu-doc-verifier（文档验证器）

**功能**：验证文档是否可访问、内容是否完整

**输入**：doc_with_permission.json、输出目录  
**输出**：`verify_result.json`、`screenshot.png`

**验证项**：
- 文档URL可访问性（HTTP 200）
- 文档内容完整性（与预期块数对比）
- 截图留存（Playwright）

#### 子技能5：feishu-logger（日志记录器）

**功能**：记录文档创建日志，支持 Markdown 和 JSON 格式

**输入**：工作流目录、输出目录  
**输出**：`CREATED_DOCS.md`、`created_docs.json`

### 5.2 编程接口

#### Python API

```python
from pathlib import Path
import subprocess

def create_feishu_doc(markdown_path: str, title: str = None) -> dict:
    """
    创建飞书文档
    
    Args:
        markdown_path: Markdown 文件路径
        title: 文档标题，默认为文件名
        
    Returns:
        dict: 包含 document_url, document_token, status 等
    """
    skill_path = Path.home() / ".openclaw/workspace/skills/feishu-doc-orchestrator"
    orchestrator = skill_path / "feishu-doc-orchestrator/scripts/orchestrator.py"
    
    cmd = [
        "python3", str(orchestrator),
        markdown_path,
        title or Path(markdown_path).stem
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # 从输出中提取文档URL
    for line in result.stdout.split('\n'):
        if "文档 URL:" in line:
            url = line.split("文档 URL:")[1].strip()
            return {"success": True, "document_url": url}
    
    return {"success": False, "error": result.stderr}
```

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

def convert_single_file(md_file: str, title: str = None):
    """转换单个文件"""
    skill_dir = Path.home() / ".openclaw/workspace/skills/feishu-doc-orchestrator"
    script = skill_dir / "feishu-doc-orchestrator/scripts/orchestrator.py"
    
    cmd = ["python3", str(script), md_file, title or Path(md_file).stem]
    
    print(f"正在转换: {md_file}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    print(result.stdout)
    if result.returncode != 0:
        print(f"错误: {result.stderr}")
        return None
    
    # 提取文档 URL
    for line in result.stdout.split('\n'):
        if "文档 URL:" in line:
            return line.split("文档 URL:")[1].strip()
    
    return None

# 使用示例
if __name__ == "__main__":
    url = convert_single_file("/tmp/demo.md", "我的文档")
    if url:
        print(f"✅ 创建成功: {url}")
    else:
        print("❌ 创建失败")
```

### 6.2 进阶示例：批量转换

```python
#!/usr/bin/env python3
"""
进阶示例：批量转换目录下的所有 Markdown 文件
"""
import subprocess
import json
from pathlib import Path
from datetime import datetime

def batch_convert(directory: str, output_log: str = "conversion_log.json"):
    """
    批量转换目录下的所有 Markdown 文件
    """
    skill_dir = Path.home() / ".openclaw/workspace/skills/feishu-doc-orchestrator"
    script = skill_dir / "feishu-doc-orchestrator/scripts/orchestrator.py"
    
    md_files = list(Path(directory).glob("*.md"))
    print(f"发现 {len(md_files)} 个 Markdown 文件")
    
    results = []
    for i, md_file in enumerate(md_files, 1):
        print(f"\n[{i}/{len(md_files)}] 处理: {md_file.name}")
        
        title = md_file.stem
        cmd = ["python3", str(script), str(md_file), title]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # 提取结果
        doc_url = None
        for line in result.stdout.split('\n'):
            if "文档 URL:" in line:
                doc_url = line.split("文档 URL:")[1].strip()
                break
        
        results.append({
            "file": str(md_file),
            "title": title,
            "status": "success" if doc_url else "failed",
            "url": doc_url,
            "timestamp": datetime.now().isoformat()
        })
        
        if doc_url:
            print(f"  ✅ {doc_url}")
        else:
            print(f"  ❌ 失败")
    
    # 保存日志
    with open(output_log, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n转换完成！日志已保存: {output_log}")
    success_count = sum(1 for r in results if r['status'] == 'success')
    print(f"成功: {success_count}/{len(results)}")
    
    return results

# 使用示例
if __name__ == "__main__":
    batch_convert("~/Documents/notes", "~/conversion_log.json")
```

### 6.3 完整工作流：CI/CD 集成

```python
#!/usr/bin/env python3
"""
生产级示例：CI/CD 流程自动生成文档
- 错误处理
- 日志记录
- 通知集成（飞书机器人）
- 失败重试
"""
import subprocess
import json
import logging
import time
from pathlib import Path
from datetime import datetime
import requests

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FeishuDocCreator:
    """飞书文档创建器（生产级）"""
    
    def __init__(self, webhook_url: str = None):
        self.skill_dir = Path.home() / ".openclaw/workspace/skills/feishu-doc-orchestrator"
        self.script = self.skill_dir / "feishu-doc-orchestrator/scripts/orchestrator.py"
        self.webhook_url = webhook_url
        self.max_retries = 3
    
    def create_doc(self, md_file: str, title: str = None, retry: int = 0) -> dict:
        """创建文档（带重试机制）"""
        if retry > self.max_retries:
            logger.error(f"超过最大重试次数: {md_file}")
            return {"success": False, "error": "Max retries exceeded"}
        
        try:
            cmd = ["python3", str(self.script), md_file, title or Path(md_file).stem]
            logger.info(f"执行命令: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode != 0:
                logger.error(f"转换失败: {result.stderr}")
                if retry < self.max_retries:
                    logger.info(f"第 {retry + 1} 次重试...")
                    time.sleep(2 ** retry)
                    return self.create_doc(md_file, title, retry + 1)
                return {"success": False, "error": result.stderr}
            
            # 提取文档URL
            for line in result.stdout.split('\n'):
                if "文档 URL:" in line:
                    url = line.split("文档 URL:")[1].strip()
                    logger.info(f"创建成功: {url}")
                    return {"success": True, "url": url}
            
            return {"success": False, "error": "URL not found"}
            
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Timeout"}
        except Exception as e:
            return {"success": False, "error": str(e)}

# 使用示例
if __name__ == "__main__":
    creator = FeishuDocCreator()
    
    docs = [
        ("docs/api.md", "API文档"),
        ("docs/guide.md", "用户指南"),
    ]
    
    for md, title in docs:
        result = creator.create_doc(md, title)
        print(f"{title}: {'✅' if result['success'] else '❌'}")
```

---

## 七、最佳实践

### 7.1 性能优化

**大批量处理时**：
- 使用批量转换脚本，避免重复加载 Python 解释器
- 调整 `feishu-block-adder` 中的批量大小（默认10个块/批）

### 7.2 安全注意事项

**配置文件安全**：
```bash
# 设置配置文件权限，防止其他用户读取
chmod 600 ~/.openclaw/.claude/feishu-config.env

# 不要将配置文件提交到 Git
echo "feishu-config.env" >> .gitignore
```

**敏感信息处理**：
- 日志文件中会自动脱敏 App Secret
- 分享文档链接时注意权限设置

### 7.3 推荐工作流

**个人使用**：
```
本地 Markdown → feishu-doc-orchestrator → 飞书云盘
```

**团队协作**：
```
Git 仓库 Markdown → CI/CD → feishu-doc-orchestrator → 飞书知识库
```

### 7.4 与其他技能的组合

**与 feishu-wiki-orchestrator 结合**：
- feishu-doc-orchestrator：创建到云盘
- feishu-wiki-orchestrator：创建到知识库
- 根据文档归属选择合适的技能

---

## 八、故障排除

### 8.1 安装问题

**问题**：`pip install` 提示权限不足
```
PermissionError: [Errno 13] Permission denied
```

**解决方案**：
```bash
# 方案1：使用 --user 参数
pip3 install --user requests python-dotenv

# 方案2：使用虚拟环境
python3 -m venv venv
source venv/bin/activate
pip install requests python-dotenv
```

### 8.2 配置问题

**问题**：`Config file not found`

**诊断步骤**：
```bash
# 1. 检查文件是否存在
ls -la ~/.openclaw/.claude/feishu-config.env

# 2. 检查文件内容格式
cat ~/.openclaw/.claude/feishu-config.env

# 3. 检查文件权限
ls -l ~/.openclaw/.claude/feishu-config.env
```

### 8.3 API 问题

**问题**：`Failed to get token`

**根因分析**：
1. App ID 或 App Secret 错误
2. 应用未发布
3. 网络问题

**解决方案**：
```bash
# 验证凭证
curl -X POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal \
  -H "Content-Type: application/json" \
  -d '{"app_id":"YOUR_APP_ID","app_secret":"YOUR_APP_SECRET"}'
```

### 8.4 调试技巧

**查看中间结果**：
```bash
# 查看解析后的块
cat workflow/step1_parse/blocks.json

# 查看文档信息
cat workflow/step2_create_with_permission/doc_with_permission.json

# 查看验证截图
ls -la workflow/step4_verify/screenshot.png
```

---

## 九、参考链接

### 9.1 源码路径

```
skills/feishu-doc-orchestrator/
├── feishu-doc-orchestrator/scripts/orchestrator.py
├── feishu-md-parser/scripts/md_parser.py
├── feishu-doc-creator-with-permission/scripts/doc_creator_with_permission.py
├── feishu-block-adder/scripts/block_adder.py
├── feishu-doc-verifier/scripts/doc_verifier.py
└── feishu-logger/scripts/logger.py
```

### 9.2 相关技能

```markdown
| 技能 | 关系 | 说明 |
|------|------|------|
| feishu-wiki-orchestrator | 替代选择 | 直接创建到知识库（而非云盘） |
| feishu-doc-creator | 简化版 | 单技能实现，无编排，适合简单场景 |
| content-extractor | 上游 | 抓取内容后可用本技能转换 |
| document-hub | 生态 | 统一的文档处理入口 |
```

### 9.3 外部文档

- [飞书开放平台 - 文档 API](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/docx-v1/document/overview)
- [飞书开放平台 - 权限管理](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/docx-v1/document-permission/overview)
- [Markdown 语法指南](https://www.markdownguide.org/)

---

## 附录：完整工作流示意图

```
┌─────────────────────────────────────────────────────────────────┐
│                        用户输入                                  │
│              Markdown 文件 + 文档标题                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 1: Markdown 解析                                          │
│  ├─ 输入: input.md                                              │
│  ├─ 处理: AST 解析 → 25种块类型识别                              │
│  └─ 输出: workflow/step1_parse/blocks.json                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 2: 文档创建 + 权限管理（原子操作）                          │
│  ├─ 调用: POST /docx/v1/documents                               │
│  ├─ 权限: 添加协作者 + 转移所有权（可选）                          │
│  └─ 输出: workflow/step2_create_with_permission/doc.json        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 3: 块添加                                                  │
│  ├─ 批量: 10个块/批次（可配置）                                   │
│  ├─ 重试: 失败自动重试3次                                        │
│  └─ 输出: workflow/step3_add_blocks/add_result.json             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 4: 文档验证                                                │
│  ├─ 检查: URL 可访问性 + 内容完整性                              │
│  ├─ 截图: Playwright 自动化截图                                  │
│  └─ 输出: workflow/step4_verify/verify_result.json + .png       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 5: 日志记录                                                │
│  ├─ Markdown 格式: CREATED_DOCS.md（人类可读）                   │
│  ├─ JSON 格式: created_docs.json（机器可读）                     │
│  └─ 用途: 审计追溯 + 批量管理                                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        输出结果                                  │
│         飞书文档 URL + 完整日志 + 工作流文件                      │
└─────────────────────────────────────────────────────────────────┘
```

---

**文档信息**

```markdown
| 项目 | 内容 |
|------|------|
| 版本 | v1.0 |
| 更新时间 | 2026-02-28 |
| 技能版本 | feishu-doc-orchestrator v1.0 |
| 作者 | AI Assistant |
| 适用 OpenClaw 版本 | >= 1.0 |
```

---

*教程完成*