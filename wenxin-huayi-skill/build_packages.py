#!/usr/bin/env python3
"""Build self-contained import/instructions ZIPs for supported AI platforms."""

from __future__ import annotations

import re
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "dist"
SKILL_FILE = ROOT / "SKILL.md"

PLATFORMS = {
    "claude": {
        "name": "Claude",
        "url": "https://claude.ai/",
        "steps": (
            "在 Claude 的 Skills 管理界面选择创建/上传 Skill，将 ZIP 中的 "
            "`wenxin-huayi/SKILL.md` 与 `README.md` 放入同一目录后压缩上传。"
            "如果当前账号或界面没有 Skills 上传入口，可将 `INSTRUCTIONS.md` "
            "复制到项目指令中使用。"
        ),
    },
    "doubao": {
        "name": "豆包",
        "url": "https://www.doubao.com/",
        "steps": (
            "登录后创建可配置自定义指令的智能体/助手，将 `INSTRUCTIONS.md` "
            "内容粘贴到角色设定或系统指令中并保存。"
        ),
    },
    "qwen": {
        "name": "通义千问",
        "url": "https://www.qianwen.com/",
        "steps": (
            "登录后打开智能体/应用创建入口，将 `INSTRUCTIONS.md` 内容粘贴到"
            "角色设定或系统指令中并保存。若账号当前不提供自定义指令能力，"
            "可将其作为每次对话的首条提示词。"
        ),
    },
    "coze": {
        "name": "Coze / 扣子",
        "url": "https://www.coze.cn/",
        "steps": (
            "创建 Bot，在人设与回复逻辑/系统提示词中粘贴 `INSTRUCTIONS.md`。"
            "按需启用平台内的联网搜索和图像生成能力，再测试并发布。"
            "本包不伪造 Coze 的内部导入 DSL；DSL 和插件能力会随区域与版本变化。"
        ),
    },
    "kimi": {
        "name": "Kimi",
        "url": "https://www.kimi.com/",
        "steps": (
            "如果账号提供自定义智能体或指令入口，将 `INSTRUCTIONS.md` "
            "粘贴并保存；否则将文件内容作为新对话的首条提示词。"
        ),
    },
    "yuanbao": {
        "name": "腾讯元宝",
        "url": "https://yuanbao.tencent.com/",
        "steps": (
            "如果账号提供智能体创建或自定义指令入口，将 `INSTRUCTIONS.md` "
            "粘贴并保存；否则将文件内容作为新对话的首条提示词。"
        ),
    },
    "chatgpt": {
        "name": "ChatGPT",
        "url": "https://chatgpt.com/gpts/editor",
        "steps": (
            "在 GPT 编辑器创建 GPT，将 `INSTRUCTIONS.md` 内容粘贴到 Instructions。"
            "按需启用网页搜索和图像生成能力，测试后由用户自行保存/发布。"
            "创建 GPT 的功能可能受账号套餐和地区限制。"
        ),
    },
}


def instruction_text(skill_text: str) -> str:
    return re.sub(r"\A---\n.*?\n---\n*", "", skill_text, count=1, flags=re.DOTALL)


def make_readme(name: str, steps: str) -> str:
    return f"""# 文心画意 — {name} 部署包

此包包含完整技能指令和适用于 {name} 的部署说明。

## 部署

{steps}

1. 根据平台能力启用联网搜索和图像生成；若没有对应工具，助手应明确说明限制并提供提示词，不可声称已检索或生成图片。
2. 输入“以文为墨，画现乾坤！”并提供主题进行测试。

## 文件

- `INSTRUCTIONS.md`：可粘贴到平台自定义指令中的完整技能说明。
- Claude 包另含 `wenxin-huayi/SKILL.md` 和 `wenxin-huayi/README.md`，用于 Skill 上传。

## 注意

本包不会登录、调用账号 API 或代替用户发布。创建、保存和发布均由用户在平台界面完成；不要将账号密码或 API 密钥填入包内。
"""


def build() -> None:
    if not SKILL_FILE.is_file():
        raise FileNotFoundError(f"Missing skill definition: {SKILL_FILE}")

    skill = SKILL_FILE.read_text(encoding="utf-8")
    instructions = instruction_text(skill)
    OUTPUT.mkdir(exist_ok=True)

    for key, platform in PLATFORMS.items():
        archive = OUTPUT / f"wenxin-huayi-{key}.zip"
        with ZipFile(archive, "w", ZIP_DEFLATED) as bundle:
            bundle.writestr("INSTRUCTIONS.md", instructions)
            bundle.writestr(
                "README.md",
                make_readme(platform["name"], platform["steps"]),
            )
            if key == "claude":
                bundle.writestr("wenxin-huayi/SKILL.md", skill)
                bundle.writestr(
                    "wenxin-huayi/README.md",
                    "# wenxin-huayi\n\n"
                    "将此目录作为 Claude Skill 上传；技能详情见 `SKILL.md`。\n",
                )
        print(f"Created {archive.relative_to(ROOT)}")


if __name__ == "__main__":
    build()
