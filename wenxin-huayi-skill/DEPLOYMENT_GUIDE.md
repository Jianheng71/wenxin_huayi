# 文心画意 MCP 部署说明书

本说明带你把文心画意 MCP 服务部署到 Cloudflare Workers，并连接到支持远程 MCP 的 AI 客户端。部署完成后，AI 可调用白名单网页抓取和提示词整理工具。

> **先看清楚：**这不是把一句 API 粘到普通聊天框就自动安装。需要部署一次服务，再到 AI 客户端的 MCP/连接器设置中添加地址。只有支持自定义远程 MCP（Streamable HTTP）的客户端才能连接；不是所有 AI 平台都支持。

## 一、先准备

- 一个 Cloudflare 账户。免费账户可以用于 `workers.dev` 入门部署。
- 一台 Mac 和网络连接。
- Node.js 与 npm。打开“终端”运行：

  ```bash
  node -v
  npm -v
  ```

  如果显示版本号，例如 `v24.21.0`，就可以继续。若提示找不到命令，请先从 [nodejs.org](https://nodejs.org/) 安装 LTS 版 Node.js，然后重新打开终端。

- 已合并到 GitHub `main` 的 MCP 服务代码。若仓库文件列表中有 `wenxin-huayi-skill/mcp-server/` 目录，说明代码已在仓库中。

## 二、在 Cloudflare 设置 workers.dev 子域名

`workers.dev` 是 Cloudflare 提供的测试/个人项目域名，不必购买域名或手工设置 DNS。

1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com/)。
2. 选择要用于部署的账户。
3. 打开 **Workers & Pages**（Workers 和 Pages）页面。
4. 在 **Overview**（概览）中找到 **Your subdomain**。若尚未设置，选择 **Set up a workers.dev subdomain**；若已有子域名，旁边会显示当前名称，并可通过 **Change** 更改。
5. 输入一个可用名称并确认。例如名称是 `myname`，子域名就是 `myname.workers.dev`。

如果菜单或按钮名称不同，可直接打开 [Workers & Pages 控制台](https://dash.cloudflare.com/?to=/:account/workers-and-pages)，并在 Overview 页面查找 **workers.dev**。此设置是账户级的，不是在普通 DNS 页面添加记录。

## 三、打开 Mac 终端

1. 按键盘 **Command ⌘ + 空格**打开 Spotlight。
2. 输入“终端”或 `Terminal`。
3. 按回车打开终端。

命令需逐行粘贴并按回车执行。不要输入命令前的 `$` 或代码块符号。

## 四、下载代码并安装依赖

在终端运行：

```bash
git clone https://github.com/Jianheng71/wenxin_huayi.git
cd wenxin_huayi/wenxin-huayi-skill/mcp-server
npm ci
```

`npm ci` 最后显示 `found 0 vulnerabilities` 且回到命令提示符，通常表示依赖安装成功。`npm warn install-scripts` 提示某些依赖包含安装脚本，不等同于安装失败；本项目无需为此运行 `npm install-scripts approve`。如果提示目标目录已存在，不要重复克隆；进入已有仓库后执行：

```bash
cd wenxin_huayi
git pull
cd wenxin-huayi-skill/mcp-server
npm ci
```

## 五、登录并部署 Worker

先运行：

```bash
npx wrangler login
```

浏览器会打开 Cloudflare 授权页面。确认登录的是设置了 `workers.dev` 子域名的 Cloudflare 账户，再点击授权。成功后终端会显示 `Successfully logged in.`。

然后运行：

```bash
npm run deploy
```

如果询问部署到账户，选择正确账户。成功时会显示类似：

```text
Deployed wenxin-huayi-mcp triggers
https://wenxin-huayi-mcp.你的子域名.workers.dev
```

最终 MCP 地址是在 Worker 根地址后加 `/mcp`，例如：

```text
https://wenxin-huayi-mcp.myname.workers.dev/mcp
```

请使用终端实际打印出来的地址和子域名，不要照抄示例。

## 六、验证服务已上线

把下面的命令中的根地址替换成 Wrangler 输出的 Worker 地址（不要带 `/mcp`），运行：

```bash
curl https://wenxin-huayi-mcp.myname.workers.dev/
```

如果返回包含以下信息的 JSON，表示 Worker 在线：

```json
{"name":"wenxin-huayi-mcp","endpoint":"/mcp","transport":"Streamable HTTP"}
```

浏览器直接打开 `/mcp` 可能不会显示网页，这是正常的：该地址需要由 MCP 客户端使用 Streamable HTTP 协议调用。

## 七、连接 AI 客户端

1. 打开 AI 客户端设置，寻找 **MCP**、**Apps / Connectors**、**开发者模式**或“自定义连接器”入口。
2. 选择添加远程 MCP 服务，传输方式选 **Streamable HTTP**（若客户端自动识别则无需选择）。
3. 粘贴完整 `/mcp` 地址并保存/连接。
4. 检查工具列表是否出现：
   - `get_wenxin_huayi_guide`
   - `fetch_literary_source`
   - `prepare_illustration_prompt`
5. 在新对话中测试：

   > 以文为墨，画现乾坤！请为“雨后小院，安静，古典，带一点暮色”创作一幅图。

有些桌面应用要求重启客户端，或要求本地 MCP 代理；以该客户端的官方说明为准。不同 AI 平台的支持情况、权限、套餐和设置菜单不同；如果设置中没有自定义远程 MCP 入口，就不能直接连接此地址。MCP 只提供服务工具，不能替平台添加原生 Skill。

Grok 网页/应用目前不能确认支持用户直接添加任意远程 MCP 地址。xAI API 可以通过自定义函数调用集成工具，但需要自行编写应用/桥接程序，不是把 MCP URL 粘贴进 Grok 聊天框即可使用。

## 八、重要安全与功能限制

- 当前 Worker **没有用户认证**。任何获得 `/mcp` 地址的人都可以调用公开的只读工具。
- 不要把密码、API 密钥、私人资料或机密文本发给该服务，也不要在公开页面张贴地址并将其当作私有凭证。
- 来源抓取限制在代码配置的 HTTPS 白名单主机，不跟随重定向；服务不会登录文学网站。
- 该 MCP 不负责网页搜索发现候选，也不负责生成图片。AI 客户端需要另外提供网页搜索能力；直接生成图片则要求客户端有图像生成工具。否则 AI 只能整理出可复制使用的提示词。
- `workers.dev` 面向入门、测试和个人项目。Cloudflare 账户所有者负责管理服务、更新代码和决定是否继续公开。

## 更新或停止服务

更新代码并重新部署：

```bash
cd wenxin_huayi
git pull
cd wenxin-huayi-skill/mcp-server
npm ci
npm run deploy
```

若需要停止服务，可在 Cloudflare Dashboard 的 **Workers & Pages** 中打开 `wenxin-huayi-mcp` Worker，并在其设置/管理界面删除该 Worker 或关闭 `workers.dev` 路由。删除 Worker 会让所有已连接客户端无法继续使用；操作前确认选中的是正确 Worker。
