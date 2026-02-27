# 如何安装 feishu-doc-orchestrator 技能

> 本文档说明如何在您的 OpenClaw 环境中安装和使用 feishu-doc-orchestrator 技能。

---

## 方式一：通过 ClawHub 安装（推荐）

如果技能已发布到 ClawHub：

```bash
# 安装技能
clawhub install feishu-doc-orchestrator

# 或者指定版本
clawhub install feishu-doc-orchestrator@1.0.0
```

**验证安装**：
```bash
ls ~/.openclaw/workspace/skills/feishu-doc-orchestrator/
```

---

## 方式二：手动复制安装

如果技能未发布到 ClawHub，或您需要自定义修改：

### 步骤1：复制技能文件

```bash
# 创建技能目录
mkdir -p ~/.openclaw/workspace/skills/

# 复制技能文件（从源码包或仓库）
cp -r /path/to/feishu-doc-orchestrator \
      ~/.openclaw/workspace/skills/

# 验证目录结构
ls ~/.openclaw/workspace/skills/feishu-doc-orchestrator/
# 应看到：feishu-md-parser/  feishu-doc-creator-with-permission/  ...
```

### 步骤2：安装 Python 依赖

```bash
pip3 install requests python-dotenv
```

### 步骤3：配置飞书凭证

创建配置文件：

```bash
mkdir -p ~/.openclaw/.claude
cat > ~/.openclaw/.claude/feishu-config.env << 'EOF'
FEISHU_APP_ID=cli_xxxxxxxx
FEISHU_APP_SECRET=xxxxxxxx
FEISHU_DRIVE_FOLDER_TOKEN=folder_xxx
EOF
```

**权限设置**：
```bash
chmod 600 ~/.openclaw/.claude/feishu-config.env
```

### 步骤4：验证安装

```bash
cd ~/.openclaw/workspace/skills/feishu-doc-orchestrator
python3 feishu-doc-orchestrator/scripts/check_config.py
```

预期输出：
```
✓ 配置文件存在
✓ 获取 tenant_access_token: 成功
✓ 配置检查通过！
```

---

## 方式三：通过 Git 克隆安装

如果技能托管在 GitHub：

```bash
cd ~/.openclaw/workspace/skills/
git clone https://github.com/your-org/feishu-doc-orchestrator.git

# 安装依赖
cd feishu-doc-orchestrator
pip3 install -r requirements.txt  # 如果有
```

---

## 安装后使用

安装完成后，在 OpenClaw 中可以通过以下方式调用：

### 方式A：直接调用子技能脚本

```python
exec("""
cd ~/.openclaw/workspace/skills/feishu-doc-orchestrator
python3 feishu-doc-orchestrator/scripts/orchestrator.py \\
    /path/to/input.md \\
    "文档标题"
""")
```

### 方式B：通过 OpenClaw 工具调用

如果 OpenClaw 已将技能注册为工具：

```python
feishu_doc(action="create", title="标题", content="# Markdown")
```

### 方式C：Python API 调用

```python
import subprocess
from pathlib import Path

skill_path = Path.home() / ".openclaw/workspace/skills/feishu-doc-orchestrator"
script = skill_path / "feishu-doc-orchestrator/scripts/orchestrator.py"

subprocess.run(["python3", str(script), "input.md", "标题"])
```

---

## 故障排除

### Q: 提示 "command not found: clawhub"

**解决**：先安装 ClawHub CLI
```bash
npm install -g clawhub
# 或
brew install clawhub
```

### Q: 提示 "No module named 'requests'"

**解决**：安装 Python 依赖
```bash
pip3 install requests python-dotenv
# 或使用 Python 模块方式
python3 -m pip install requests python-dotenv
```

### Q: 提示 "Config file not found"

**解决**：创建配置文件
```bash
mkdir -p ~/.openclaw/.claude
touch ~/.openclaw/.claude/feishu-config.env
```

然后编辑文件，添加 FEISHU_APP_ID 等配置。

### Q: 提示 "Permission denied"

**解决**：检查飞书应用权限
1. 访问 https://open.feishu.cn/app
2. 找到您的应用
3. 开启权限：`docx:document:create`, `docx:document:write` 等
4. 发布应用版本

---

## 文件结构说明

安装后的目录结构：

```
~/.openclaw/workspace/skills/feishu-doc-orchestrator/
├── SKILL.md                          # 技能说明文档
├── feishu-doc-orchestrator/          # 主技能
│   └── scripts/
│       ├── orchestrator.py           # 主编排脚本 ⭐
│       ├── check_config.py           # 配置检查
│       └── create_simple.py          # 简单测试
├── feishu-md-parser/                 # 子技能1：Markdown解析
│   └── scripts/md_parser.py
├── feishu-doc-creator-with-permission/  # 子技能2：创建+权限
│   └── scripts/doc_creator_with_permission.py
├── feishu-block-adder/               # 子技能3：块添加
│   └── scripts/block_adder.py
├── feishu-doc-verifier/              # 子技能4：验证
│   └── scripts/doc_verifier.py
└── feishu-logger/                    # 子技能5：日志
    └── scripts/logger.py
```

---

## 相关链接

- **ClawHub**: https://clawhub.com
- **OpenClaw 文档**: https://docs.openclaw.ai
- **飞书开放平台**: https://open.feishu.cn

---

*最后更新: 2026-02-28*