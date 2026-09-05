---
navbar: false
footer: false
---

<script setup>
import { useRouter } from 'vue-router'
import { onMounted } from 'vue'

const router = useRouter()

// 根路径 / 自动重定向到默认语言官网（中文）
// 英文用户可在官网右上角切换为 English，或直接访问 /en/
onMounted(() => {
  router.replace('/zh/')
})
</script>

**正在跳转到中文官网… 若未自动跳转，请访问 [/zh/](/zh/) 或 [/en/](/en/)。**
