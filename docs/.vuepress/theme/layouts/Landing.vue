<script setup lang="ts">
import { useRoute } from 'vue-router'
import { computed } from 'vue'

const route = useRoute()
const isEn = computed(() => route.path.startsWith('/en/'))
const prefix = computed(() => (isEn.value ? '/en' : '/zh'))
const docs = computed(() => `${prefix.value}/docs/get-started/quickstart`)

const t = {
  en: {
    navHome: 'Home', navFeatures: 'Features', navPerf: 'Performance',
    navAcc: 'Accuracy', navQuick: 'Quick Start', docsBtn: 'Docs',
    heroTitle1: 'Built for LLM inference',
    heroTitleGold: 'Visual Testing Platform',
    heroSub: 'BenchScope is an open-source LLM benchmarking platform that stress-tests throughput & latency of inference services and runs accuracy evaluation on model outputs; supports vLLM / SGLang and any OpenAI-compatible API.',
    featuresKicker: 'Features', featuresTitle: 'A complete capability, out of the box',
    featuresLead: 'From install to report in one command.',
    perfKicker: 'Performance', perfTitle: 'Performance Testing',
    perfLead: 'Load-test OpenAI-compatible services or vLLM / SGLang backends.',
    accKicker: 'Accuracy', accTitle: 'Accuracy Testing',
    accLead: 'Built-in datasets and scorers evaluate output quality against baselines.',
    quickTitle: 'Up and running in 30 seconds',
    quickInstall: '# Install', quickStart: '# Start the web platform', quickOpt: '# Common options',
    quickHint: 'See Quick Start, Configuration and CLI Reference.',
    footerBrand: 'BenchScope — LLM performance & accuracy testing platform',
    copyright: 'HarnessTek', langLabel: '中文',
    gh: 'GitHub',
  },
  zh: {
    navHome: '首页', navFeatures: '功能', navPerf: '性能测试',
    navAcc: '精度测试', navQuick: '快速开始', docsBtn: '文档',
    heroTitle1: '为 LLM 推理而生',
    heroTitleGold: '可视化测试平台',
    heroSub: 'BenchScope 是一个开源的大模型推理测试平台 —— 一键压测推理服务的吞吐与延迟，并对模型输出做精度评测；支持 vLLM / SGLang 及任意 OpenAI 兼容 API。',
    featuresKicker: 'Features', featuresTitle: '开箱即用的完整能力',
    featuresLead: '从安装到出报告，一条命令完成。',
    perfKicker: 'Performance', perfTitle: '性能测试',
    perfLead: '对 OpenAI 兼容推理服务或 vLLM / SGLang 后端进行压测。',
    accKicker: 'Accuracy', accTitle: '精度测试',
    accLead: '内置多种评测数据集与判分器，对模型输出质量做量化评估并与基线对标。',
    quickTitle: '30 秒上手',
    quickInstall: '# 安装', quickStart: '# 启动 Web 平台', quickOpt: '# 常用选项',
    quickHint: '详见快速入门、配置说明与 CLI 参考。',
    footerBrand: 'BenchScope — 大模型推理性能 & 精度测试平台',
    copyright: 'HarnessTek', langLabel: 'English',
    gh: 'GitHub',
  },
}[isEn.value ? 'en' : 'zh'] as any
</script>

