import { defineUserConfig } from 'vuepress'
import { viteBundler } from '@vuepress/bundler-vite'
import { defaultTheme } from '@vuepress/theme-default'
import { searchPlugin } from '@vuepress/plugin-search'

const DOC_SIDEBAR = [
  {
    text: '开始使用',
    collapsible: true,
    children: [
      '/docs/get-started/quickstart',
      '/docs/get-started/configuration',
      '/docs/get-started/cli',
      '/docs/get-started/update-uninstall',
    ],
  },
  {
    text: '核心能力',
    collapsible: true,
    children: [
      '/docs/core/performance',
      '/docs/core/accuracy',
      '/docs/core/sessions',
      '/docs/core/datas',
      '/docs/core/settings',
    ],
  },
  {
    text: '教程',
    collapsible: true,
    children: [
      '/docs/tutorials/perf-concurrency',
      '/docs/tutorials/perf-threshold',
      '/docs/tutorials/accuracy-guide',
    ],
  },
  {
    text: '更新说明',
    collapsible: true,
    children: [
      '/docs/changelog/v1-1-0',
      '/docs/changelog/v1-0-8',
      '/docs/changelog/v1-0-7',
      '/docs/changelog/v1-0-6',
      '/docs/changelog/v1-0-5',
    ],
  },
  {
    text: '开发指南',
    collapsible: true,
    children: [
      '/docs/development/architecture',
      '/docs/development/bench-engine',
      '/docs/development/contributing',
    ],
  },
]

export default defineUserConfig({
  lang: 'zh-CN',
  title: 'BenchScope',
  description: 'LLM 性能与精度可视化测试平台',
  base: '/',
  bundler: viteBundler({
    viteOptions: {
      css: { minify: false },
      build: { cssMinify: false },
    },
  }),
  theme: defaultTheme({
    logo: '/images/logo-gold.png',
    repo: 'https://github.com/LABELNET/benchscope',
    docsDir: 'docs',
    locales: {
      '/zh/': {
        lang: 'zh-CN',
        title: 'BenchScope',
        description: 'LLM 性能与精度可视化测试平台',
        selectLanguageName: '简体中文',
        navbar: [{ text: '官网', link: '/zh/' }],
        sidebar: {
          '/zh/docs/': DOC_SIDEBAR,
        },
      },
      '/en/': {
        lang: 'en-US',
        title: 'BenchScope',
        description: 'LLM inference performance & accuracy testing platform',
        selectLanguageName: 'English',
        navbar: [{ text: 'Home', link: '/en/' }],
        sidebar: {
          '/en/docs/': DOC_SIDEBAR,
        },
      },
    },
  }),
  locales: {
    '/zh/': { lang: 'zh-CN', title: 'BenchScope', description: 'LLM 性能与精度可视化测试平台' },
    '/en/': { lang: 'en-US', title: 'BenchScope', description: 'LLM inference testing platform' },
  },
  plugins: [
    searchPlugin({
      locales: {
        '/zh/': { placeholder: '搜索文档' },
        '/en/': { placeholder: 'Search' },
      },
    }),
  ],
})
