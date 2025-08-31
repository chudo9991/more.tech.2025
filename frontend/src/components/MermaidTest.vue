<template>
  <div class="mermaid-test">
    <h3>Тест Mermaid</h3>
    <div class="mermaid" ref="mermaidRef"></div>
    <button @click="testMermaid">Тестировать Mermaid</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import mermaid from 'mermaid'

const mermaidRef = ref(null)

const testMermaid = async () => {
  try {
    console.log('Тестирование Mermaid...')
    
    // Инициализация
    mermaid.initialize({
      startOnLoad: false,
      theme: 'default'
    })
    
    const testCode = `
graph TD
    A[Начало] --> B[Вопрос 1]
    B --> C[Вопрос 2]
    C --> D[Конец]
    `
    
    console.log('Mermaid код:', testCode)
    
    // Рендеринг
    const { svg } = await mermaid.render('test-diagram', testCode)
    mermaidRef.value.innerHTML = svg
    
    console.log('Mermaid тест успешен!')
    
  } catch (error) {
    console.error('Ошибка теста Mermaid:', error)
  }
}

onMounted(() => {
  console.log('MermaidTest компонент загружен')
  console.log('Mermaid доступен:', typeof mermaid !== 'undefined')
  if (typeof mermaid !== 'undefined') {
    console.log('Версия Mermaid:', mermaid.version)
  }
})
</script>

<style scoped>
.mermaid-test {
  padding: 20px;
  border: 1px solid #ccc;
  margin: 20px;
}

.mermaid {
  text-align: center;
  margin: 20px 0;
  min-height: 200px;
  border: 1px solid #eee;
  padding: 20px;
}

button {
  padding: 10px 20px;
  background: #409EFF;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background: #337ecc;
}
</style>
