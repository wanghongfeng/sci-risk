<template>
  <div class="classification-definition">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>风险分类分级定义</span>
        </div>
      </template>
      
      <el-tabs v-model="activeTab" class="classification-tabs">
        <el-tab-pane label="风险类型定义" name="riskTypes">
          <div class="tab-content">
            <div class="action-bar">
              <el-button type="primary" size="small" @click="openAddRiskTypeDialog"><el-icon><Plus /></el-icon>新增风险类型</el-button>
            </div>
            
            <el-table :data="riskTypes" style="width: 100%" border stripe>
              <el-table-column prop="typeId" label="类型ID" width="120" />
              <el-table-column prop="typeName" label="类型名称" width="180" />
              <el-table-column prop="description" label="类型描述" min-width="200" show-overflow-tooltip />
              <el-table-column prop="color" label="标识颜色" width="120">
                <template #default="scope">
                  <div class="color-block" :style="{ backgroundColor: scope.row.color }"></div>
                </template>
              </el-table-column>
              <el-table-column prop="createTime" label="创建时间" width="180" />
              <el-table-column label="操作" width="180" fixed="right">
                <template #default="scope">
                  <el-button type="primary" size="small" @click="openEditRiskTypeDialog(scope.row)"><el-icon><Edit /></el-icon>编辑</el-button>
                  <el-button type="danger" size="small" @click="handleDeleteRiskType(scope.row)"><el-icon><Delete /></el-icon>删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>
        
        <el-tab-pane label="风险等级定义" name="riskLevels">
          <div class="tab-content">
            <div class="action-bar">
              <el-button type="primary" size="small" @click="openAddRiskLevelDialog"><el-icon><Plus /></el-icon>新增风险等级</el-button>
            </div>
            
            <el-table :data="riskLevels" style="width: 100%" border stripe>
              <el-table-column prop="levelId" label="等级ID" width="120" />
              <el-table-column prop="levelName" label="等级名称" width="120" />
              <el-table-column prop="levelValue" label="等级值" width="100" align="center" />
              <el-table-column prop="description" label="等级描述" min-width="200" show-overflow-tooltip />
              <el-table-column prop="color" label="标识颜色" width="120">
                <template #default="scope">
                  <div class="color-block" :style="{ backgroundColor: scope.row.color }"></div>
                </template>
              </el-table-column>
              <el-table-column prop="createTime" label="创建时间" width="180" />
              <el-table-column label="操作" width="180" fixed="right">
                <template #default="scope">
                  <el-button type="primary" size="small" @click="openEditRiskLevelDialog(scope.row)"><el-icon><Edit /></el-icon>编辑</el-button>
                  <el-button type="danger" size="small" @click="handleDeleteRiskLevel(scope.row)"><el-icon><Delete /></el-icon>删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>
    
    <!-- 新增/编辑风险类型对话框 -->
    <el-dialog v-model="riskTypeDialogVisible" :title="riskTypeDialogTitle" width="600px">
      <el-form :model="riskTypeForm" label-width="120px" :rules="riskTypeRules" ref="riskTypeFormRef">
        <el-form-item label="类型名称" prop="typeName">
          <el-input v-model="riskTypeForm.typeName" placeholder="请输入风险类型名称" />
        </el-form-item>
        <el-form-item label="类型描述" prop="description">
          <el-input v-model="riskTypeForm.description" type="textarea" placeholder="请输入风险类型描述" :rows="3" />
        </el-form-item>
        <el-form-item label="标识颜色" prop="color">
          <el-color-picker v-model="riskTypeForm.color" show-alpha />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="riskTypeDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSaveRiskType">确定</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 新增/编辑风险等级对话框 -->
    <el-dialog v-model="riskLevelDialogVisible" :title="riskLevelDialogTitle" width="600px">
      <el-form :model="riskLevelForm" label-width="120px" :rules="riskLevelRules" ref="riskLevelFormRef">
        <el-form-item label="等级名称" prop="levelName">
          <el-input v-model="riskLevelForm.levelName" placeholder="请输入风险等级名称" />
        </el-form-item>
        <el-form-item label="等级值" prop="levelValue">
          <el-input v-model.number="riskLevelForm.levelValue" type="number" placeholder="请输入风险等级值" />
        </el-form-item>
        <el-form-item label="等级描述" prop="description">
          <el-input v-model="riskLevelForm.description" type="textarea" placeholder="请输入风险等级描述" :rows="3" />
        </el-form-item>
        <el-form-item label="标识颜色" prop="color">
          <el-color-picker v-model="riskLevelForm.color" show-alpha />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="riskLevelDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSaveRiskLevel">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, Edit, Delete } from '@element-plus/icons-vue'

