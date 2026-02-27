# Skill Tutorials - OpenClaw 技能教程项目

> 基于 PARA 方法管理的 OpenClaw 技能教程项目，包含 49+ 个技能的详细文档和源码。

---

## 📁 项目结构（PARA）

```
.
├── 01-Projects/skill-tutorials/    # 本项目主目录
│   ├── 99-meta/                    # 项目元数据（写作规范、模板）
│   ├── docs/                       # 项目文档（README、安装指南等）
│   ├── scripts/                    # 自动化脚本
│   ├── src/                        # 技能源代码
│   │   └── extracted/skills/       # 提取的技能源码
│   ├── tutorials/                  # 技能教程（按分类）
│   │   ├── 01-feishu-ecosystem/    # 飞书生态技能
│   │   ├── 02-content-generation/  # 内容生成技能
│   │   ├── 03-data-processing/     # 数据处理技能
│   │   ├── 04-dev-tools/           # 开发工具技能
│   │   ├── 05-external-integrations/ # 外部集成技能
│   │   └── 06-ai-agents/           # AI Agent 技能
│   └── versions/                   # 教程风格版本
└── README.md                       # 本文件
```

---

## 🚀 快速开始

### 方式1：克隆整个项目

```bash
git clone https://github.com/wulaosiji/skills.git
cd skills/01-Projects/skill-tutorials
```

### 方式2：使用 OpenClaw 安装

告诉 OpenClaw：
```
请帮我从 https://github.com/wulaosiji/skills 安装 feishu-doc-orchestrator 技能
```

---

## 📚 内容导航

| 目录 | 内容 | 数量 |
|------|------|------|
| [tutorials/01-feishu-ecosystem](tutorials/01-feishu-ecosystem/) | 飞书生态技能（文档创建、消息发送等） | 15 个 |
| [tutorials/02-content-generation](tutorials/02-content-generation/) | 内容生成技能（视频、图片、写作） | 13 个 |
| [tutorials/03-data-processing](tutorials/03-data-processing/) | 数据处理技能（PDF、OCR、爬取） | 8 个 |
| [tutorials/04-dev-tools](tutorials/04-dev-tools/) | 开发工具技能（GitHub、日历等） | 6 个 |
| [tutorials/05-external-integrations](tutorials/05-external-integrations/) | 外部集成技能（地图、语音等） | 5 个 |
| [tutorials/06-ai-agents](tutorials/06-ai-agents/) | AI Agent 技能（安全、审计等） | 4 个 |

---

## 📝 写作规范

查看 [99-meta/WRITING_STANDARD.md](99-meta/WRITING_STANDARD.md) 了解教程写作标准。

所有教程遵循统一的9章节结构：
1. 概述（功能简介、适用场景、依赖要求）
2. 安装配置（环境检查、安装步骤、配置文件）
3. 核心概念（架构图、关键术语、工作流程）
4. 快速开始（最小可用示例）
5. 详细用法（功能点详解、API说明）
6. 示例代码（基础+进阶+生产级）
7. 最佳实践（性能、安全、常见陷阱）
8. 故障排除（错误场景、诊断步骤、解决方案）
9. 参考链接（源码路径、相关技能、外部文档）

---

## 🛠️ 技能源码

所有技能源码位于 `src/extracted/skills/` 目录下，每个技能包含：
- `SKILL.md` - 技能说明文档
- `scripts/` - 可执行脚本
- 其他资源文件

---

## 📊 项目统计

- **总技能数**: 49+
- **教程文档**: 49 篇
- **源码文件**: 1200+ 个
- **代码行数**: 53,000+ 行

---

## 🤝 使用建议

### 对于普通用户
1. 浏览 `tutorials/` 找到需要的技能
2. 阅读对应教程了解使用方法
3. 复制源码或让 OpenClaw 自动安装

### 对于开发者
1. 参考 `99-meta/WRITING_STANDARD.md` 编写新教程
2. 使用 `scripts/` 中的工具批量生成文档
3. 提交 PR 贡献新技能或改进现有教程

---

## 📄 许可证

MIT License - 详见 LICENSE 文件

---

*最后更新: 2026-02-28*