<template>
  <div class="ln-root">
    <header class="ln-header">
      <div class="ln-header-in">
        <a class="ln-brand" href="#home"><img class="ln-logo" src="/images/logo-gold.png" alt="BenchScope"><span>BenchScope</span></a>
        <nav class="ln-nav">
          <a href="#home">{{ t.navHome }}</a>
          <a href="#features">{{ t.navFeatures }}</a>
          <a href="#performance">{{ t.navPerf }}</a>
          <a href="#accuracy">{{ t.navAcc }}</a>
          <a href="#quickstart">{{ t.navQuick }}</a>
        </nav>
        <div class="ln-actions">
          <a class="ln-gh" :href="'https://github.com/LABELNET/benchscope'" target="_blank" rel="noopener" :title="'GitHub'">
            <svg viewBox="0 0 16 16" width="20" height="20" fill="currentColor"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8Z"/></svg>
          </a>
          <a class="ln-docs" :href="docs">{{ t.docsBtn }}</a>
          <a class="ln-lang" :href="isEn ? '/zh/' : '/en/'" hreflang="zh">{{ t.langLabel }}</a>
        </div>
      </div>
    </header>

    <section id="home" class="ln-section ln-home">
      <div class="ln-wrap">
        <h1 class="ln-h1">{{ t.heroTitle1 }}<br><span class="ln-gold">{{ t.heroTitleGold }}</span></h1>
        <p class="ln-sub">{{ t.heroSub }}</p>
        <div class="ln-cta">
          <a class="ln-btn ln-primary" :href="docs">{{ t.docsBtn }}</a>
          <a class="ln-btn ln-ghost" href="#quickstart">{{ t.navQuick }}</a>
        </div>
        <div class="ln-tags"><span class="ln-tag">pip install benchscope</span><span class="ln-tag">vLLM · SGLang · OpenAI</span><span class="ln-tag">Apache 2.0</span><span class="ln-tag">Real-time</span></div>
        <img class="ln-shot" src="/images/benchscope-performance_default.png" alt="BenchScope UI">
      </div>
    </section>

    <section id="features" class="ln-section">
      <div class="ln-wrap">
        <p class="ln-kicker">{{ t.featuresKicker }}</p>
        <h2 class="ln-title">{{ t.featuresTitle }}</h2>
        <p class="ln-lead">{{ t.featuresLead }}</p>
        <div class="ln-grid">
          <div class="ln-card"><div class="ln-ico">⚡</div><h3>{{ (isEn ? 'Easy install' : '安装简单') }}</h3><p>{{ (isEn ? 'pip install benchscope then a single command starts the whole web platform.' : 'pip install benchscope，随后一条命令即可启动整个 Web 平台。') }}</p></div>
          <div class="ln-card"><div class="ln-ico">📊</div><h3>{{ (isEn ? 'Dual-mode performance' : '性能测试双模式') }}</h3><p>{{ (isEn ? 'Concurrency load testing and Threshold probing.' : '并发压测与阈值探测双模式。') }}</p></div>
          <div class="ln-card"><div class="ln-ico">🎯</div><h3>{{ (isEn ? 'Dual-mode accuracy' : '精度测试双模式') }}</h3><p>{{ (isEn ? 'Native (local weights) and Serving (OpenAI-compatible) evaluation.' : '原生与服务双模式评测。') }}</p></div>
          <div class="ln-card"><div class="ln-ico">🔄</div><h3>{{ (isEn ? 'Real-time feedback' : '实时数据反馈') }}</h3><p>{{ (isEn ? 'Every concurrency result streams live into tables, charts and progress.' : '每个并发结果实时流入表格、曲线与进度。') }}</p></div>
          <div class="ln-card"><div class="ln-ico">📈</div><h3>{{ (isEn ? 'Visualization charts' : '可视化曲线') }}</h3><p>{{ (isEn ? 'Throughput / TTFT / TPOT / ITL multi-dimensional charts.' : '吞吐 / TTFT / TPOT / ITL 多维统计图。') }}</p></div>
          <div class="ln-card"><div class="ln-ico">💾</div><h3>{{ (isEn ? 'Log cache &amp; download' : '日志缓存下载') }}</h3><p>{{ (isEn ? 'Run logs, mean / P99 summaries and Excel export.' : '运行日志、mean / P99 汇总与 Excel 导出。') }}</p></div>
        </div>
      </div>
    </section>

    <section id="performance" class="ln-section">
      <div class="ln-wrap">
        <p class="ln-kicker">{{ t.perfKicker }}</p>
        <h2 class="ln-title">{{ t.perfTitle }}</h2>
        <p class="ln-lead">{{ t.perfLead }}</p>
        <div class="ln-pair">
          <div class="ln-mode"><h3>{{ (isEn ? 'Concurrency Mode' : '并发压测') }}</h3><p>{{ (isEn ? 'Apply multiple concurrency levels and record each level\u2019s metrics in real time.' : '固定多个并发级别逐级施压，实时记录每个并发的指标。') }}</p> <img src="/images/benchscope-performance_perf_running.png" alt="concurrency"></div>
          <div class="ln-mode"><h3>{{ (isEn ? 'Threshold Mode' : '阈值探测') }}</h3><p>{{ (isEn ? 'Auto-search the max concurrency meeting your threshold.' : '自动搜寻满足阈值条件的最大并发。') }}</p> <img src="/images/benchscope-performance_perf_running_statistics.png" alt="threshold"></div>
        </div>
      </div>
    </section>

    <section id="accuracy" class="ln-section">
      <div class="ln-wrap">
        <p class="ln-kicker">{{ t.accKicker }}</p>
        <h2 class="ln-title">{{ t.accTitle }}</h2>
        <p class="ln-lead">{{ t.accLead }}</p>
        <div class="ln-pair">
          <div class="ln-mode"><h3>{{ (isEn ? 'Native' : '原生模式') }}</h3><p>{{ (isEn ? 'Load local weights / HF id and evaluate offline.' : '直接加载本地权重离线评测。') }}</p> <img src="/images/benchscope-accuracy_default.png" alt="native"></div>
          <div class="ln-mode"><h3>{{ (isEn ? 'Serving' : '服务模式') }}</h3><p>{{ (isEn ? 'Evaluate a deployed service through the OpenAI-compatible link.' : '通过 OpenAI 兼容链路评测已部署服务。') }}</p> <img src="/images/benchscope-accuracy_default.png" alt="serving"></div>
        </div>
      </div>
    </section>

    <section id="quickstart" class="ln-section ln-quick">
      <div class="ln-wrap">
        <p class="ln-kicker">Quick Start</p>
        <h2 class="ln-title">{{ t.quickTitle }}</h2>
        <pre class="ln-code"><span class="ln-c">{{ t.quickInstall }}</span>