// 标签页
const activeTab = ref('riskTypes')

// 风险类型数据
const riskTypes = ref([
  { typeId: 'RT001', typeName: '供应链风险', description: '与供应商、物流、生产相关的风险', color: '#409eff', createTime: '2026-01-01 10:00:00' },
  { typeId: 'RT002', typeName: '市场风险', description: '与市场需求、竞争、价格相关的风险', color: '#67c23a', createTime: '2026-01-01 10:00:00' },
  { typeId: 'RT003', typeName: '政策风险', description: '与法律法规、政策变化相关的风险', color: '#e6a23c', createTime: '2026-01-01 10:00:00' },
  { typeId: 'RT004', typeName: '财务风险', description: '与资金、成本、汇率相关的风险', color: '#f56c6c', createTime: '2026-01-01 10:00:00' },
  { typeId: 'RT005', typeName: '其他风险', description: '其他类型的风险', color: '#909399', createTime: '2026-01-01 10:00:00' }
])

// 风险等级数据
const riskLevels = ref([
  { levelId: 'RL001', levelName: '低风险', levelValue: 1, description: '影响较小，可忽略', color: '#67c23a', createTime: '2026-01-01 10:00:00' },
  { levelId: 'RL002', levelName: '中风险', levelValue: 2, description: '有一定影响，需要关注', color: '#e6a23c', createTime: '2026-01-01 10:00:00' },
  { levelId: 'RL003', levelName: '高风险', levelValue: 3, description: '影响较大，需要立即处理', color: '#f56c6c', createTime: '2026-01-01 10:00:00' }
])

// 风险类型对话框
const riskTypeDialogVisible = ref(false)
const riskTypeDialogTitle = ref('新增风险类型')
const riskTypeFormRef = ref(null)
const riskTypeForm = reactive({
  typeId: '',
  typeName: '',
  description: '',
  color: '#409eff'
})
const riskTypeRules = {
  typeName: [{ required: true, message: '请输入类型名称', trigger: 'blur' }],
  description: [{ required: true, message: '请输入类型描述', trigger: 'blur' }],
  color: [{ required: true, message: '请选择标识颜色', trigger: 'blur' }]
}

// 风险等级对话框
const riskLevelDialogVisible = ref(false)
const riskLevelDialogTitle = ref('新增风险等级')
const riskLevelFormRef = ref(null)
const riskLevelForm = reactive({
  levelId: '',
  levelName: '',
  levelValue: 1,
  description: '',
  color: '#67c23a'
})
const riskLevelRules = {
  levelName: [{ required: true, message: '请输入等级名称', trigger: 'blur' }],
  levelValue: [{ required: true, message: '请输入等级值', trigger: 'blur' }, { type: 'number', message: '请输入数字', trigger: 'blur' }],
  description: [{ required: true, message: '请输入等级描述', trigger: 'blur' }],
  color: [{ required: true, message: '请选择标识颜色', trigger: 'blur' }]
}

// 打开新增风险类型对话框
const openAddRiskTypeDialog = () => {
  riskTypeDialogTitle.value = '新增风险类型'
  Object.assign(riskTypeForm, {
    typeId: '',
    typeName: '',
    description: '',
    color: '#409eff'
  })
  riskTypeDialogVisible.value = true
}

