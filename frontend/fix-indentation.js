#!/usr/bin/env node

const fs = require('fs')
const path = require('path')

// Функция для рекурсивного поиска файлов
function findFiles(dir, extensions, files = []) {
  const items = fs.readdirSync(dir)
  
  for (const item of items) {
    const fullPath = path.join(dir, item)
    const stat = fs.statSync(fullPath)
    
    if (stat.isDirectory()) {
      // Пропускаем node_modules, .git и другие служебные папки
      if (!['node_modules', '.git', 'dist', 'build', '.nuxt', '.output'].includes(item)) {
        findFiles(fullPath, extensions, files)
      }
    } else if (stat.isFile()) {
      const ext = path.extname(item)
      if (extensions.includes(ext)) {
        files.push(fullPath)
      }
    }
  }
  
  return files
}

// Функция для исправления отступов
function fixIndentation(content) {
  const lines = content.split('\n')
  const fixedLines = []
  
  for (const line of lines) {
    // Заменяем табы на 2 пробела
    let fixedLine = line.replace(/\t/g, '  ')
    
    // Заменяем 4 пробела на 2 пробела в начале строки
    fixedLine = fixedLine.replace(/^( {4})+/g, (match) => {
      const spaceCount = match.length
      const newSpaceCount = (spaceCount / 4) * 2
      return ' '.repeat(newSpaceCount)
    })
    
    // Удаляем trailing whitespace
    fixedLine = fixedLine.replace(/\s+$/, '')
    
    fixedLines.push(fixedLine)
  }
  
  return fixedLines.join('\n')
}

// Основная функция
function main() {
  const srcDir = path.join(__dirname, 'src')
  const extensions = ['.vue', '.js', '.ts', '.css', '.scss', '.json']
  
  console.log('🔍 Поиск файлов для исправления отступов...')
  
  const files = findFiles(srcDir, extensions)
  
  console.log(`📁 Найдено ${files.length} файлов`)
  
  let fixedCount = 0
  
  for (const file of files) {
    try {
      const content = fs.readFileSync(file, 'utf8')
      const fixedContent = fixIndentation(content)
      
      // Проверяем, изменился ли контент
      if (content !== fixedContent) {
        fs.writeFileSync(file, fixedContent, 'utf8')
        console.log(`✅ Исправлен: ${path.relative(__dirname, file)}`)
        fixedCount++
      }
    } catch (error) {
      console.error(`❌ Ошибка при обработке ${file}:`, error.message)
    }
  }
  
  console.log(`\n🎉 Готово! Исправлено ${fixedCount} файлов из ${files.length}`)
  
  if (fixedCount === 0) {
    console.log('✨ Все файлы уже имеют правильные отступы!')
  }
}

// Запуск скрипта
if (require.main === module) {
  main()
}

module.exports = { fixIndentation, findFiles }