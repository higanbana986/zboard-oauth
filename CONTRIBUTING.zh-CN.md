# 贡献指南

[English](CONTRIBUTING.md) · **简体中文**

报告可复现的 OAuth 问题时，提供插件版本、ZBoard 构建、提供方类型和脱敏日志。凭据或认证漏洞通过[安全政策](SECURITY.zh-CN.md)报告。

从 `main` 创建范围明确的工作分支。提供方行为变更应覆盖成功授权、身份拒绝、超时和宿主策略边界。提交 PR 前运行 `sh scripts/check.sh`，同时更新受影响指南的中英文版本。

安装包与运行时版本必须一致。源码构建和协议测试不代表真实提供方登录或系统代码签名已验证。请明确列出实际执行的检查。

独立签名发布后，使用 [ZeroDeNet 市场](https://github.com/zerodenet/plugins)的提交模板申请收录。OAuth 源码和发行包始终保留在本仓库。
