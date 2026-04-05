<template>
  <div class="tariff-management">
    <el-card>
      <template #header>
        <div class="card-header">关税管理</div>
      </template>
      <div class="placeholder">
        <el-empty description="关税管理页面"></el-empty>
      </div>
    </el-card>
  </div>
</template>

<script setup>
</script>

<style scoped>
.tariff-management {
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