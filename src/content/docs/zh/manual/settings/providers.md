---
title: Provider 管理
description: Settings「Providers」面板操作手册：添加 / 编辑 / 删除推理服务提供方、测试连接、模型探测、后台执行逻辑。
---

# Provider 管理

「Providers」面板（菜单 key `environment`）用于配置**多个推理服务提供方（OpenAI 兼容接口）**：每个 Provider 一个卡片，可添加、编辑、删除并测试连接。激活的 Provider 会同步到配置 `api` 字段，成为任务执行与会话请求的转发目标。

## 1. 功能说明

- **多 Provider 并存**：可同时配置多个推理服务（如 Local vLLM、Remote SGLang），各页面通过 Provider 选择使用对应服务。
- **在线状态探测**：每个 Provider 卡片实时显示 在线 / 离线 状态与探测到的**模型列表**（模型 tag 可一键复制）。
- **激活与同步**：第一个添加的 Provider 自动激活；激活项的 `base_url` / `endpoint` / `api_key` / `extra_headers` 同步写入配置 `api` 字段（任务执行与会话代理统一读取 `api`）。
- **端点约定**：Provider 的 `endpoint` 默认为 `/v1/chat/completions`（探测模型时后端请求 `{base_url}/v1/models`）。

<div class="info">

**info**：BenchScope 的 API **不暴露** OpenAI 兼容的 `/v1/*` 推理端点；会话请求由后端代理转发到激活的 Provider。参考 [架构](/zh/docs/tools/architecture/) 与 [会话](/zh/docs/tools/sessions/)。

</div>

## 2. 页面结构

```
┌──────────────────────────────────────────────────────────┐
│ Providers                                  [Add Provider] │
│ 配置多个推理服务提供方（OpenAI 兼容接口）...（providersHint） │
├──────────────────────────────────────────────────────────┤
│ Provider 卡片（每个 Provider 一张）                        │
│  Local vLLM    ● 在线                           [删除]    │
│  ─────────────────────────────────────────────────────── │
│  Provider Name   [__________________________]            │
│  Base URL        [http://127.0.0.1:8000]                 │
│  API Key         [sk-...（密码框）]                       │
│  模型状态        ● 在线 / ○ 离线                          │
│  模型            [model-a] [model-b]（tag，图标可复制）     │
│  ─────────────────────────────────────────────────────── │
│                 [编辑 / 保存]      [测试连接]              │
└──────────────────────────────────────────────────────────┘
（空列表时显示：暂无 Provider，点击右上角 Add Provider 添加）
```

## 3. 输入参数

### 3.1 Add Provider 弹窗

| 字段 | 类型 | 限制 / 约束 | 默认值 | 说明 |
| --- | --- | --- | --- | --- |
| `name`（Provider Name） | 字符串 | **必填**，trim 后非空 | 空 | Provider 名称，如 Local vLLM / Remote SGLang |
| `base_url`（Base URL） | 字符串 | 可选；OpenAI 兼容服务地址 | 空（placeholder `http://127.0.0.1:8000`） | 推理服务 Base URL，末尾 `/` 由后端自动去除 |
| `api_key`（API Key） | 字符串 | 可选（密码框） | 空（placeholder `sk-...（可不填）`） | API Key；非空时探测请求带 `Authorization: Bearer <key>` |
| `endpoint` | 字符串 | 页面无输入框，后端默认 | `/v1/chat/completions` | 会话请求路径 |
| `extra_headers` | 对象 | 页面无输入框，后端默认 | `{}` | 额外请求头 |

### 3.2 Provider 卡片编辑字段

| 字段 | 类型 | 限制 / 约束 | 说明 |
| --- | --- | --- | --- |
| `name`（Provider Name） | 字符串 | 必填，trim 后非空 | 非编辑态只读，点击「编辑」解锁 |
| `base_url`（Base URL） | 字符串 | 可选 | 同上 |
| `api_key`（API Key） | 字符串 | 可选（密码框） | 同上 |

## 4. 操作步骤

### 4.1 添加 Provider

