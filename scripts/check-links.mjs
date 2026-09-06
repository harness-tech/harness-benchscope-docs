#!/usr/bin/env node
/**
 * 内容级链接校验（Astro 版）：检查 src/content/docs 下所有 markdown 中的
 *   - 绝对路由内链（/zh/docs/...、/en/docs/...）
 *   - 图片引用（/images/...）
 * 是否指向存在的目标 / 资源。
 *
 * 用法: node scripts/check-links.mjs   （或 npm run test:links）
 * 退出码: 0 = 全部通过；1 = 存在失效链接。
 */
import { readFileSync, existsSync, statSync, readdirSync } from 'node:fs'
import { join, extname, resolve } from 'node:path'

const ROOT = new URL('../', import.meta.url).pathname
const DOCS = join(ROOT, 'src/content/docs')
const PUBLIC = join(ROOT, 'public')

function collectMd(dir, out = []) {
  for (const name of readdirSync(dir)) {
    const p = join(dir, name)
    if (statSync(p).isDirectory()) collectMd(p, out)
    else if (extname(p) === '.md') out.push(p)
  }
  return out
}
function collectPublic(dir = PUBLIC, base = '', out = []) {
  for (const name of readdirSync(dir)) {
    const p = join(dir, name)
    if (statSync(p).isDirectory()) collectPublic(p, `${base}/${name}`, out)
    else out.push(`${base}/${name}`)
  }
  return out
}

const mdFiles = collectMd(DOCS)
const publicAssets = collectPublic()
const mdSet = new Set(mdFiles.map((f) => f.replace(resolve(DOCS) + '/', '').replace(/\.md$/, '')))

const linkRe = /\]\(([^)]+)\)/g
const errors = []

for (const file of mdFiles) {
  const content = readFileSync(file, 'utf8')
  for (const m of content.matchAll(linkRe)) {
    const raw = m[1].trim()
    const url = raw.split(' ')[0].split('#')[0]
    if (!url || /^https?:|^mailto:|^data:|^#/.test(url)) continue
    if (url.startsWith('/images/')) {
      const asset = '/' + url.replace(/^\//, '')
      if (!publicAssets.some((a) => a === asset.replace(/^\/images/, '/images'))) {
        errors.push(`${file}: 图片不存在 ${url}`)
      }
    } else if (url.startsWith('/zh/docs/') || url.startsWith('/en/docs/')) {
      const rel = url.replace(/^\/(zh|en)\/docs\//, '').replace(/\/$/, '')
      const lang = url.startsWith('/en/') ? 'en' : 'zh'
      // 目录 index 路由既可写 /docs/<sec>/ 也可写 /docs/<sec>/index
      if (!mdSet.has(`${lang}/${rel}`) && !mdSet.has(`${lang}/${rel}/index`)) {
        errors.push(`${file}: 路由不存在 ${url}`)
      }
    } else if (url.endsWith('.md')) {
      // 仍有残留的 md 相对链接 → 视为迁移未完成
      errors.push(`${file}: 残留 .md 链接未转换 ${url}`)
    }
  }
}

const shown = [...new Set(errors)]
if (shown.length) {
  console.error(`❌ 发现 ${shown.length} 处失效/遗留引用：`)
  for (const e of shown) console.error('  - ' + e)
  process.exit(1)
}
console.log(`✅ 链接校验通过（${mdFiles.length} 个文档，${publicAssets.length} 个资源）`)
