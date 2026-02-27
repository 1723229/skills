# feishu-doc-orchestrator - 飞书文档创建编排技能

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
| Python | >= 3.8 | https://python.org | 必需 |
| requests | >= 2.25.0 | pip install requests | 必需 |
| python-dotenv | >= 0.19.0 | pip install python-dotenv | 必需 |
| 飞书应用 | 企业自建应用 | https://open.feishu.cn | 必需 |
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

1. 打开 https://drive.feishu.cn（飞书云盘）
2. 创建或选择文件夹，右键 →「分享」→「复制链接」
3. 从链接中提取 `folder_token`：
   ```
   https://drive.feishu.cn/file/folder/DYPXf8ZktlOCIXdmGq3cfjevn2F
                                        └────────────────────────── folder_token
   ```

### 2.4 配置文件详解

**创建配置文件**：

```bash
$ mkdir -p ~/.openclaw/.claude
$ cat > ~/.openclaw/.claude/feishu-config.env << 'EOF'
# 飞书开放平台 - 应用凭证
FEISHU_APP_ID=cli_xxxxxxxx
FEISHU_APP_SECRET=xxxxxxxx

# 飞书 API 域名
FEISHU_API_DOMAIN=https://open.feishu.cn

# 云盘文件夹 Token
FEISHU_DRIVE_FOLDER_TOKEN=DYPXf8ZktlOCIXdmGq3cfjevn2F

# 可选：自动添加协作者
# FEISHU_AUTO_COLLABORATOR_ID=ou_xxxxxxxx
EOF
```

**配置项说明**：

| 配置项 | 必填 | 获取方式 | 说明 |
|--------|------|----------|------|
| FEISHU_APP_ID | ✓ | 应用详情页 | 应用唯一标识 |
| FEISHU_APP_SECRET | ✓ | 应用详情页 | 应用密钥，勿泄露 |
| FEISHU_API_DOMAIN | ✗ | 固定值 | 国内版用默认 |
| FEISHU_DRIVE_FOLDER_TOKEN | ✓ | 云盘文件夹链接 | 文档创建位置 |
| FEISHU_AUTO_COLLABORATOR_ID | ✗ | 用户 Open ID | 自动添加协作者 |

### 2.5 验证配置

**步骤1：运行配置检查脚本**

```bash
$ cd ~/.openclaw/workspace/skills/feishu-doc-orchestrator
$ python3 feishu-doc-orchestrator/scripts/check_config.py

========================================
飞书文档创建技能 - 配置检查
========================================
✓ 配置文件存在
✓ FEISHU_APP_ID: cli_xxx... (长度正确)
✓ 获取 tenant_access_token: 成功
✓ 飞书 API 连接: 正常

配置检查通过！可以开始使用。
========================================
```

**常见问题**：

| 错误信息 | 原因 | 解决方案 |
|----------|------|----------|
| Config file not found | 配置文件路径错误 | 检查 ~/.openclaw/.claude/feishu-config.env |
| Failed to get token | App ID/Secret 错误 | 确认凭证正确，应用已发布 |
| Permission denied | 权限未开启 | 检查应用权限设置 |
| Folder not found | folder_token 错误 | 确认文件夹存在 |

---

## 三、核心概念

### 3.1 编排架构

```
┌──────────────────────────────────────┐
│           Orchestrator               │
│          协调5个子技能                │
└──────────────────────────────────────┘
                   │
    ┌──────────────┼──────────────┐
    │              │              │
    ▼              ▼              ▼
┌──────┐    ┌──────────┐    ┌──────┐
│Step 1│───▶│  Step 2  │───▶│Step 3│
│解析  │    │创建+权限 │    │块添加│
└──────┘    └──────────┘    └──┬───┘
                               │
                    ┌──────────┴──┐
                    ▼             ▼
              ┌────────┐    ┌────────┐
              │Step 4  │    │Step 5  │
              │验证    │    │日志    │
              └────────┘    └────────┘
```

