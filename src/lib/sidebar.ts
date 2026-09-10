import { getCollection } from 'astro:content'

export interface LinkItem { id: string; href: string; title: string }
export interface SubGroup { label: string; icon?: string; children: LinkItem[] }
export interface Group { key: string; label: string; icon: string; children: LinkItem[]; subgroups?: SubGroup[] }

export const LABELS: Record<string, { zh: string; en: string }> = {
  quickstart: { zh: '快速开始', en: 'Quick Start' },
  install: { zh: '安装', en: 'Install' },
  manual: { zh: '使用手册', en: 'User Manual' },
  'manual/dashboard': { zh: 'Dashboard', en: 'Dashboard' },
  'manual/performance': { zh: 'Performance', en: 'Performance' },
  'manual/accuracy': { zh: 'Accuracy', en: 'Accuracy' },
  'manual/sessions': { zh: 'Sessions', en: 'Sessions' },
  'manual/datas': { zh: 'Datas', en: 'Datas' },
  'manual/settings': { zh: 'Settings', en: 'Settings' },
  performance: { zh: '性能测试', en: 'Performance' },
  accuracy: { zh: '精度测试', en: 'Accuracy' },
  data: { zh: '数据分析', en: 'Data' },
  tools: { zh: '高级工具', en: 'Tools' },
  cli: { zh: 'CLI', en: 'CLI' },
  api: { zh: 'API', en: 'API' },
  releases: { zh: '发布', en: 'Releases' },
  help: { zh: '帮助', en: 'Help' },
}

/** 每个一级分区对应的图标（见 Icons.astro 名称） */
export const SECTION_ICONS: Record<string, string> = {
  quickstart: 'rocket',
  install: 'download',
  manual: 'book',
  'manual/dashboard': 'home',
  'manual/performance': 'gauge',
  'manual/accuracy': 'target',
  'manual/sessions': 'chat',
  'manual/datas': 'database',
  'manual/settings': 'sliders',
  performance: 'gauge',
  accuracy: 'target',
  data: 'database',
  tools: 'gear',
  cli: 'terminal',
  api: 'code',
  releases: 'package',
  help: 'chat',
}

/** 使用手册子分组的顺序（按 Web 导航：Dashboard / Performance / Accuracy / Sessions / Datas / Settings） */
export const MANUAL_SUBGROUPS = ['dashboard', 'performance', 'accuracy', 'sessions', 'datas', 'settings']

/** 副导航 / 侧栏的一级分区顺序（install 并入 quickstart，manual 紧随 quickstart 之后） */
export const ORDER = ['quickstart', 'manual', 'performance', 'accuracy', 'data', 'tools', 'cli', 'api', 'releases', 'help']

/** 页面 section 目录 → 所属一级分组 key（install 归入 quickstart，manual/* 归入 manual） */
export const SECTION_GROUP: Record<string, string> = {
  quickstart: 'quickstart',
  install: 'quickstart',
  manual: 'manual',
  'manual/dashboard': 'manual',
  'manual/performance': 'manual',
  'manual/accuracy': 'manual',
  'manual/sessions': 'manual',
  'manual/datas': 'manual',
  'manual/settings': 'manual',
  performance: 'performance',
  accuracy: 'accuracy',
  data: 'data',
  tools: 'tools',
  cli: 'cli',
  api: 'api',
  releases: 'releases',
  help: 'help',
}

type CollectionEntry = { id: string; data: { title?: string } }

function landingItem(all: CollectionEntry[], lang: string, dir: string): LinkItem | null {
  const landing = all.find((e) => e.id === `${lang}/${dir}`)
  return landing ? { id: landing.id, href: `/${lang}/docs/${dir}/`, title: landing.data.title || dir } : null
}

