#!/usr/bin/env node
/**
 * 生成搜索索引 search-index.json（基于 src/content/docs 的 md 首行标题）。
 * 输出到 public/search-index.json，供客户端 minisearch 使用。
 * 用法: node scripts/build-search-index.mjs
 */
import { readFileSync, writeFileSync, readdirSync, statSync } from 'node:fs'
import { join, extname } from 'node:path'

const ROOT = new URL('../', import.meta.url).pathname
const DOCS = join(ROOT, 'src/content/docs')

function walk(d, out = []) {
  for (const n of readdirSync(d)) {
    const p = join(d, n)
    if (statSync(p).isDirectory()) walk(p, out)
    else if (extname(p) === '.md') out.push(p)
  }
  return out
}

const entries = []
for (const f of walk(DOCS)) {
  const rel = f.replace(join(DOCS, '/'), '')
  const lang = rel.startsWith('en/') ? 'en' : 'zh'
  const path = rel.replace(/\.md$/, '').split('/').slice(1) // 去语言前缀
  if (!path.length || path.join('/').toLowerCase().endsWith('readme')) continue
  const content = readFileSync(f, 'utf8')
  // index.md 折叠为目录根路由（/zh/docs/quickstart/）
  let route = path.join('/')
  if (route.endsWith('/index')) route = route.slice(0, -'/index'.length)
  const titleM = content.match(/^#\s+(.+)$/m)
  const title = (titleM ? titleM[1] : path.join(' ')).trim()
  const body = content.replace(/^#.*$/m, '').replace(/[#>*`\[\]|]/g, ' ').slice(0, 400)
  entries.push({ id: `/${lang}/docs/${route}/`, lang, title, body })
}

const json = JSON.stringify({ updated: new Date().toISOString(), entries })
writeFileSync(join(ROOT, 'public/search-index.json'), json, 'utf8')
console.log(`✓ 搜索索引：${entries.length} 条 -> public/search-index.json`)
