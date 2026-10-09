# wenxin-huayi-skill

一个将文学原句转化为诗意、中国风与电影感图像提示词的 AI Skill：先检索并核实文学出处，再按六维画面感标准筛选高分句子，最后调用图像生成工具创作。提供 Claude、豆包、通义千问、Coze、Kimi、腾讯元宝和 ChatGPT 的独立部署包。

## 项目结构

```text
wenxin-huayi-skill/
├── README.md
├── SKILL.md
├── deploy.html
└── build_packages.py
```

项目无需下载语料、数据库或第三方依赖。构建器使用 Python 标准库生成各平台独立 ZIP 包。

## 构建与部署

运行：

```bash
python3 build_packages.py
```

生成的 `dist/` 包括七个独立 ZIP。打开 `deploy.html`，下载对应包并打开目标平台；每个 ZIP 都有平台专属部署说明和完整 `INSTRUCTIONS.md`。Claude 包另含标准 Skill 文件结构。触发短语为：**以文为墨，画现乾坤！**

部署需要用户在平台内登录、创建助手并粘贴指令或上传 Skill。当前各平台的导入接口、权限和发布流程不统一，本项目不会假称可从本地直接替用户发布，也不会收集账号凭据。ChatGPT 的 GPT 创建等能力可能受账号套餐和地区限制；若平台不支持自定义指令，可将指令作为每次对话的首条提示词。

`deploy.html` 是静态下载入口；部署到网页托管服务时，将此目录作为站点根目录发布即可。生成的 ZIP 必须与页面一起部署。

用户可以提供主题、情绪或构图偏好，例如：

- `以文为墨，画现乾坤！雨后小院，安静，古典，带一点暮色`
- `以文为墨，画现乾坤！江南烟雨，乌篷船与石桥，朦胧诗意`
- `以文为墨，画现乾坤！林黛玉的清冷与敏感，古典园林，含蓄的情绪`

Skill 会现搜5–10条候选，记录作者、篇名、原句和来源，按六个维度各0–2分评分。只保留总分至少9/12的句子，最终引用1–2句；若没有候选达标，则继续检索，不降低门槛。

## 文学来源与版权

优先检索白名单文学站点：`gushiwen.org`、`so.gushiwen.cn`、`shicimingju.com`、`sanwen.net`、`sanwen8.cn`、`365meiwen.com`、`purepen.com`、`guoxuedashi.com`。白名单无法访问或候选不足时，转向可核实的出版社、图书馆、高校、期刊等权威来源。对每条入选文本核实作者、篇名、原文与链接；优先选用公版作品。受版权保护的作品只使用必要的简短片段，不输出长篇摘录。

## 六维评分标准

完整标准、示例及评分切入点见 [`SKILL.md`](SKILL.md)：

1. 具象度与微观细节（Concreteness & Micro-Detailing）
2. 色彩光影与通感（Color, Lighting & Synesthesia）
3. 空间构图与镜头感（Spatial Layout & Camera Movement）
4. 动词精准度与动态捕捉（Precision of Verbs & Dynamic Capture）
5. 瞬间定格与戏剧张力（Temporal Freeze & Visual Tension）
6. 氛围隐喻与客体对应（Atmosphere & Objective Correlative）
