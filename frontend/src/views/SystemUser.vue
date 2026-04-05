<template>
  <div class="system-user">
    <el-card>
      <template #header>
        <div class="card-header">用户管理</div>
      </template>
      <div class="placeholder">
        <el-empty description="用户管理页面"></el-empty>
      </div>
    </el-card>
  </div>
</template>

<script setup>
</script>

<style scoped>
.system-user {
  height: 100%;
}

.card-header {
  font-weight: 600;
  font-size: 16px;
}

.placeholder {
  padding: 40px 0;
  text-align: center;
}
</style>