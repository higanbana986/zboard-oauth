# 发布指南

[English](publishing.md) · **简体中文**

每个 `vX.Y.Z` 标签只发布本插件，清单和运行时都必须报告 `X.Y.Z`。独立仓库的初始版本为 `v0.0.1`。

## 配置 Actions

创建名为 `release` 的环境，限制为已审核的发布标签，并设置：

| 配置 | 类型 | 内容 |
| --- | --- | --- |
| `PLUGIN_SIGNING_KEY` | 环境 Secret | Base64 Ed25519 私钥（编码前 64 字节） |
| `PLUGIN_PUBLISHER_ID` | 环境 Variable | 稳定发布者 ID，默认 `higanbana986` |
| `PLUGIN_PUBLIC_KEY` | 环境 Variable | 配套 Base64 Ed25519 公钥（32 字节） |

在安全位置使用 ZBoard 的 `pluginpackager -keygen` 生成密钥。私钥不进入 Git，公钥通过可信渠道分发。CI 开发密钥不得用于公开发行。

发布流程核对标签属于 main 历史，在不接触发布密钥的阶段运行检查，再构建五个平台包、验证元数据、生成校验文件和 `marketplace-entry.json`，最后发布 GitHub Release。已有发行版本不覆盖。失败的草稿发行保留以供检查；重试前删除不完整草稿。未配置签名参数时，创建标签不会成功发布。

## 触发发布

签名环境配置完成后，在 `main` 上选择已审核且清单与运行时版本一致的提交，初始发行版本为 `v0.0.1`。

- 从该提交创建 `release/v0.0.1` 分支，即可在没有既有标签时启动发布。检查与签名成功后，工作流在已验证的源码提交创建标签和 Release。
- 也可以推送对应的 `v0.0.1` 标签，或在 Actions → Release → Run workflow 中选择已审核的 main 提交或发行标签，并填写 `v0.0.1`。

工作流检出所选引用，校验它属于 main 历史，拒绝指向其他提交的既有标签及已存在的 Release。所有发布任务串行执行，并使用 `release` 环境。若环境限制了部署引用，需明确允许发布分支，或改用已获准的标签；工作流不会绕过环境规则。

Checks 产物是临时开发包，与正式签名 Release 产物分开。生产发布者密钥应跨版本保持稳定，以便宿主验证升级。

## 提交市场

从 Release 下载 `marketplace-entry.json`，使用[市场提交模板](https://github.com/zerodenet/plugins/issues/new?template=submit-plugin.yml)，并在独立 PR 中把插件条目提交到 `catalogs/zboard.json`。市场审核身份与公钥归属、验证安装包签名，并记录宿主和平台验收情况。插件发布流程不需要跨仓库写入 Token。

GitHub Release 下载地址有重定向。拒绝重定向的既有 ZBoard 版本需离线导入或使用兼容的直连镜像；市场收录本身不会改变宿主限制。

真实提供方登录和目标平台执行须单独记录，CI 不代表这些验收已完成。本工作流不提供 macOS 代码签名或公证。