// 打开编辑风险类型对话框
const openEditRiskTypeDialog = (row) => {
  riskTypeDialogTitle.value = '编辑风险类型'
  Object.assign(riskTypeForm, row)
  riskTypeDialogVisible.value = true
}

// 保存风险类型
const handleSaveRiskType = async () => {
  if (!riskTypeFormRef.value) return
  
  try {
    await riskTypeFormRef.value.validate()
    
    if (!riskTypeForm.typeId) {
      // 新增
      const newId = 'RT' + String(riskTypes.value.length + 1).padStart(3, '0')
      const newType = {
        ...riskTypeForm,
        typeId: newId,
        createTime: new Date().toLocaleString('zh-CN')
      }
      riskTypes.value.push(newType)
      ElMessage.success('新增风险类型成功')
    } else {
      // 编辑
      const index = riskTypes.value.findIndex(item => item.typeId === riskTypeForm.typeId)
      if (index !== -1) {
        riskTypes.value[index] = { ...riskTypeForm }
        ElMessage.success('编辑风险类型成功')
      }
    }
    
    riskTypeDialogVisible.value = false
  } catch (error) {
    console.error('表单验证失败:', error)
  }
}

// 删除风险类型
const handleDeleteRiskType = (row) => {
  ElMessage.confirm('确定要删除这个风险类型吗？', '删除确认', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    const index = riskTypes.value.findIndex(item => item.typeId === row.typeId)
    if (index !== -1) {
      riskTypes.value.splice(index, 1)
      ElMessage.success('删除风险类型成功')
    }
  }).catch(() => {
    // 取消删除
  })
}

// 打开新增风险等级对话框
const openAddRiskLevelDialog = () => {
  riskLevelDialogTitle.value = '新增风险等级'
  Object.assign(riskLevelForm, {
    levelId: '',
    levelName: '',
    levelValue: 1,
    description: '',
    color: '#67c23a'
  })
  riskLevelDialogVisible.value = true
}

// 打开编辑风险等级对话框
const openEditRiskLevelDialog = (row) => {
  riskLevelDialogTitle.value = '编辑风险等级'
  Object.assign(riskLevelForm, row)
  riskLevelDialogVisible.value = true
}

// 保存风险等级
const handleSaveRiskLevel = async () => {
  if (!riskLevelFormRef.value) return
  
  try {
    await riskLevelFormRef.value.validate()
    
    if (!riskLevelForm.levelId) {
      // 新增
      const newId = 'RL' + String(riskLevels.value.length + 1).padStart(3, '0')
      const newLevel = {
        ...riskLevelForm,
        levelId: newId,
        createTime: new Date().toLocaleString('zh-CN')
      }
      riskLevels.value.push(newLevel)
      ElMessage.success('新增风险等级成功')
    } else {
      // 编辑
      const index = riskLevels.value.findIndex(item => item.levelId === riskLevelForm.levelId)
      if (index !== -1) {
        riskLevels.value[index] = { ...riskLevelForm }
        ElMessage.success('编辑风险等级成功')
      }
    }
    
    riskLevelDialogVisible.value = false
  } catch (error) {
    console.error('表单验证失败:', error)
  }
}

// 删除风险等级
const handleDeleteRiskLevel = (row) => {
  ElMessage.confirm('确定要删除这个风险等级吗？', '删除确认', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    const index = riskLevels.value.findIndex(item => item.levelId === row.levelId)
    if (index !== -1) {
      riskLevels.value.splice(index, 1)
      ElMessage.success('删除风险等级成功')
    }
  }).catch(() => {
    // 取消删除
  })
}

onMounted(() => {
  // 可以在这里加载初始数据
  console.log('ClassificationDefinition mounted')
})
</script>

<style scoped>
.classification-definition {
  padding: 0 8px;
}

.page-card {
  margin-bottom: 16px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.classification-tabs {
  margin-top: 16px;
}

.tab-content {
  padding: 16px 0;
}

.action-bar {
  margin-bottom: 16px;
}

.color-block {
  width: 40px;
  height: 20px;
  border-radius: 4px;
  border: 1px solid #dcdfe6;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}
</style>