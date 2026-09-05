import { defineClientConfig } from 'vuepress/client'
import { useRouter } from 'vue-router'
import './styles/index.css'
import Landing from './theme/layouts/Landing.vue'

/** 在文档页面注入可隐藏的「本页」右侧目录导航 */
function buildRightToc() {
  const host = document.querySelector('.theme-default-content')
  document.querySelector('.bs-right-toc-wrap')?.remove()
  if (!host) return

  const wrap = document.createElement('aside')
  wrap.className = 'bs-right-toc-wrap'
  wrap.innerHTML =
    '<div class="bs-right-toc-head"><span class="bs-right-toc-title">本页</span>' +
    '<button class="bs-right-toc-hide" title="隐藏本页导航" aria-label="隐藏本页导航">×</button></div>' +
    '<nav class="bs-right-toc"></nav>'

  const nav = wrap.querySelector('.bs-right-toc') as HTMLElement
  const titles = host.querySelectorAll('h2, h3')
  if (titles.length === 0) return

  titles.forEach((h) => {
    const id = h.id
    if (!id) return
    const a = document.createElement('a')
    a.textContent = h.textContent || ''
    a.href = '#' + id
    const lv = h.tagName === 'H3' ? 2 : 1
    a.style.paddingLeft = lv === 2 ? '10px' : '0'
    a.className = 'bs-right-toc-link lv' + lv
    nav.appendChild(a)
  })

  const hide = wrap.querySelector('.bs-right-toc-hide') as HTMLElement
  hide.addEventListener('click', () => wrap.classList.add('hidden'))
  document.body.appendChild(wrap)
}

export default defineClientConfig({
  layouts: { Landing },
  setup() {
    const router = useRouter()
    router.afterEach((to) => {
      // 仅在浏览器端执行（SSR 无 document）
      if (typeof window === 'undefined') return
      setTimeout(() => {
        if (to.path.includes('/docs/')) buildRightToc()
        else document.querySelector('.bs-right-toc-wrap')?.remove()
      }, 50)
    })
  },
})
