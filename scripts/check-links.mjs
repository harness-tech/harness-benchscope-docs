#!/usr/bin/env node
/**
 * 内容级链接校验：检查 docs/zh 与 docs/en 下所有 markdown 文件中的
 *   - 相对内链（../../xxx.md, ./xx.md）
 *   - 相对图片引用（![xxx](/images/...) 或 相对路径）
 * 是否指向存在的文件 / 资源。
 *
 * 用法: node scripts/check-links.mjs   （或 npm run test:links）
 * 退出码: 0 = 全部通过；1 = 存在失效链接。
 */
import { readFileSync, existsSync } from 'node:fs'
import { readdirSync, statSync } from 'node:fs'
import { dirname, resolve, join, extname } from 'node:path'

const ROOT = new URL('../', import.meta.url).pathname
const DOCS = join(ROOT, 'docs')

/** 递归收集所有 .md 文件 */
function collectMd(dir) {
  const out = []
  for (const name of readdirSync(dir)) {
    const p = join(dir, name)
    if (statSync(p).isDirectory()) out.push(...collectMd(p))
    else if (extname(p) === '.md') out.push(p)
  }
  return out
}

/** 递归收集 public 图片资源 */
function collectPublic() {
  const out = []
  const pub = join(DOCS, '.vuepress', 'public')
  if (!existsSync(pub)) return out
  const walk = (d) => {
    for (const name of readdirSync(d)) {
      const p = join(d, name)
      if (statSync(p).isDirectory()) walk(p)
      else out.push('/' + p.slice(pub.length + 1))
    }
  }
  walk(pub)
  return out
}

const mdFiles = [...collectMd(join(DOCS, 'zh')), ...collectMd(join(DOCS, 'en'))]
const publicAssets = collectPublic()

const errors = []
// 内链/相对图片：foo.md、../foo.md、./x.md、相对图片相对路径
const relRefRe = /\]\(([^)#]+?)(?:#[^)]*)?\)/g
// 绝对图片：/images/...
const absImgRe = /\]\((\/[^)#]+?)(?:#[^)]*)?\)/g

for (const file of mdFiles) {
  const content = readFileSync(file, 'utf8')
  const srcDir = dirname(file)

  // 1) 相对引用（md 链接 与 相对图片）
  for (const m of content.matchAll(relRefRe)) {
    let target = m[1].trim()
    if (!target || /^https?:|^mailto:|^#/.test(target)) continue
    if (target.startsWith('/')) {
      // 绝对路径 → 映射到 public 资源
      if (!publicAssets.includes(target)) {
        errors.push(`${file}: 绝对资源不存在 ${target}`)
      }
      continue
    }
    // 去掉 query / hash，处理相对路径（base 为 docs/zh 或 docs/en 各自文档根）
    const rel = target.split('?')[0].split('#')[0]
    // 相对链接基准：markdown 相对路径相对于当前文件目录；但根 /docs/get-started 语义 → 这里按文件相对解析为主
    let resolved = resolve(srcDir, rel)
    // 若无法按文件相对解析成功，尝试相对 zh/en 文档根解析
    if (!existsSync(resolved)) {
      const altBase = join(DOCS, file.includes('/zh/') ? 'zh' : 'en')
      resolved = resolve(altBase, rel)
    }
    if (!existsSync(resolved)) {
      errors.push(`${file}: 相对目标不存在 -> ${target} (解析: ${resolved})`)
    }
  }

  // 2) 绝对图片
  for (const m of content.matchAll(absImgRe)) {
    const target = m[1]
    if (/^https?:/.test(target)) continue
    if (!publicAssets.includes(target)) {
      errors.push(`${file}: 图片不存在 -> ${target}`)
    }
  }
}

const base = DOCS
const shown = [...new Set(errors)]
if (shown.length) {
  console.error(`❌ 发现 ${shown.length} 处失效引用：`)
  for (const e of shown) console.error('  - ' + e)
  process.exit(1)
}
console.log(`✅ 链接校验通过（${mdFiles.length} 个文档，${publicAssets.length} 个资源）— ${base}`)
