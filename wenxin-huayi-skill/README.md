# wenxin-huayi-skill

一个将文学原句转化为诗意、中国风与电影感图像提示词的 AI Skill：先检索并核实文学出处，再按六维画面感标准筛选高分句子，最后调用图像生成工具创作。提供 Claude、豆包、通义千问、Coze、Kimi、腾讯元宝和 ChatGPT 的独立部署包。

## 项目结构

```text
wenxin-huayi-skill/
├── README.md
├── SKILL.md
├── deploy.html
├── build_packages.py
└── mcp-server/
    ├── README.md
    ├── package.json
    ├── wrangler.toml
    └── src/index.ts
```

无需下载语料或数据库。平台 ZIP 构建器只使用 Python 标准库；MCP 服务使用下方 `mcp-server/` 中的 npm 依赖。

## 构建与部署

运行：

```bash
python3 build_packages.py
```

生成的 `dist/` 包括七个独立 ZIP。打开 `deploy.html`，下载对应包并打开目标平台；每个 ZIP 都有平台专属部署说明和完整 `INSTRUCTIONS.md`。Claude 包另含标准 Skill 文件结构。触发短语为：**以文为墨，画现乾坤！**

部署需要用户在平台内登录、创建助手并粘贴指令或上传 Skill。当前各平台的导入接口、权限和发布流程不统一，本项目不会假称可从本地直接替用户发布，也不会收集账号凭据。ChatGPT 的 GPT 创建等能力可能受账号套餐和地区限制；若平台不支持自定义指令，可将指令作为每次对话的首条提示词。

`deploy.html` 是静态下载入口；部署到网页托管服务时，将此目录作为站点根目录发布即可。生成的 ZIP 必须与页面一起部署。

## MCP 服务部署（连接一次，后续由 AI 调用）

项目还提供 Cloudflare Workers 上的无状态远程 MCP 服务。连接成功后，兼容 MCP 的 AI 客户端可以调用文学流程指南、白名单来源抓取、六维评分汇总和英文绘画提示词整理工具。MCP 不会绕过平台权限自动安装，也不代表七个平台都支持远程 MCP；用户需要先在目标 AI 的连接器/工具设置中添加 MCP 地址。AI 平台仍需提供网页搜索以发现候选；是否能生成图片取决于该平台自身的图像工具。

在 Cloudflare 账户部署：

```bash
cd mcp-server
npm install
npx wrangler login
npm run deploy
```

部署后地址形如 `https://wenxin-huayi-mcp.<你的 Cloudflare 子域>.workers.dev/mcp`。将该地址添加到 AI 客户端的远程 MCP 连接设置中；连接成功后测试调用 `get_wenxin_huayi_guide`。部分只支持本地 MCP 配置的客户端需要本机代理（如 `mcp-remote`）；有些客户端暂不支持用户自定义 MCP。发布者需自行管理 Cloudflare 账户和部署权限。

服务只开放只读白名单网页抓取和提示词整理，不登录文学网站、不访问白名单外地址、不跟随重定向，也不调用图像生成 API。来源抓取有8秒超时和128KB上限。该 MCP endpoint 不要求用户身份验证，不应添加私密数据、写操作或账号密钥；公开部署后任何人都能调用这些公开能力。

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
