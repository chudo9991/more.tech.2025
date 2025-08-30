<template>
  <div class="resume-detail">
    <div class="page-header">
      <h1>Детали резюме</h1>
      <el-button @click="$router.push('/resumes')" icon="ArrowLeft">
        Назад к списку
      </el-button>
    </div>
    
    <el-card>
      <template #header>
        <span>Информация о резюме</span>
      </template>
      
      <div class="detail-content">
        <p>Страница детального просмотра резюме будет реализована в следующем этапе.</p>
        <p>ID резюме: {{ $route.params.id }}</p>
      </div>
    </el-card>
  </div>
</template>

<script>
import { ArrowLeft } from '@element-plus/icons-vue'

export default {
  name: 'ResumeDetail',
  components: {
    ArrowLeft
  }
}
</script>

<style scoped>
.resume-detail {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h1 {
  margin: 0;
  color: #303133;
}

.detail-content {
  padding: 20px;
  text-align: center;
  color: #606266;
}
</style>
