import { getCollection } from 'astro:content'

export interface LinkItem { id: string; href: string; title: string }
export interface Group { label: string; children: LinkItem[] }

export const LABELS: Record<string, { zh: string; en: string }> = {
  quickstart: { zh: '快速开始', en: 'Quick Start' },
  install: { zh: '安装', en: 'Install' },
  accuracy: { zh: '精度', en: 'Accuracy' },
  performance: { zh: '性能', en: 'Performance' },
  data: { zh: '数据', en: 'Data' },
  tools: { zh: '工具（高级）', en: 'Tools' },
  cli: { zh: 'CLI', en: 'CLI' },
  api: { zh: 'API', en: 'API' },
  releases: { zh: '发布', en: 'Releases' },
  help: { zh: '帮助', en: 'Help' },
}
export const ORDER = ['quickstart', 'install', 'accuracy', 'performance', 'data', 'tools', 'cli', 'api', 'releases', 'help']

export async function buildSidebar(lang: 'zh' | 'en') {
  const all = await getCollection('docs', (e) => e.id.startsWith(`${lang}/`) && !e.id.toLowerCase().endsWith('/readme'))
  const isEn = lang === 'en'

  const groups: Group[] = ORDER.map((p) => {
    // `dir/index.md` -> id === `${lang}/${p}`（Astro 把 index 折叠为目录根 id）
    const landing = all.find((e) => e.id === `${lang}/${p}`)
    const landingItem = landing
      ? { id: landing.id, href: `/${lang}/docs/${p}/`, title: landing.data.title || p }
      : null
    const items = all
      .filter((e) => e.id.startsWith(`${lang}/${p}/`))
      .map((e) => {
        const rest = e.id.slice(`${lang}/${p}/`.length)
        const title = e.data.title || rest.replace(/[-_]/g, ' ')
        return { id: e.id, href: `/${lang}/docs/${p}/${rest}/`, title }
      })
      .sort((a, b) => a.title.localeCompare(b.title, isEn ? 'en' : 'zh'))
    return { label: LABELS[p][lang], children: landingItem ? [landingItem, ...items] : items }
  })

  // 扁平化 prev/next 顺序
  const flat = all
    .map((e) => {
      const rest = e.id.slice(`${lang}/`.length)
      const seg = rest.split('/')
      const isIndex = seg.length > 1 && seg[seg.length - 1] === 'index'
      const title = e.data.title || rest.replace(/[-_]/g, ' ')
      const routeRest = isIndex ? seg.slice(0, -1).join('/') : rest
      return { id: e.id, href: `/${lang}/docs/${routeRest}/`, title }
    })
    .sort((a, b) => a.id.localeCompare(b.id, isEn ? 'en' : 'zh'))

  return { groups, flat }
}
