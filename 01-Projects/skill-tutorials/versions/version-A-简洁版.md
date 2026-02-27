# feishu-doc-orchestrator

## 一句话说明
将 Markdown 转成飞书文档，支持25种块类型。

---

## 什么时候用

| 场景 | 示例 |
|------|------|
| 知识沉淀 | 把笔记转成飞书文档 |
| 批量处理 | 一堆 Markdown 要转换 |
| 团队协作 | 创建带权限的共享文档 |

---

## 5分钟上手

### 1. 安装
```bash
cp -r skills/feishu-doc-orchestrator ~/.openclaw/workspace/skills/
pip3 install requests python-dotenv
```

### 2. 配置
创建 `~/.openclaw/.claude/feishu-config.env`：
```ini
FEISHU_APP_ID=cli_xxx
FEISHU_APP_SECRET=xxx
```

### 3. 使用
```bash
python3 scripts/create_simple.py
```

或在 OpenClaw 里直接说：
> "把 docs/guide.md 转成飞书文档"

---

## 支持的块类型

**文本**: text, heading1-9, quote  
**列表**: bullet, ordered, todo, task  
**代码**: code, callout  
**高级**: table, bitable, image  

完整列表见 [SKILL.md](skills/feishu-doc-orchestrator/SKILL.md)

---

## 常见问题

**Q: 提示 "APP_ID not found"？**  
A: 检查配置文件路径是否正确

**Q: 文档创建成功但内容为空？**  
A: 检查 Markdown 编码是否为 UTF-8

---

*适用于：想快速上手的用户*