1. 左侧菜单点击「Providers」。
2. 点击面板右上角 **Add Provider** 按钮，打开添加弹窗（标题 Add Provider，提示「添加一个推理服务提供方（OpenAI 兼容接口）」）。
3. 填写 **Provider Name**（必填）、**Base URL**、**API Key**（可选）。
4. 点击弹窗底部 **保存** 按钮（`name` 为空时按钮禁用）；或 **取消** 关闭弹窗。
5. 添加成功后卡片列表刷新，并自动探测该 Provider 的在线状态与模型。

### 4.2 编辑与保存 Provider

1. 在目标 Provider 卡片底部点击 **编辑**（卡片字段解锁）。
2. 修改 Provider Name / Base URL / API Key。
3. 点击 **保存**：成功后自动重新探测该 Provider 状态。

### 4.3 测试连接

1. 点击 Provider 卡片底部的 **测试连接** 按钮（按钮进入 loading 状态）。
2. 探测成功：提示「连接成功」，卡片显示 在线 + 模型 tag 列表。
3. 探测失败：提示「连接失败」，卡片显示 离线、模型为空。

### 4.4 复制 / 删除 Provider

1. 复制模型：点击模型 tag 上的复制图标，模型名写入剪贴板。
2. 删除：点击卡片右上角 **删除**（红色）按钮，删除后列表刷新并重新探测。

## 5. 后台执行逻辑

### 5.1 页面加载与探测

1. `GET /api/config/providers` → 返回 `{providers: [...], active_provider: "..."}`。
2. 前端对**每个 Provider 并发**调用 `POST /api/config/test-connection`，body 为 `{base_url, endpoint, api_key, extra_headers}`。
3. 后端 `test_connection`：`requests.get("{base_url}/v1/models")`，`api_key` 非空时附加 `Authorization: Bearer <key>`，合并 `extra_headers`，**超时 6 秒**；成功返回 `{"ok": true, "models": [...]}`（模型 id 列表），异常返回 `{"ok": false, "error": "..."}`（error 截断 300 字符）。

### 5.2 添加 / 编辑 / 删除

| 操作 | API | 后端逻辑 |
| --- | --- | --- |
| 添加 | `POST /api/config/providers` | 校验 `name` 非空（否则 400）；生成 id `provider_<毫秒时间戳>`；**首个 Provider 自动激活**；`_sync_api_from_active` 把激活项写入配置 `api` 字段；落盘 settings.json |
| 编辑 | `PUT /api/config/providers/{id}` | 未知 id 返回 404；`name` 为空返回 400；若编辑的是激活项，重新同步 `api` 字段 |
| 删除 | `DELETE /api/config/providers/{id}` | 未知 id 返回 404；若删除的是激活项，**剩余第一个 Provider 自动激活**并同步 `api` 字段 |
| 激活 | `POST /api/config/providers/{id}` 的 `/activate` 子路由 | 切换 `active_provider` 并同步 `api` 字段（当前 Settings 页未提供按钮，可经 API 调用） |

### 5.3 配置同步链路

```
激活 Provider ──同步──▶ 配置 api 字段（base_url/endpoint/api_key/extra_headers）
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
        性能 / 精度任务执行         会话请求代理转发
```

配置持久化于 `~/.benchscope/settings.json`（`providers` 数组 + `active_provider` + `api` 字段）。

## 6. 常见问题

**问题：多个 Provider 中哪个生效？**

`active_provider` 指向的 Provider 生效：其 `base_url` / `endpoint` / `api_key` / `extra_headers` 同步到配置 `api` 字段，任务执行与会话请求都转发到它。当前版本添加的**第一个** Provider 自动激活，删除激活项时剩余第一个自动顶上。

**问题：测试连接失败（显示离线）怎么排查？**

依次确认：Base URL 可访问（`{base_url}/v1/models` 能返回 200）；API Key 正确（非空时带 Bearer 头）；网络可达（后端探测超时为 6 秒）。可用 `curl {base_url}/v1/models` 在服务器侧验证。

**问题：Provider 的模型列表从哪来？**

来自探测：后端请求 `{base_url}/v1/models`，把响应 `data[].id` 作为模型列表展示在卡片上；列表不代表 BenchScope 白名单，仅反映该服务当前可用的模型。