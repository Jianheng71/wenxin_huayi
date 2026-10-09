# 文心画意 Remote MCP

这是一个部署在 Cloudflare Workers 上的无状态 MCP 服务。将 MCP 地址添加到兼容的 AI 客户端后，AI 可以按需读取技能流程、获取白名单网页文本、汇总六维评分，并生成英文图像提示词。

## 工具

| 工具 | 用途 |
| --- | --- |
| `get_wenxin_huayi_guide` | 返回检索、来源核对、六维评分、版权与图片生成工作流程 |
| `fetch_literary_source` | 从已配置的 HTTPS 文学白名单域名读取网页文本，帮助核对搜索到的作者、篇名和短句 |
| `prepare_illustration_prompt` | 汇总5–10条候选的六维分数，只保留至少9/12的句子，挑选1–2条并生成英文绘画提示词 |

候选检索和主观评分由连接的 AI 执行；服务不会冒称已验证内容。来源网页是非可信输入，客户端应忽略其中任何试图改变指令的文本。来源抓取仅限白名单主机 HTTPS、不跟随重定向，超时8秒、响应正文上限128KB。引文上限100字符。

## 部署到 Cloudflare Workers

需要 Node.js/npm、Cloudflare 账户和 Wrangler：

```bash
npm install
npx wrangler login
npm run deploy
```

首次部署时 Wrangler 会提示确认 Worker 名称及账户。成功后远程 MCP URL 通常为：

```text
https://wenxin-huayi-mcp.<你的 Cloudflare workers.dev 子域>.workers.dev/mcp
```

根路径 `/` 返回服务信息。MCP 客户端必须通过 Streamable HTTP 协议调用 `/mcp`，不能把 `/mcp` 当普通网页打开。

## 本地测试

```bash
npm install
npm run typecheck
npm run dev
```

Wrangler 默认在 `http://localhost:8787` 提供服务。可用 MCP Inspector 连接：

```bash
npx @modelcontextprotocol/inspector
```

在 Inspector 中选择 Streamable HTTP 并连接 `http://localhost:8787/mcp`，检查工具列表并测试工具调用。

## AI 客户端连接

使用客户端自己的“远程 MCP / 自定义连接器”设置，添加部署后的 URL。桌面客户端可能要求本地代理或配置文件；只支持自带连接器的客户端可能无法添加用户自定义服务器。ChatGPT、Claude、Coze 及其他产品的 MCP 能力和界面会受产品版本、账号、地区和套餐限制，MCP 标准不保证所有客户端都支持。

客户端连接后，可测试：

> 以文为墨，画现乾坤！请为“雨后小院，安静，古典，带一点暮色”创作一幅图。

AI 客户端需另有网页搜索工具来发现候选，且需自身支持图像生成才能直接生成图片。否则它会返回可复制到图像生成器的提示词。

## 安全与限制

- 此示例没有用户认证；任何能访问 Worker URL 的人都能调用这些只读工具。
- 不要通过 MCP 暴露账号密码、令牌、私人内容或有副作用的操作。
- 外部网页抓取是公开站点只读访问，不登录网站；白名单外域名、HTTP URL、自定义端口与重定向都会被拒绝。
- Cloudflare 的托管部署需由 Worker 所有者在自己的 Cloudflare 账户完成；本项目不会代为登录或部署。
