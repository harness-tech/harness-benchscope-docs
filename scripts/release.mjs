#!/usr/bin/env node
/**
 * BenchScope Docs —— 版本 / 发布脚本
 *
 * 版本定位：1.0.0.dev，约定 x.y.z
 *   - z 变动（patch，如 1.0.0 -> 1.0.1）：
 *       只 git tag + git push（含 tag），不发布 release。
 *   - x.y 变动（minor/major，如 1.0 -> 1.1 / 2.0）：
 *       git tag + git push + 推送 release + 总结 release notes；
 *       「发布」流程暂未定义（脚本在此给出占位与提示，不自动执行外部发布）。
 *
 * 用法：
 *   node scripts/release.mjs <patch|minor|major> [--no-tag] [--push]
 *
 * 约定（与 AGENTS.md「版本与发布」一致）：
 *   - 绝不自动修改 package.json 版本除非显式传入（默认按算出的新版本写入并提示）。
 *   - 不自动执行 git push / 打 tag —— 本脚本默认只打印将要执行的命令，
 *     由维护者确认后手动执行（或加 --push 自动执行）。
 */
import { execSync } from 'node:child_process'
import { readFileSync, writeFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'

const __dirname = dirname(fileURLToPath(import.meta.url))
const ROOT = join(__dirname, '..')
const PKG_PATH = join(ROOT, 'package.json')

const args = process.argv.slice(2)
const bump = args.find((a) => ['patch', 'minor', 'major'].includes(a))
const doPush = args.includes('--push')
const noWrite = args.includes('--no-tag') // 仅展示，不写版本

if (!bump) {
  console.error('用法: node scripts/release.mjs <patch|minor|major> [--push]')
  console.error('  示例: node scripts/release.mjs patch   # z 变动，只打 tag + 推代码')
  console.error('        node scripts/release.mjs minor   # x.y 变动，tag + release notes + 发布(待定义)')
  process.exit(1)
}

// —— 读取当前版本 ——
const pkg = JSON.parse(readFileSync(PKG_PATH, 'utf8'))
const cur = String(pkg.version)
// dev/rc 后缀处理：1.0.0.dev 视为 1.0.0 → 计算下一版本
const base = cur.replace(/\.(dev|rc|beta|alpha).*$/, '')
const [maj, min, pat] = base.split('.').map((n) => Number(n))

let next
if (bump === 'major') next = `${maj + 1}.0.0`
else if (bump === 'minor') next = `${maj}.${min + 1}.0`
else next = `${maj}.${min}.${pat + 1}`

const tag = `v${next}`
const isPatch = bump === 'patch'

function sh(cmd) {
  try {
    return execSync(cmd, { cwd: ROOT, encoding: 'utf8' }).trim()
  } catch {
    return ''
  }
}

// —— 确认工作区 / 当前提交 ——
const commit = sh('git rev-parse --short HEAD')
const branch = sh('git rev-parse --abbrev-ref HEAD') || '(detached)'
const remote = sh('git remote get-url origin') || '(no remote)'

console.log('─'.repeat(60))
console.log(`版本定位    : 1.0.0.dev   (约定 x.y.z)`)
console.log(`当前版本    : ${pkg.version}   (基准 ${base})`)
console.log(`本次变动    : ${bump}  →  新版本 ${next}  (tag: ${tag})`)
console.log(`类型        : ${isPatch ? 'PATCH(z)' : bump.toUpperCase() + '(x.y)'}`)
console.log(`分支 / commit: ${branch} @ ${commit}`)
console.log(`remote      : ${remote}`)
console.log('─'.repeat(60))

// —— 更新 package.json ——
if (!noWrite) {
  pkg.version = next
  writeFileSync(PKG_PATH, JSON.stringify(pkg, null, 2) + '\n', 'utf8')
  console.log(`✓ package.json version -> ${next}`)
}

// —— 命令预览 ——
const cmds = [
  `git add package.json`,
  `git commit -m "chore(release): v${next}"`,
  `git tag ${tag}`,
  `git push origin ${branch}`,
  ...(doPush ? [`git push origin ${tag}`] : []),
]

console.log('\n待执行命令（本次为预览，未实际推送）:')
cmds.forEach((c) => console.log(`  $ ${c}`))

// —— release notes ——
console.log('\n-release notes 草稿----------------------------------')
if (isPatch) {
  console.log(`## [${tag}] — ${new Date().toISOString().slice(0, 10)}`)
  console.log(`\n### Patch（z 变动）\n`)
  console.log('仅打 tag 并推送代码；不发布 release。')
  console.log('变更摘要：（维护者填写）')
} else {
  console.log(`## [${tag}] — ${new Date().toISOString().slice(0, 10)}`)
  console.log(`\n### ${bump.toUpperCase()}（x.y 变动）\n`)
  console.log('- 打 tag + 推送 release + 总结 release notes')
  console.log('- 发布（publish）流程暂未定义 —— 维护者确认后按未来发布的渠道执行')
  console.log('\n变更要点：（维护者填写）')
}
console.log('─'.repeat(60))

console.log('\n⚠️  本脚本不自动执行 git 命令（预览模式）。')
if (isPatch) {
  console.log(`   Patch 流程：打 tag ${tag} + 推送代码即可（${doPush ? '已加 --push' : '手动推送'}'）。`)
} else {
  console.log(`   Minor/Major 流程：打 tag ${tag} + 推送 release + 总结 release notes + 发布(待定义)。`)
}
console.log('\n如需自动执行 push，请显式加 --push 后在确认产物无误时手动运行。')
