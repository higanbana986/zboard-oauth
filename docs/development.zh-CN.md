# 开发指南

[English](development.md) · **简体中文**

克隆 `https://github.com/higanbana986/zboard-oauth.git`，从仓库根目录开发，PR 目标为 `main`。

| 工具 | 要求 |
| --- | --- |
| Go | go.mod 指定的 1.26.8 |
| Node.js | CI 使用 22；本地至少 18 |
| Python | 3 |
| ZBoard 打包器 | 实现插件 SDK 和 `backend/tools/pluginpackager` 的源码版本 |

```sh
sh scripts/check.sh
python3 scripts/package.py --zboard /path/to/zboard --platform linux-amd64
```

检查包含格式、竞态测试、vet、gRPC 进程边界、浏览器行为、发行元数据和版本一致性。包内仅包含清单、签名、UI 和目标运行时。生成文件位于 `.build/`、`.local/` 和 `dist/`。

SDK 依赖锁定在 `go.mod`，默认检查使用 `GOWORK=off`。联合开发可以使用本地 SDK 工作区，但提交前须再用锁定依赖验证。

支持交叉构建 Linux amd64/arm64、macOS amd64/arm64 和 Windows amd64。交叉编译通过不代表目标平台运行已验收。签名和自动发布见[发布指南](publishing.zh-CN.md)。

成功推送到 `main` 后，Checks 运行页面的 Artifacts 区域会提供 `oauth-development-<提交号>`，包含五平台包、SHA-256 校验文件、临时开发公钥和测试说明，保留 14 天。仅上传公钥，不上传私钥。这些包仅用于隔离测试宿主，不能作为生产发行提交市场。PR 和正式发布前置检查仅构建 Linux amd64 开发包，不上传产物。

不传 `--key` 时，打包会自动创建并复用 `.local/publisher.key`。保留该密钥，使后续本地构建沿用同一签名身份。新版 ZBoard 打包工具将公钥附在安装包签名信息中，宿主首次导入时确认并保存此插件的信任。旧包可在导入弹窗的兼容选项中提供 `.pub` 公钥。正式发行仍支持显式指定 `--key` 和 `--key-id`。已发布版本不可覆盖，本次开发调整不替换 v0.0.1 产物。
