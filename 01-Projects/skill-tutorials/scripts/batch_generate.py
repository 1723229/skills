#!/usr/bin/env python3
"""
批量生成技能教程文档
"""
import os
import json
from pathlib import Path

SKILL_CATEGORIES = {
    "01-feishu-ecosystem": [
        "feishu-doc-orchestrator", "feishu-wiki-orchestrator", "feishu-chat-extractor",
        "feishu-chat-monitor", "feishu-pdf-downloader", "feishu-doc-perm",
        "feishu-voice-sender", "feishu-video-sender", "feishu-card-parser",
        "feishu-group-welcome", "feishu-message-recall", "feishu-doc-converter",
        "feishu-doc-creator", "feishu-doc", "feishu-bitable-field"
    ],
    "02-content-generation": [
        "video-generation", "zhuoran-selfie", "zhuoran-video-selfie",
        "qizhuo-selfie", "clawra-selfie", "clawra-video-selfie",
        "baoyu-slide-deck", "long-form-writer", "infographic-generator",
        "md-to-wechat", "voice-clone", "daily-report", "meme-generator"
    ],
    "03-data-processing": [
        "document-hub", "pdf", "image-ocr",
        "content-extractor", "wechat-article-fetcher", "twitter-scraper",
        "rss-feed", "logic-validator"
    ],
    "04-dev-tools": [
        "gh-cli", "remotion-best-practices", "calendar",
        "find-skills", "feishu-doc", "smart-shopping"
    ],
    "05-external-integrations": [
        "bright-data", "amap-navigator", "media_hub",
        "whisper-stt"
    ],
    "06-ai-agents": [
        "security-hardening", "skill-security-audit",
        "secure-key-manager", "security-drill"
    ],
    "07-media": [
        "media_hub", "video-generation", "zhuoran-video-selfie"
    ],
    "08-security": [
        "security-hardening", "skill-security-audit",
        "secure-key-manager", "security-drill"
    ],
    "09-utilities": [
        "find-skills", "logic-validator"
    ]
}

TUTORIAL_TEMPLATE = """# {skill_name}

> {description}

---

## 概述

### 功能简介

{skill_name} 技能用于...（功能描述）

### 适用场景

- 场景1
- 场景2
- 场景3

### 依赖要求

- **Python版本**: 3.8+
- **依赖包**: requests
- **外部服务**: （如需要）

---

## 安装配置

### 安装步骤

```bash
cp -r skills/{skill_folder} ~/.openclaw/workspace/skills/
```

### 配置

（配置说明）

---

## 快速开始

### 使用方法

```bash
（使用命令）
```

---

## 详细用法

（详细说明）

---

## 示例代码

```python
# 基础示例
```

---

## 故障排除

### 常见问题

**Q1: 问题描述**

A: 解决方案

---

## 参考链接

- **源码路径**: `skills/{skill_folder}/`
- **SKILL.md**: `skills/{skill_folder}/SKILL.md`

---

*文档生成时间: 2026-02-27*
*自动生成: 待补充详细内容*
"""

def generate_tutorial(skill_name, category, output_dir):
    """生成单个教程文档"""
    skill_folder = skill_name
    description = f"{skill_name} 技能 - 待补充描述"
    
    # 读取原始 SKILL.md 如果有
    skill_md_path = Path(f"extracted/skills/{skill_name}/SKILL.md")
    if skill_md_path.exists():
        with open(skill_md_path) as f:
            content = f.read()
            # 提取描述
            if "description:" in content:
                desc_line = [l for l in content.split('\n') if 'description:' in l]
                if desc_line:
                    description = desc_line[0].split('description:')[1].strip()
    
    # 生成文档编号
    cat_skills = SKILL_CATEGORIES.get(category, [])
    if skill_name in cat_skills:
        idx = cat_skills.index(skill_name) + 1
        filename = f"{idx:02d}-{skill_name}.md"
    else:
        filename = f"{skill_name}.md"
    
    output_path = Path(output_dir) / category / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    content = TUTORIAL_TEMPLATE.format(
        skill_name=skill_name,
        skill_folder=skill_folder,
        description=description
    )
    
    with open(output_path, 'w') as f:
        f.write(content)
    
    return output_path

def main():
    base_dir = Path(__file__).parent.parent
    extracted_dir = base_dir / "extracted" / "skills"
    tutorials_dir = base_dir / "tutorials"
    
    # 获取所有技能文件夹
    all_skills = [d.name for d in extracted_dir.iterdir() if d.is_dir() and d.name != 'skills']
    
    generated = []
    for skill in all_skills:
        # 找到技能所属分类
        category = None
        for cat, skills in SKILL_CATEGORIES.items():
            if skill in skills:
                category = cat
                break
        
        if not category:
            category = "09-utilities"
        
        output_path = generate_tutorial(skill, category, tutorials_dir)
        generated.append(str(output_path))
    
    print(f"生成完成！共 {len(generated)} 个教程文档")
    print(f"输出目录: {tutorials_dir}")
    
    # 保存生成清单
    with open(base_dir / "generated_list.txt", 'w') as f:
        f.write('\n'.join(generated))

if __name__ == "__main__":
    main()
