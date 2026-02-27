# 如何安装 feishu-doc-orchestrator 技能

> 详细介绍在 OpenClaw 环境中安装此技能的 3 种方式，包括"发给 OpenClaw 自动安装"。

---

## 方式一：发给 OpenClaw 自动安装（最简单）

**适用场景**：你有技能包的 zip 文件或文件内容

### 步骤1：准备技能包文件

获取技能包（以下任选一种）：
- 从同事/朋友处获得 `feishu-doc-orchestrator.zip`
- 从 GitHub 下载：https://github.com/xxx/feishu-doc-orchestrator
- 已有解压后的文件夹

### 步骤2：发给 OpenClaw

**如果是单个文件（如压缩包）**：

直接拖放或粘贴到 OpenClaw 对话框：
```
用户：帮我安装这个技能 [上传 feishu-doc-orchestrator.zip]

OpenClaw：收到，我来解压并安装...
✓ 已解压到 ~/.openclaw/workspace/skills/feishu-doc-orchestrator/
✓ 目录结构检查通过
✓ 现在需要配置飞书凭证，请提供：
  1. FEISHU_APP_ID
  2. FEISHU_APP_SECRET
  3. FEISHU_DRIVE_FOLDER_TOKEN
```

**如果是文件内容（文本形式）**：

把文件内容粘贴给 OpenClaw：
```
用户：请帮我在 skills/feishu-doc-orchestrator/scripts/ 下创建这个文件：

```python
[粘贴 orchestrator.py 的完整代码]
```

OpenClaw：已创建文件，继续创建其他文件...
```

### 步骤3：配置飞书凭证

告诉 OpenClaw 你的飞书配置：

```
用户：配置飞书凭证
APP_ID: cli_xxxxxxxx
APP_SECRET: xxxxxxxx
FOLDER_TOKEN: folder_xxx

OpenClaw：已写入配置文件 ~/.openclaw/.claude/feishu-config.env
正在验证...
✓ 配置验证通过！
```

---

## 方式二：命令行手动安装

**适用场景**：你习惯用命令行，或直接访问服务器

### 步骤1：下载技能包

```bash
# 方式A：Git 克隆
cd ~/.openclaw/workspace/skills/
git clone https://github.com/your-org/feishu-doc-orchestrator.git

# 方式B：下载解压
cd ~/.openclaw/workspace/skills/
wget https://example.com/feishu-doc-orchestrator.zip
unzip feishu-doc-orchestrator.zip
```

### 步骤2：安装依赖

```bash
pip3 install requests python-dotenv
```

### 步骤3：配置凭证

```bash
mkdir -p ~/.openclaw/.claude
cat > ~/.openclaw/.claude/feishu-config.env << EOF
FEISHU_APP_ID=cli_xxxxxxxx
FEISHU_APP_SECRET=xxxxxxxx
FEISHU_DRIVE_FOLDER_TOKEN=folder_xxx
EOF

chmod 600 ~/.openclaw/.claude/feishu-config.env
```

### 步骤4：验证安装

```bash
cd ~/.openclaw/workspace/skills/feishu-doc-orchestrator
python3 feishu-doc-orchestrator/scripts/check_config.py
```

---

## 方式三：通过 ClawHub 安装（如果已发布）

**适用场景**：技能已发布到 ClawHub

```bash
# 安装 ClawHub CLI（如果还没有）
npm install -g clawhub

# 搜索技能
clawhub search feishu-doc

# 安装
clawhub install feishu-doc-orchestrator
```

---

## 对比：哪种方式适合你？

| 方式 | 难度 | 适用场景 | 前提条件 |
|------|------|----------|----------|
| **发给 OpenClaw** | ⭐ 最简单 | 不熟悉命令行，有文件包 | 能与 OpenClaw 对话 |
| **命令行安装** | ⭐⭐ 中等 | 熟悉 Linux/Mac 命令行 | 有服务器/电脑终端访问权限 |
| **ClawHub** | ⭐⭐⭐ 需配置 | 技能已发布 | 已安装 Node.js 和 clawhub CLI |

---

## 实操示例：发给 OpenClaw 安装

### 场景1：你有 zip 文件

**你**：
```
请帮我安装这个技能包 [上传 feishu-doc-orchestrator.zip]
我的飞书配置：
- APP_ID: cli_a123456789
- APP_SECRET: abc123def456
- FOLDER_TOKEN: folder_xxx
```

**OpenClaw 会**：
1. 解压 zip 到 `~/.openclaw/workspace/skills/feishu-doc-orchestrator/`
2. 检查目录结构是否完整
3. 创建 `~/.openclaw/.claude/feishu-config.env` 并写入配置
4. 运行验证脚本确认可用
5. 报告安装结果

### 场景2：你没有文件，需要从零创建

**你**：
```
请帮我创建 feishu-doc-orchestrator 技能，我需要这些文件：

文件1：feishu-doc-orchestrator/scripts/orchestrator.py
内容：
```python
#!/usr/bin/env python3
# 粘贴完整代码...
```

文件2：feishu-md-parser/scripts/md_parser.py
内容：
```python
# 粘贴完整代码...
```

[继续粘贴其他文件...]
```

**OpenClaw 会**：
1. 逐个创建文件和目录
2. 确认每个文件写入成功
3. 最后验证整体结构

---

## 安装后验证

无论哪种方式安装，最后都让 OpenClaw 验证：

```
用户：验证 feishu-doc-orchestrator 是否安装成功

OpenClaw：
检查项目：
✓ 技能目录存在
✓ 所有子技能目录完整（5个）
✓ Python 依赖已安装（requests, python-dotenv）
✓ 飞书配置有效（token 获取成功）
✓ 测试文档创建成功

结论：安装成功，可以正常使用！
```

---

## 常见问题

### Q: 发给 OpenClaw 安装时，文件太大怎么办？

**解决**：分批次发送
```
用户：先安装主技能部分，包含这些文件：
1. orchestrator.py
2. check_config.py

[发完第一批]

用户：继续安装子技能1：
1. md_parser.py

[继续分批...]
```

### Q: 安装后其他 OpenClaw 会话能用吗？

**回答**：可以。技能安装在 `~/.openclaw/workspace/skills/`，所有 OpenClaw 会话共享。

### Q: 如何更新已安装的技能？

**解决**：重新发送新版文件，或：
```bash
# 备份旧版本
mv feishu-doc-orchestrator feishu-doc-orchestrator.backup

# 安装新版本
# [重新执行安装步骤]
```

---

*最后更新: 2026-02-28*