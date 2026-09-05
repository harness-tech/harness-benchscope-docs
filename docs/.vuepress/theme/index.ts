import { defaultTheme } from '@vuepress/theme-default'
import { getDirname, path } from '@vuepress/utils'
import type { Theme } from 'vuepress'

const __dirname = getDirname(import.meta.url)

/**
 * BenchScope 自定义主题：继承 defaultTheme，并注册「官网落地页」布局。
 * 落地页使用 layout: Landing；文档页使用 defaultTheme 的默认布局（白色导航 + 左侧目录 + 搜索）。
 */
export const benchscopeTheme = (options: any): Theme => ({
  name: 'benchscope-theme',
  extends: defaultTheme(options),
  layouts: {
    Landing: path.resolve(__dirname, 'layouts/Landing.vue'),
  },
})
