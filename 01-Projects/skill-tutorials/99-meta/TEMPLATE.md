# {{SKILL_NAME}}

> {{SKILL_DESCRIPTION}}

---

## 概述

### 功能简介

{{功能简介}}

### 适用场景

- {{场景1}}
- {{场景2}}
- {{场景3}}

### 依赖要求

- **Python版本**: {{python_version}}
- **依赖包**: {{dependencies}}
- **外部服务**: {{external_services}}

---

## 安装配置

### 环境要求

```bash
{{环境检查命令}}
```

### 安装步骤

1. **复制技能文件**

```bash
cp -r skills/{{skill_folder}} ~/.openclaw/workspace/skills/
```

2. **安装依赖**

```bash
{{pip_install_commands}}
```

3. **配置环境变量**（如需要）

```bash
{{env_config}}
```

### 配置文件

{{配置文件说明}}

---

## 快速开始

### 最小可用示例

```python
{{minimal_example}}
```

### 常用命令

```bash
{{common_commands}}
```

---

## 详细用法

### 核心API

#### `{{function_name}}({{params}})`

**功能**: {{功能描述}}

**参数**:

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| {{param}} | {{type}} | {{required}} | {{default}} | {{description}} |

**返回值**:

| 字段 | 类型 | 说明 |
|------|------|------|
| {{field}} | {{type}} | {{description}} |

**示例**:

```python
{{code_example}}
```

---

## 示例代码

### 基础示例

```python
{{basic_example}}
```

### 进阶示例

```python
{{advanced_example}}
```

### 完整工作流

```python
{{full_workflow}}
```

---

## 故障排除

### 常见问题

**Q1: {{问题1}}**

A: {{答案1}}

**Q2: {{问题2}}**

A: {{答案2}}

### 错误码说明

| 错误码 | 含义 | 解决方案 |
|--------|------|----------|
| {{code}} | {{meaning}} | {{solution}} |

### 调试技巧

{{debug_tips}}

---

## 参考链接

- **源码路径**: `skills/{{skill_folder}}/`
- **SKILL.md**: `skills/{{skill_folder}}/SKILL.md`
- **相关技能**:
  - {{related_skill_1}}
  - {{related_skill_2}}
- **外部文档**: {{external_docs}}

---

*文档生成时间: {{timestamp}}*
*技能版本: {{version}}*