**设计原理**：
- **关注点分离**：每个子技能只负责一件事
- **失败隔离**：单个步骤失败不影响其他步骤重试
- **数据持久化**：中间结果保存到文件，可审计调试

### 3.2 支持的25种块类型

| 类别 | 数量 | 块类型 | Markdown 示例 |
|------|------|--------|---------------|
| 文本 | 11 | text, heading1-9, quote | `# 标题`, `> 引用` |
| 列表 | 4 | bullet, ordered, todo, task | `- 项`, `1. 项` |
| 特殊 | 5 | code, callout, divider, image | ` ```code`, `::: tip` |
| AI | 1 | ai_template | 飞书AI模板块 |
| 高级 | 4 | table, bitable, grid, sheet | `\|表格\|` |

### 3.3 工作流程文件

```
workflow/
├── step1_parse/
│   ├── blocks.json
│   └── metadata.json
├── step2_create_with_permission/
│   └── doc_with_permission.json
├── step3_add_blocks/
│   └── add_result.json
└── step4_verify/
    ├── verify_result.json
    └── screenshot.png

CREATED_DOCS.md
created_docs.json
```

---

## 四、快速开始

### 4.1 最小可用示例

**步骤1：准备 Markdown 文件**

```bash
$ cat > /tmp/demo.md << 'EOF'
# 项目简介

## 功能特性

- 功能一
- 功能二

## 代码示例

```python
print("Hello")
```
EOF
```

**步骤2：执行转换**

```bash
$ python3 feishu-doc-orchestrator/scripts/orchestrator.py \
    /tmp/demo.md "项目文档"

文档创建完成！
文档 URL: https://xxx.feishu.cn/docx/...
耗时: 3.45 秒
```

**步骤3：验证结果**

1. 点击输出的文档 URL
2. 检查内容是否完整
3. 检查权限设置

### 4.2 命令行参数

```bash
python3 orchestrator.py <markdown文件> [文档标题] [工作流目录]

参数说明:
  markdown文件   必需  要转换的 Markdown 文件路径
  文档标题       可选  默认为文件名（不含扩展名）
  工作流目录     可选  默认为 workflow/
```

---

## 五、详细用法

### 5.1 子技能详解

**Markdown解析器** (feishu-md-parser)

| 项目 | 说明 |
|------|------|
| 功能 | 将 Markdown 解析为飞书块格式 |
| 输入 | Markdown 文件路径、输出目录 |
| 输出 | blocks.json、metadata.json |
| 支持 | 25种块类型解析 |

**创建+权限** (feishu-doc-creator-with-permission)

| 项目 | 说明 |
|------|------|
| 功能 | 创建飞书文档并配置权限 |
| 输入 | 文档标题、输出目录 |
| 输出 | doc_with_permission.json |
| 权限 | 自动添加协作者、转移所有权 |

**块添加器** (feishu-block-adder)

| 项目 | 说明 |
|------|------|
| 功能 | 批量添加块到飞书文档 |
| 输入 | blocks.json、doc.json、输出目录 |
| 输出 | add_result.json |
| 策略 | 每批50个块，失败重试3次 |

### 5.2 Python API

```python
import subprocess
from pathlib import Path

def create_doc(md_path: str, title: str):
    """创建飞书文档"""
    script = Path.home() / ".openclaw/workspace/skills/feishu-doc-orchestrator/scripts/orchestrator.py"
    result = subprocess.run(
        ["python3", str(script), md_path, title],
        capture_output=True, text=True
    )
    return result
```

---

## 六、示例代码

### 6.1 基础示例

```python
#!/usr/bin/env python3
import subprocess
from pathlib import Path

