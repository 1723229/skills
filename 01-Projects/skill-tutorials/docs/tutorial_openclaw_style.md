# feishu-doc-orchestrator - Markdown转飞书文档

> 在 OpenClaw 中将 Markdown 文件转换为飞书文档，支持表格、代码块、权限管理等完整功能。

---

## 一、功能简介

**feishu-doc-orchestrator** 是 OpenClaw 内置的技能编排方案，用于将 Markdown 内容转换为飞书云文档。它通过协调5个子技能完成：

1. **Markdown 解析** - 识别标题、表格、代码块等25种元素
2. **文档创建** - 在飞书云盘创建新文档
3. **权限配置** - 自动添加协作者（可选）
4. **内容填充** - 将解析后的内容写入文档
5. **结果验证** - 检查文档可访问性

**核心优势**：
- 支持飞书原生表格（非图片）
- 保留 Markdown 格式（代码高亮、列表层级等）
- 自动处理权限，无需手动分享

---

## 二、适用场景

| 场景 | 示例 | 效果 |
|------|------|------|
| 批量文档迁移 | 将项目 README 批量转为飞书文档 | 保留格式，生成可编辑文档 |
| 自动化报告 | 每日/周报自动生成并发送到飞书 | 零人工，定时产出 |
| 知识库建设 | 技术文档、API 文档统一管理 | 集中存储，团队协作 |

---

## 三、使用方法

### 3.1 在 OpenClaw 中调用

**方式一：直接创建文档（推荐）**

```python
# 创建飞书文档，直接传入 Markdown 内容
feishu_doc(
    action="create",
    title="文档标题",
    content="""# 标题

## 章节

内容正文...

| 表格 | 列2 |
|------|-----|
| 数据 | 数据 |
"""
)
```

**方式二：追加到现有文档**

```python
# 在已有文档中追加内容
feishu_doc(
    action="append",
    doc_token="已有的文档token",
    content="## 新增章节\n\n新内容..."
)
```

**方式三：读取本地 Markdown 文件**

```python
# 读取本地文件并创建文档
content = read("/path/to/file.md")
feishu_doc(
    action="create",
    title="从Markdown导入",
    content=content
)
```

### 3.2 支持的 Markdown 语法

| Markdown | 飞书效果 | 说明 |
|----------|----------|------|
| `# 标题` | 标题1 | 支持1-9级 |
| `- 列表` | 无序列表 | 支持嵌套 |
| `1. 列表` | 有序列表 | 自动编号 |
| `\|表格\|` | **原生表格** | 可编辑的表格 |
| ` ```py ` | 代码块 | 支持语法高亮 |
| `**粗体**` | 粗体 | 行内样式 |
| `> 引用` | 引用块 | 灰色背景 |

### 3.3 参数说明

**feishu_doc 工具参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| action | string | ✓ | `create` 或 `append` |
| title | string | ✓(create) | 文档标题 |
| content | string | ✓ | Markdown 内容 |
| doc_token | string | ✓(append) | 现有文档的 token |

**权限配置**（可选，在创建时生效）：

配置项在 `~/.openclaw/.env` 中设置：

```bash
# 自动添加协作者（Open ID）
FEISHU_AUTO_COLLABORATOR_ID=ou_xxxxxxxx

# 自动转移所有权
FEISHU_AUTO_TRANSFER_OWNER_ID=ou_xxxxxxxx
```

---

## 四、完整示例

### 示例1：创建带表格的技术文档

```python
content = """# API 接口文档

## 认证方式

所有接口需要携带 Token：

```bash
Authorization: Bearer {your_token}
```

## 接口列表

| 接口 | 方法 | 说明 |
|------|------|------|
| /api/users | GET | 获取用户列表 |
| /api/users | POST | 创建用户 |
| /api/users/{id} | DELETE | 删除用户 |

## 响应格式

```json
{
  "code": 0,
  "data": {},
  "message": "success"
}
```

> 💡 提示：所有时间戳使用 Unix 毫秒格式
"""

result = feishu_doc(
    action="create",
    title="API接口文档",
    content=content
)

print(f"文档已创建: {result['url']}")
```

**预期结果**：
- 飞书文档包含3级标题结构
- 表格是**原生可编辑**的（非图片）
- 代码块有语法高亮
- 提示块显示为飞书 callout 样式

### 示例2：批量生成周报

```python
import datetime

# 生成周报内容
week_number = datetime.datetime.now().isocalendar()[1]
content = f"""# 第{week_number}周工作周报

## 本周完成

- 完成项目 A 的需求评审
- 修复了 5 个 Bug
- 编写了技术文档

## 下周计划

| 任务 | 负责人 | 截止时间 |
|------|--------|----------|
| 接口开发 | 张三 | 下周三 |
| 测试用例 | 李四 | 下周五 |

## 问题与风险

目前无阻塞性问题。
"""

# 创建到飞书
feishu_doc(
    action="create",
    title=f"周报-第{week_number}周",
    content=content
)
```

---

## 五、常见问题

### Q1: 表格显示为纯文本？

**原因**：使用了错误的表格语法。

**解决**：确保表格格式正确：
```markdown
| 表头1 | 表头2 |
|-------|-------|
| 数据1 | 数据2 |
```

### Q2: 文档创建成功但内容为空？

**原因**：内容参数未正确传递。

**解决**：检查 content 参数是否为字符串：
```python
# 正确
feishu_doc(action="create", title="测试", content="# 标题")

# 错误 - content 是 None 或未定义
feishu_doc(action="create", title="测试", content=undefined_var)
```

### Q3: 如何获取文档的 doc_token？

**方法**：从创建结果中提取
```python
result = feishu_doc(action="create", ...)
doc_token = result['document_id']  # 或 'document_token'
```

---

## 六、注意事项

1. **表格支持**：飞书 API 支持原生表格，但创建较慢（每个单元格需单独填充）
2. **图片限制**：Markdown 中的图片需使用飞书可访问的 URL
3. **权限**：默认只有创建者有编辑权限，如需共享请配置 `FEISHU_AUTO_COLLABORATOR_ID`
4. **内容长度**：超大文档（>5000字）建议分多次 `append`

---

## 七、相关技能

| 技能 | 用途 | 区别 |
|------|------|------|
| feishu_doc | 创建/编辑云文档 | 本技能的基础调用方式 |
| feishu_wiki | 创建知识库文档 | 文档创建在知识库而非云盘 |
| feishu_bitable | 创建多维表格 | 结构化数据，非富文本 |

---

*最后更新: 2026-02-28*