<span class="ln-v">pip install benchscope</span>

<span class="ln-c">{{ t.quickStart }}</span>
<span class="ln-v">benchscope</span>

<span class="ln-c">{{ t.quickOpt }}</span>
<span class="ln-v">benchscope --port 8080 --no-browser</span></pre>
        <p class="ln-hint">→ <a :href="docs">{{ (isEn ? 'Read the documentation' : '阅读文档') }}</a></p>
      </div>
    </section>

    <footer class="ln-footer">
      <div class="ln-wrap">
        <div class="ln-fnav">
          <a href="#home">{{ t.navHome }}</a>
          <a href="#features">{{ t.navFeatures }}</a>
          <a href="#performance">{{ t.navPerf }}</a>
          <a href="#accuracy">{{ t.navAcc }}</a>
          <a href="#quickstart">{{ t.navQuick }}</a>
          <a :href="docs">{{ t.docsBtn }}</a>
        </div>
        <div class="ln-flegal">© 2026 <a href="https://www.harness-tech.com" target="_blank" rel="noopener">{{ t.copyright }}</a> · Apache License 2.0</div>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.ln-root{font-family:'PingFang SC','Hiragino Sans GB','Microsoft YaHei','Noto Sans SC',system-ui,sans-serif;color:#23201a;background:#fff;min-height:100vh}
.ln-header{position:sticky;top:0;z-index:90;background:#16130d;box-shadow:0 2px 14px rgba(0,0,0,.28)}
.ln-header-in{max-width:1180px;margin:0 auto;padding:0 20px;height:62px;display:flex;align-items:center;gap:28px}
.ln-brand{display:flex;align-items:center;gap:10px;color:#e9e2cf;font-weight:700;font-size:18px;text-decoration:none;margin-right:auto}
.ln-logo{height:34px;width:34px;border-radius:8px}
.ln-nav{display:flex;gap:4px}
.ln-nav a{color:#9f967f;text-decoration:none;padding:8px 12px;border-radius:8px;font-size:14.5px;transition:.15s}
.ln-nav a:hover{color:#c8a24a;background:rgba(200,162,74,.12)}
.ln-actions{display:flex;align-items:center;gap:12px}
.ln-gh{color:#e9e2cf;display:inline-flex}
.ln-gh:hover{color:#c8a24a}
.ln-docs{color:#4a3a12;background:#c8a24a;text-decoration:none;padding:7px 16px;border-radius:999px;font-weight:600;font-size:14px}
.ln-docs:hover{background:#b08a34;color:#fff}
.ln-lang{color:#9f967f;text-decoration:none;font-size:13px}
.ln-lang:hover{color:#c8a24a}
.ln-section{min-height:100vh;display:flex;align-items:center;padding:72px 20px 56px;scroll-margin-top:62px}
.ln-wrap{max-width:1080px;margin:0 auto;width:100%}
.ln-home{background:radial-gradient(1200px 600px at 85% -10%,rgba(200,162,74,.18),transparent 60%),linear-gradient(180deg,#1c1810,#16130d);color:#eee6d2;min-height:calc(100vh - 62px)}
.ln-h1{font-size:clamp(34px,6vw,56px);font-weight:800;margin:0 0 16px;color:#fff}
.ln-gold{color:#c8a24a}
.ln-sub{font-size:clamp(16px,2vw,20px);color:#cfc5a8;max-width:720px;line-height:1.8;margin:0 0 30px}
.ln-cta{display:flex;gap:14px;margin-bottom:34px}
.ln-btn{display:inline-block;padding:13px 26px;border-radius:999px;font-weight:600;text-decoration:none}
.ln-primary{background:#c8a24a;color:#4a3a12}
.ln-primary:hover{background:#b08a34;color:#fff}
.ln-ghost{border:1px solid rgba(200,162,74,.6);color:#c8a24a}
.ln-ghost:hover{background:rgba(200,162,74,.12)}
.ln-tags{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:30px}
.ln-tag{font-size:12.5px;padding:6px 12px;border-radius:999px;background:rgba(200,162,74,.12);border:1px solid rgba(200,162,74,.35);color:#c8a24a}
.ln-shot{max-width:880px;width:100%;border:1px solid rgba(200,162,74,.35);border-radius:16px;box-shadow:0 24px 60px rgba(0,0,0,.5)}
.ln-kicker{font-size:14px;letter-spacing:2px;text-transform:uppercase;color:#b08a34;font-weight:700;margin:0 0 8px}
.ln-title{font-size:clamp(26px,4vw,40px);font-weight:800;margin:0 0 14px}
.ln-lead{font-size:17px;color:#5a564d;max-width:720px;line-height:1.8;margin:0 0 30px}
.ln-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:18px}
.ln-card{background:#fff;border:1px solid #e8e2d3;border-radius:14px;padding:22px;box-shadow:0 6px 18px rgba(196,170,110,.08);transition:.18s}
.ln-card:hover{transform:translateY(-4px);box-shadow:0 14px 30px rgba(196,170,110,.16);border-color:#c8a24a}
.ln-ico{width:46px;height:46px;border-radius:12px;display:flex;align-items:center;justify-content:center;background:#f6edd9;color:#b08a34;margin-bottom:14px;font-size:22px}
.ln-card h3{margin:0 0 8px;font-size:17px}
.ln-card p{margin:0;color:#5a564d;font-size:14px;line-height:1.7}
.ln-pair{display:grid;grid-template-columns:1fr 1fr;gap:22px}
.ln-mode{background:#fff;border:1px solid #e8e2d3;border-radius:16px;padding:26px;box-shadow:0 8px 24px rgba(196,170,110,.08)}
.ln-mode h3{margin:0 0 10px;font-size:19px;color:#b08a34}
.ln-mode p{color:#5a564d;font-size:14.5px;line-height:1.8;margin:0 0 16px}
.ln-mode img{width:100%;border-radius:10px;border:1px solid #e8e2d3}
.ln-quick{background:#faf8f3}
.ln-code{background:#1d1a13;color:#e9e2cf;border-radius:14px;padding:22px 24px;font-family:'SF Mono','JetBrains Mono',Menlo,Consolas,monospace;font-size:14px;line-height:1.8;overflow:auto;margin:0 0 14px}
.ln-c{color:#c8a24a}
.ln-v{color:#9ecb7b}
.ln-hint{color:#5a564d;font-size:14px}
.ln-hint a{color:#b08a34}
.ln-footer{background:#16130d;color:#9f967f;padding:36px 20px 28px}
.ln-fnav{display:flex;flex-wrap:wrap;gap:8px 18px;margin-bottom:16px}
.ln-fnav a{color:#9f967f;text-decoration:none;font-size:13.5px}
.ln-fnav a:hover{color:#c8a24a}
.ln-flegal{font-size:13px}
.ln-flegal a{color:#c8a24a;text-decoration:none}
@media(max-width:860px){.ln-pair{grid-template-columns:1fr}.ln-nav{display:none}}
</style>