def convert_single(md_path: str, title: str) -> str:
    script = Path.home() / ".openclaw/workspace/skills/feishu-doc-orchestrator/scripts/orchestrator.py"
    result = subprocess.run(
        ["python3", str(script), md_path, title],
        capture_output=True, text=True
    )
    
    for line in result.stdout.split('\n'):
        if "文档 URL:" in line:
            return line.split("文档 URL:")[1].strip()
    return None

# 使用
url = convert_single("/tmp/demo.md", "我的文档")
print(f"✅ 成功: {url}")
```

### 6.2 批量转换

```python
def batch_convert(md_files: list):
    results = []
    for f in md_files:
        url = convert_single(f, Path(f).stem)
        results.append({"file": f, "url": url})
    return results

docs = batch_convert(["a.md", "b.md", "c.md"])
```

### 6.3 CI/CD 集成

```python
class FeishuDocPublisher:
    def __init__(self):
        self.script = Path.home() / ".openclaw/workspace/skills/feishu-doc-orchestrator/scripts/orchestrator.py"
    
    def publish(self, md_path: str, title: str) -> dict:
        result = subprocess.run(
            ["python3", str(self.script), md_path, title],
            capture_output=True, text=True, timeout=120
        )
        return {"success": result.returncode == 0}
```

---

## 七、最佳实践

### 7.1 性能优化

- 批量处理时使用并行
- 图片使用飞书云盘托管
- 定期清理工作流目录

### 7.2 安全注意事项

```bash
# 设置配置文件权限
chmod 600 ~/.openclaw/.claude/feishu-config.env

# 添加到 .gitignore
echo "feishu-config.env" >> .gitignore
```

### 7.3 与其他技能组合

| 技能 | 组合方式 | 说明 |
|------|----------|------|
| feishu-wiki-orchestrator | 替代选择 | 创建到知识库 |
| content-extractor | 上游处理 | 抓取内容后转换 |
| document-hub | 统一入口 | 文档处理中心 |

---

## 八、故障排除

### 8.1 安装问题

| 问题 | 现象 | 解决方案 |
|------|------|----------|
| pip 权限不足 | PermissionError | 使用 `pip install --user` |
| 模块未找到 | ModuleNotFoundError | 使用 `python -m pip` |

### 8.2 配置问题

| 问题 | 现象 | 解决方案 |
|------|------|----------|
| 配置未找到 | Config file not found | 检查文件路径 |
| Token 获取失败 | Failed to get token | 确认 App ID/Secret |
| 权限不足 | Permission denied | 检查应用权限设置 |

### 8.3 运行时问题

| 问题 | 现象 | 解决方案 |
|------|------|----------|
| 块添加失败 | 部分块未显示 | 检查 Markdown 语法 |
| 文档无法访问 | 403 错误 | 检查权限配置 |
| 超时 | Timeout | 增加超时时间或分批处理 |

### 8.4 调试技巧

```bash
# 查看中间结果
cat workflow/step1_parse/blocks.json

# 单独测试子技能
python3 feishu-md-parser/scripts/md_parser.py input.md output_dir

# 检查配置
python3 feishu-doc-orchestrator/scripts/check_config.py
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

| 技能 | 关系 | 说明 |
|------|------|------|
| feishu-wiki-orchestrator | 替代选择 | 直接创建到知识库 |
| feishu-doc-creator | 简化版 | 单技能实现 |
| content-extractor | 上游 | 抓取内容后转换 |
| document-hub | 生态 | 统一文档处理入口 |

### 9.3 外部文档

- [飞书开放平台 - 文档 API](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/docx-v1/document/create)
- [飞书开放平台 - 权限管理](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/docx-v1/document-permission/member/create)
- [Markdown 语法参考](https://www.markdownguide.org/)

---

**文档信息**

| 项目 | 内容 |
|------|------|
| 版本 | v1.0 |
| 更新时间 | 2026-02-28 |
| 技能版本 | feishu-doc-orchestrator v1.0 |
| 作者 | AI Assistant |
| 适用 OpenClaw 版本 | >= 1.0 |

---

*教程完成*