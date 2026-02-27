# Skill Tutorials Project - 技能教程项目

> 基于 xiaozhua_skills_pack 的全量技能教程文档

## 项目结构

```
skill-tutorials/
├── README.md                           # 项目总览（本文档）
├── extracted/                          # 技能包解压目录
│   └── skills/                         # 60+ 个技能源码
├── tutorials/                          # 教程输出目录
│   ├── 01-feishu-ecosystem/            # 飞书生态技能（18个）
│   ├── 02-content-generation/          # 内容生成技能（12个）
│   ├── 03-data-processing/             # 数据处理技能（8个）
│   ├── 04-dev-tools/                   # 开发工具技能（6个）
│   ├── 05-external-integrations/       # 外部集成技能（5个）
│   ├── 06-ai-agents/                   # AI Agent技能（4个）
│   ├── 07-media/                       # 媒体处理技能（5个）
│   ├── 08-security/                    # 安全工具技能（4个）
│   ├── 09-utilities/                   # 实用工具技能（3个）
│   └── 99-meta/                        # 元文档（索引、模板）
└── scripts/                            # 自动化脚本
    ├── generate-tutorial.py            # 教程生成脚本
    └── upload-to-feishu.py             # 飞书知识库上传脚本
```

---

## 教程清单（共62个）

### 01-飞书生态 (18个)

| # | 技能名称 | 功能描述 | 状态 |
|---|----------|----------|------|
| 1 | feishu-doc-orchestrator | Markdown转飞书文档编排器 | ⏳ |
| 2 | feishu-wiki-orchestrator | 飞书知识库文档创建编排 | ⏳ |
| 3 | feishu-md-parser | Markdown解析器（子技能） | ⏳ |
| 4 | feishu-block-adder | 文档块添加器（子技能） | ⏳ |
| 5 | feishu-doc-creator-with-permission | 文档创建+权限管理 | ⏳ |
| 6 | feishu-doc-verifier | 文档验证工具 | ⏳ |
| 7 | feishu-logger | 日志记录器 | ⏳ |
| 8 | feishu-doc-converter | 文档格式转换 | ⏳ |
| 9 | feishu-doc-creator | 文档创建统一入口 | ⏳ |
| 10 | feishu-chat-extractor | 群聊历史消息提取 | ⏳ |
| 11 | feishu-chat-monitor | @消息监控提醒 | ⏳ |
| 12 | feishu-pdf-downloader | PDF下载工具 | ⏳ |
| 13 | feishu-doc-perm | 文档权限管理 | ⏳ |
| 14 | feishu-voice-sender | 语音消息发送 | ⏳ |
| 15 | feishu-video-sender | 视频消息发送 | ⏳ |
| 16 | feishu-card-parser | 卡片消息解析 | ⏳ |
| 17 | feishu-group-welcome | 新成员欢迎工具 | ⏳ |
| 18 | feishu-message-recall | 消息撤回工具 | ⏳ |

### 02-内容生成 (12个)

| # | 技能名称 | 功能描述 | 状态 |
|---|----------|----------|------|
| 19 | video-generation | AI视频生成（Hero/超分） | ⏳ |
| 20 | zhuoran-selfie | 卓然自拍照片生成 | ⏳ |
| 21 | zhuoran-video-selfie | 卓然自拍视频生成 | ⏳ |
| 22 | qizhuo-selfie | 奇卓自拍照片生成 | ⏳ |
| 23 | clawra-selfie | Clawra自拍照片生成 | ⏳ |
| 24 | clawra-video-selfie | Clawra自拍视频生成 | ⏳ |
| 25 | baoyu-slide-deck | 幻灯片生成 | ⏳ |
| 26 | long-form-writer | 长文生成器 | ⏳ |
| 27 | infographic-generator | 信息图生成 | ⏳ |
| 28 | md-to-wechat | Markdown转公众号 | ⏳ |
| 29 | voice-clone | 声音克隆 | ⏳ |
| 30 | daily-report | 早晚报生成 | ⏳ |

### 03-数据处理 (8个)

