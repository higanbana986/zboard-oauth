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
python3 scripts/package.py --zboard /path/to/zboard --dev-key --platform linux-amd64
```

检查包含格式、竞态测试、vet、gRPC 进程边界、浏览器行为、发行元数据和版本一致性。包内仅包含清单、签名、UI 和目标运行时。生成文件位于 `.build/`、`.local/` 和 `dist/`。

SDK 依赖锁定在 `go.mod`，默认检查使用 `GOWORK=off`。联合开发可以使用本地 SDK 工作区，但提交前须再用锁定依赖验证。

支持交叉构建 Linux amd64/arm64、macOS amd64/arm64 和 Windows amd64。交叉编译通过不代表目标平台运行已验收。签名和自动发布见[发布指南](publishing.zh-CN.md)。
