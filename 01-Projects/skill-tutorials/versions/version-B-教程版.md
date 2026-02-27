# 【手把手教程】feishu-doc-orchestrator 完全指南

> 本教程将带你从零开始，把 Markdown 文件转换成精美的飞书文档。

---

## 教程目标

学完本教程，你将能够：
- ✅ 配置飞书开放平台应用
- ✅ 将任意 Markdown 转为飞书文档
- ✅ 批量处理多个文档
- ✅ 处理常见的报错

预计学习时间：**15分钟**

---

## 准备工作

### 你需要准备

1. 一个飞书企业账号（个人版也可）
2. 飞书开放平台的管理权限
3. 本地已安装 Python 3.8+

### 步骤1：创建飞书应用

1. 访问 https://open.feishu.cn/
2. 点击「创建企业自建应用」
3. 填写应用名称："文档助手"
4. 记录 **App ID** 和 **App Secret**

### 步骤2：开启权限

进入应用管理后台，开启以下权限：
- `docx:document:read` - 读取文档
- `docx:document:write` - 创建文档
- `drive:drive:read` - 读取云盘

### 步骤3：发布应用

点击「版本管理与发布」→「创建版本」→「申请发布」

等待管理员审批通过（或如果你是管理员，直接通过）

---

## 实战演练

### 第一步：安装技能

打开终端，执行：

```bash
# 复制技能文件
cp -r skills/feishu-doc-orchestrator ~/.openclaw/workspace/skills/

# 安装依赖
cd ~/.openclaw/workspace/skills/feishu-doc-orchestrator
pip3 install -r requirements.txt
```

### 第二步：配置应用信息

创建配置文件：

```bash
mkdir -p ~/.openclaw/.claude
cat > ~/.openclaw/.claude/feishu-config.env << 'EOF'
FEISHU_APP_ID=cli_你的AppID
FEISHU_APP_SECRET=你的AppSecret
EOF
```

### 第三步：验证配置

```bash
python3 scripts/check_config.py
```

看到 "配置验证通过！" 即可继续。

### 第四步：创建第一个文档

准备一个测试 Markdown 文件：

```bash
cat > /tmp/test.md << 'EOF'
# 我的第一个文档

这是正文内容。

## 功能列表

- 功能一
- 功能二
- 功能三
EOF
```

执行转换：

```bash
python3 scripts/orchestrator.py /tmp/test.md "测试文档"
```

### 第五步：查看结果

命令行会输出：
```
✅ 文档创建成功！
📄 文档链接: https://xxx.feishu.cn/docx/xxx
📊 块数量: 5
```

点击链接查看你的飞书文档！

---

## 进阶技巧

### 批量转换

```bash
for f in docs/*.md; do
    python3 scripts/orchestrator.py "$f" "$(basename $f .md)"
done
```

### 添加协作者

编辑配置文件，添加：
```ini
FEISHU_AUTO_COLLABORATOR_ID=ou_xxx
```

---

## 故障排除

| 现象 | 原因 | 解决 |
|------|------|------|
| "APP_ID not found" | 配置文件路径错误 | 检查路径和文件名 |
| "权限不足" | 应用未开启权限 | 去开放平台开启对应权限 |
| "无法访问文档" | 文档创建成功但无权限 | 检查协作者ID是否正确 |

---

## 下一步

- 探索 [25种支持的块类型](skills/feishu-doc-orchestrator/SKILL.md)
- 学习 [feishu-wiki-orchestrator](wiki版本.md) 直接创建到知识库
- 查看 [高级配置选项](advanced.md)

---

*适用于：喜欢循序渐进学习的用户*
