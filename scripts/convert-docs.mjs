#!/usr/bin/env node
/**
 * 迁移转换脚本：把旧式风格的文档 md 转为 Astro 可用形式。
 *  1) `::: tip` 容器 -> <div class="tip">...</div>
 *  2) 相对 `.md` 链接（./x.md、../x.md）-> /{lang}/docs/{path}
 * 用法: node scripts/convert-docs.mjs [dir]
 */
import { readFileSync, writeFileSync, readdirSync, statSync } from 'node:fs'
import { join, extname } from 'node:path'

const ROOT = new URL('../', import.meta.url).pathname
const dir = process.argv[2] ? join(ROOT, process.argv[2]) : join(ROOT, 'src/content/docs')

function walk(d, out = []) {
  for (const n of readdirSync(d)) {
    const p = join(d, n)
    if (statSync(p).isDirectory()) walk(p, out)
    else if (extname(p) === '.md') out.push(p)
  }
  return out
}

function convertContainers(md) {
  // 逐行扫描 ::: 起止块
  const lines = md.split('\n')
  const out = []
  let i = 0
  while (i < lines.length) {
    const m = lines[i].match(/^:+\s+(tip|warning|info|danger|note)\s*(.*)$/)
    if (m) {
      const type = m[1]
      const title = m[2].trim() || type
      const block = []
      i++
      while (i < lines.length && !/^:+\s*$/.test(lines[i])) {
        block.push(lines[i]); i++
      }
      i++ // skip :::
      out.push(`<div class="${type}">\n\n**${title}**：\n\n${block.join('\n')}\n\n</div>`)
    } else {
      out.push(lines[i]); i++
    }
  }
  return out.join('\n')
}

function convertLinks(md, lang, rel) {
  // 相对链接（./ ../ 或纯相对文件名，且不以 / 开头）-> 绝对路由
  md = md.replace(/\]\(((?:\.{0,2}\/)?[^)#\s:]+\/?)\.md(#[^)]*)?\)/g, (_whole, target, hash) => {
    const segs = target.split('/')
    const parts = [...rel.slice(0, -1)]
    for (const seg of segs) {
      if (seg === '..') parts.pop()
      else if (seg === '.' || seg === '' || seg.includes('http')) continue
      else parts.push(seg)
    }
    return `](${lang === 'zh' ? '/zh' : '/en'}/docs/${parts.join('/')}${hash || ''})`
  })
  // 绝对路由去 .md 后缀（如 /zh/docs/core/performance.md）
  md = md.replace(/\]\(\/(zh|en)\/docs\/([^)#\s]+)\.md(#[^)]*)?\)/g, (whole, l, path, hash) => {
    return `](${l ? '/' + l : ''}/docs/${path}${hash || ''})`
  })
  return md
}

const files = walk(dir)
let count = 0
for (const f of files) {
  let md = readFileSync(f, 'utf8')
  const orig = md
  // 识别语言与相对路径
  const relPath = f.replace(join(ROOT, 'src/content/docs/'), '') // zh/get-started/quickstart.md
  const lang = relPath.startsWith('zh/') ? 'zh' : 'en'
  const rel = relPath.replace(/\.md$/, '').split('/').slice(1) // 去 zh/en 前缀

  md = convertContainers(md)
  md = convertLinks(md, lang, rel)
  if (md !== orig) {
    writeFileSync(f, md)
    count++
  }
}
console.log(`✓ 转换完成：${files.length} 个文件，${count} 个已修改`)
