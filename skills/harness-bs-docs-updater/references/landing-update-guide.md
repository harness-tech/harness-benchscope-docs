# 官网落地页更新指南

本文档指导如何更新 benchscope-docs 官网（落地页）内容。

## 文件对应关系

| 屏 | 文件 | 内容 |
|---|---|---|
| 第 1 屏 | `src/components/ScreenIntro.astro` | 品牌介绍 + 打字效果 + CTA |
| 第 2 屏 | `src/components/ScreenFeatures.astro` | 功能 8 宫格 |
| 第 3 屏 | `src/components/ScreenPerf.astro` | 性能 4 子面板 |
| 第 4 屏 | `src/components/ScreenAccuracy.astro` | 精度 + 数据集 Tags |
| 第 5 屏 | `src/components/ScreenData.astro` | 4 Tab（RT / Statistics / PERF DATAS / LOGS） |
| 第 6 屏 | `src/components/ScreenAdvanced.astro` | 高级 6 宫格 |
| 第 7 屏 | `src/components/ScreenQuickStart.astro` | 五步引导 |

## 更新原则

1. **只改对应文件**：修改第 N 屏时，编辑对应的 `Screen*.astro`，不要在 `Landing.astro` 中直接修改
2. **双语同步**：每个组件内通过 `isEn` 条件定义中英文文案
3. **简洁有力**：每项功能描述 ≤ 2 行，避免冗长
4. **Mock 数据**：表格类预览使用真实格式 + mock 数值
5. **截图占位**：未获取到截图时用 `<!-- TODO -->` 标记

## 新增功能的处理

### 评估是否需要新屏幕

| 条件 | 处理方式 |
|---|---|
| 功能属于现有屏幕主题 | 扩展现有屏幕 |
| 功能是全新大类（≥3 个子功能） | 考虑新增屏幕 |
| 功能是小改进 | 更新对应屏幕描述即可 |

### 功能 8 宫格更新（第 2 屏）

```astro
// 在 ScreenFeatures.astro 的 features 数组中添加
{ i: 'iconName', t: '功能名', d: '一句话描述' },
```

图标从 `src/lib/icons.ts` 的 `ico()` 函数中选取。

### 性能子面板更新（第 3 屏）

表格数据使用 `ppv-table` 样式类，保持 8 列布局：
```astro
<table class="ppv-table ppv-rt">
  <thead><tr><th>Metric</th><th class="r">avg</th><th class="r">p99</th></tr></thead>
  <tbody>
    <tr><td>指标名</td><td class="r">数值</td><td class="r">数值</td></tr>
  </tbody>
</table>
```

## 截图规范

- 截图尺寸：≥ 1280×720
- 格式：PNG
- 命名：`benchscope-<页面>-<状态>.png`（如 `benchscope-performance_running.png`）
- 存放：`public/images/`
- 引用：`/images/benchscope-xxx.png`

## 设计约束

- 所有颜色使用 CSS 变量（`var(--gold)` / `var(--text-2)` 等）
- 全直角：`border-radius: 0`
- 图片默认灰色蒙版，hover 显示原图
- 按钮圆角 `6px`
- hover 微交互：`transform: translateY(-2px)` + 阴影