| # | 技能名称 | 功能描述 | 状态 |
|---|----------|----------|------|
| 31 | document-hub | 文档处理中心 | ⏳ |
| 32 | pdf | PDF处理工具 | ⏳ |
| 33 | image-ocr | 图片OCR识别 | ⏳ |
| 34 | content-extractor | 多平台内容抓取 | ⏳ |
| 35 | wechat-article-fetcher | 微信文章抓取 | ⏳ |
| 36 | twitter-scraper | Twitter/X抓取 | ⏳ |
| 37 | rss-feed | RSS订阅处理 | ⏳ |
| 38 | feishu-bitable-field | 多维表格字段管理 | ⏳ |

### 04-开发工具 (6个)

| # | 技能名称 | 功能描述 | 状态 |
|---|----------|----------|------|
| 39 | gh-cli | GitHub CLI完整指南 | ⏳ |
| 40 | remotion-best-practices | Remotion视频开发最佳实践 | ⏳ |
| 41 | calendar | Google Calendar集成 | ⏳ |
| 42 | find-skills | 技能发现工具 | ⏳ |
| 43 | feishu-doc | 飞书文档API工具 | ⏳ |
| 44 | smart-shopping | 智能购物助手 | ⏳ |

### 05-外部集成 (5个)

| # | 技能名称 | 功能描述 | 状态 |
|---|----------|----------|------|
| 45 | bright-data | Bright Data爬虫API | ⏳ |
| 46 | amap-navigator | 高德地图导航 | ⏳ |
| 47 | media_hub | 媒体处理中心 | ⏳ |
| 48 | whisper-stt | 本地语音转录 | ⏳ |
| 49 | logic-validator | 逻辑验证系统 | ⏳ |

### 06-AI Agent (4个)

| # | 技能名称 | 功能描述 | 状态 |
|---|----------|----------|------|
| 50 | security-hardening | 安全加固工具 | ⏳ |
| 51 | skill-security-audit | 技能安全审计 | ⏳ |
| 52 | secure-key-manager | 安全密钥管理 | ⏳ |
| 53 | security-drill | 安全演练工具 | ⏳ |

### 07-媒体处理 (5个)

| # | 技能名称 | 功能描述 | 状态 |
|---|----------|----------|------|
| 54 | media_hub/video_understanding | 视频理解 | ⏳ |
| 55 | media_hub/tts | 语音合成 | ⏳ |
| 56 | video-generation/scripts | 视频链生成 | ⏳ |
| 57 | zhuoran-video-selfie/assets | 垫图资源管理 | ⏳ |
| 58 | infographic-generator/templates | 提示词模板 | ⏳ |

### 08-安全工具 (4个)

| # | 技能名称 | 功能描述 | 状态 |
|---|----------|----------|------|
| 59 | security-hardening/install | 安全加固安装脚本 | ⏳ |
| 60 | security-hardening/verify | 安全验证工具 | ⏳ |
| 61 | skill-security-audit/audit | 技能审计脚本 | ⏳ |
| 62 | security-drill/SKILL | 安全演练流程 | ⏳ |

---

## 教程文档模板

每个教程文档包含以下章节：

```markdown
# [技能名称]

## 概述
- 功能简介
- 适用场景
- 依赖要求

## 安装配置
- 环境要求
- 安装步骤
- 配置文件

## 快速开始
- 最小可用示例
- 常用命令

## 详细用法
- 核心API/函数
- 参数说明
- 返回值

## 示例代码
- 基础示例
- 进阶示例
- 完整工作流

## 故障排除
- 常见问题
- 错误码说明
- 调试技巧

## 参考链接
- 源码路径
- 相关技能
- 外部文档
```

---

## 生成进度

- [ ] 创建项目结构 ✅
- [ ] 生成教程模板
- [ ] 批量生成62篇教程
- [ ] 上传到飞书知识库
- [ ] 创建总索引文档

---

**项目路径**: `~/.openclaw/workspace/skill-tutorials/`
**技能来源**: `/tmp/xiaozhua_skills_pack.zip` + `/tmp/skills_source.zip`
**教程数量**: 62个
**预计完成**: 持续更新中