function itemsFor(all: CollectionEntry[], lang: string, dir: string, isEn: boolean): LinkItem[] {
  return all
    .filter((e) => e.id.startsWith(`${lang}/${dir}/`))
    .map((e) => {
      const rest = e.id.slice(`${lang}/${dir}/`.length)
      const title = e.data.title || rest.replace(/[-_]/g, ' ')
      return { id: e.id, href: `/${lang}/docs/${dir}/${rest}/`, title }
    })
    .sort((a, b) => a.title.localeCompare(b.title, isEn ? 'en' : 'zh'))
}

function groupChildren(all: CollectionEntry[], lang: string, dir: string, isEn: boolean): LinkItem[] {
  const landing = landingItem(all, lang, dir)
  const items = itemsFor(all, lang, dir, isEn)
  return landing ? [landing, ...items] : items
}

/** 版本号正则：从 "v1.0.5" / "v1-0-5" 提取 → [1,0,5] */
function versionNum(t: string): number[] {
  const m = t.match(/(\d+)[._-]?(\d+)[._-]?(\d+)/)
  return m ? [Number(m[1]), Number(m[2]), Number(m[3])] : [0, 0, 0]
}
/** 发布页按版本倒序（最新在上） */
function sortReleases(items: LinkItem[]): LinkItem[] {
  return [...items].sort((a, b) => {
    const va = versionNum(a.title)
    const vb = versionNum(b.title)
    for (let i = 0; i < 3; i++) if (va[i] !== vb[i]) return vb[i] - va[i]
    return a.title.localeCompare(b.title)
  })
}

export async function buildSidebar(lang: 'zh' | 'en') {
  const all = await getCollection('docs', (e) => e.id.startsWith(`${lang}/`) && !e.id.toLowerCase().endsWith('/readme'))
  const isEn = lang === 'en'

  const groups: Group[] = ORDER.map((p) => {
    const children = groupChildren(all, lang, p, isEn)
    // 发布：落地页（概述）置顶，版本子页按倒序（最新在上）
    let kids = children
    if (p === 'releases') {
      const landingChildren = children[0] ? [children[0]] : []
      const rest = children.slice(1)
      kids = [...landingChildren, ...sortReleases(rest)]
    }
    // 快速开始：把 install 作为独立子分组并入（保留独立「安装」分组信息）
    const subgroups: SubGroup[] = []
    if (p === 'quickstart') {
      const instLanding = landingItem(all, lang, 'install')
      const instItems = itemsFor(all, lang, 'install', isEn)
      const instChildren = instLanding ? [instLanding, ...instItems] : instItems
      subgroups.push({ label: LABELS.install[lang], icon: SECTION_ICONS.install, children: instChildren })
    }
    // 使用手册：children 只保留手册落地页（总览），子分组按 Web 导航（dashboard/performance/accuracy/sessions/datas/settings）展开
    if (p === 'manual') {
      const manualLanding = landingItem(all, lang, 'manual')
      kids = manualLanding ? [manualLanding] : []
      for (const sub of MANUAL_SUBGROUPS) {
        const subLanding = landingItem(all, lang, `manual/${sub}`)
        const subItems = itemsFor(all, lang, `manual/${sub}`, isEn)
        const subChildren = subLanding ? [subLanding, ...subItems] : subItems
        if (subChildren.length) {
          subgroups.push({
            label: LABELS[`manual/${sub}`][lang],
            icon: SECTION_ICONS[`manual/${sub}`] ?? 'doc',
            children: subChildren,
          })
        }
      }
    }
    return {
      key: p,
      label: LABELS[p][lang],
      icon: SECTION_ICONS[p] ?? 'doc',
      children: kids,
      subgroups: subgroups.length ? subgroups : undefined,
    }
  })

  // 扁平化 prev/next 顺序（依 ORDER + install 并入 quickstart）
  const flat: LinkItem[] = []
  for (const g of groups) {
    for (const c of g.children) flat.push(c)
    if (g.subgroups) for (const s of g.subgroups) for (const c of s.children) flat.push(c)
  }

  return { groups, flat }
}
