# 仓库开发规范

[English](AGENTS.md) · **简体中文**

OAuth 是独立插件。服务代码位于 `cmd/` 和 `internal/`，浏览器资源位于 `ui/`，测试不进入安装包。插件 ID 为 `zboard.oauth`，Go 模块为 `github.com/higanbana986/zboard-oauth`。

修改行为前阅读[贡献指南](CONTRIBUTING.zh-CN.md)、[开发指南](docs/development.zh-CN.md)和[架构边界](docs/governance.zh-CN.md)。账户、注册策略、凭据、权限和插件生命周期属于 ZBoard，禁止绕过专用宿主 API。

运行 `sh scripts/check.sh`；打包改动还须验证签名开发包。清单、运行时和文档版本必须同步更新。英文和简体中文文档保持一致。禁止提交私钥、凭据、生成包或本地工作区。

PR 统一提交到 `main`。从已审核主线创建独立的 SemVer 发布标签：开发版使用 `vX.Y.Z-dev.N`，候选版使用 `vX.Y.Z-rc.N`，正式版使用 `vX.Y.Z`。发布签名只在受保护的发布环境执行。市场只接收元数据，不复制插件源码。移动文件时保留作者与历史。
