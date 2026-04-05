<template>
  <div class="menu-manage" :style="{ fontSize: fontSize + 'px' }">
    <el-card class="toolbar">
      <div class="toolbar-content">
        <el-button type="primary" :icon="Plus" size="small" @click="handleAdd">新增菜单</el-button>
        <el-button :icon="Download" size="small" @click="handleExport">导出</el-button>
        <el-button :icon="Refresh" size="small" @click="loadMenus">刷新</el-button>
      </div>
    </el-card>

    <el-card class="table-card">
      <el-table
        :data="menuList"
        row-key="menuId"
        :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
        default-expand-all
        border
        :size="tableSize"
        style="width: 100%"
      >
        <el-table-column prop="menuName" label="菜单名称" :width="columnWidth.menuName" show-overflow-tooltip />
        <el-table-column prop="menuCode" label="菜单代码" :width="columnWidth.menuCode" show-overflow-tooltip />
        <el-table-column prop="routePath" label="路由路径" :width="columnWidth.routePath" show-overflow-tooltip />
        <el-table-column prop="icon" label="图标" :width="columnWidth.icon" />
        <el-table-column prop="sortOrder" label="排序" width="60" align="center" />
        <el-table-column prop="isVisible" label="显示" width="60" align="center">
          <template #default="{ row }">
            <el-tag :type="row.isVisible ? 'success' : 'info'" size="small">
              {{ row.isVisible ? '是' : '否' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="permission" label="权限标识" :width="columnWidth.permission" show-overflow-tooltip />
        <el-table-column label="操作" fixed="right" :width="isMobile ? '150' : '200'">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button link type="danger" size="small" @click="handleDelete(row)">删除</el-button>
            <el-button link type="success" size="small" @click="handleAddChild(row)">子菜单</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      :width="dialogWidth"
      @close="handleDialogClose"
      :fullscreen="isMobile"
    >
      <el-form ref="formRef" :model="formData" :rules="formRules" :label-width="formLabelWidth" size="small">
        <el-form-item label="菜单ID" prop="menuId" v-if="formType === 'add'">
          <el-input v-model="formData.menuId" placeholder="请输入菜单ID" />
        </el-form-item>
        <el-form-item label="菜单名称" prop="menuName">
          <el-input v-model="formData.menuName" placeholder="请输入菜单名称" />
        </el-form-item>
        <el-form-item label="菜单代码" prop="menuCode">
          <el-input v-model="formData.menuCode" placeholder="请输入菜单代码" />
        </el-form-item>
        <el-form-item label="父菜单" prop="parentId">
          <el-select v-model="formData.parentId" placeholder="请选择父菜单" clearable style="width: 100%">
            <el-option label="作为顶级菜单" value="0" />
            <el-option
              v-for="menu in flatMenuList"
              :key="menu.menuId"
              :label="menu.menuName"
              :value="menu.menuId"
              :disabled="menu.menuId === formData.menuId"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="路由路径" prop="routePath">
          <el-input v-model="formData.routePath" placeholder="请输入路由路径" />
        </el-form-item>
        <el-form-item label="图标" prop="icon">
          <el-input v-model="formData.icon" placeholder="请输入图标名称" />
        </el-form-item>
        <el-form-item label="排序" prop="sortOrder">
          <el-input-number v-model="formData.sortOrder" :min="0" :max="999" />
        </el-form-item>
        <el-form-item label="显示" prop="isVisible">
          <el-switch v-model="formData.isVisible" />
        </el-form-item>
        <el-form-item label="权限标识" prop="permission">
          <el-input v-model="formData.permission" placeholder="请输入权限标识" />
        </el-form-item>
        <el-form-item label="组件" prop="component">
          <el-input v-model="formData.component" placeholder="请输入组件名称" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false" size="small">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitLoading" size="small">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Download, Refresh } from '@element-plus/icons-vue'
import axios from 'axios'
import config from '../config'

const menuList = ref([])
const dialogVisible = ref(false)
const dialogTitle = ref('')
const formType = ref('add')
const submitLoading = ref(false)
const formRef = ref(null)
const windowWidth = ref(window.innerWidth)
const isMobile = computed(() => windowWidth.value < 768)

const fontSize = computed(() => {
  const scale = Math.min(windowWidth.value / 1920, 1)
  return Math.round(14 * scale * 10) / 10
})

const tableSize = computed(() => isMobile.value ? 'small' : 'default')

const columnWidth = computed(() => {
  if (windowWidth.value < 768) {
    return { menuName: 120, menuCode: 100, routePath: 100, icon: 60, permission: 100 }
  }
  if (windowWidth.value < 1200) {
    return { menuName: 150, menuCode: 110, routePath: 130, icon: 80, permission: 130 }
  }
  return { menuName: 180, menuCode: 120, routePath: 150, icon: 100, permission: 150 }
})

const dialogWidth = computed(() => {
  if (windowWidth.value < 768) return '90%'
  if (windowWidth.value < 1200) return '500px'
  return '600px'
})

const formLabelWidth = computed(() => isMobile.value ? '70px' : '100px')

const formData = ref({
  menuId: '',
  menuName: '',
  menuCode: '',
  parentId: '0',
  routePath: '',
  icon: '',
  sortOrder: 0,
  isVisible: true,
  permission: '',
  component: ''
})

const formRules = {
  menuId: [{ required: true, message: '请输入菜单ID', trigger: 'blur' }],
  menuName: [{ required: true, message: '请输入菜单名称', trigger: 'blur' }],
  menuCode: [{ required: true, message: '请输入菜单代码', trigger: 'blur' }]
}

const flatMenuList = computed(() => {
  const result = []
  const flatten = (menus, level = 0) => {
    menus.forEach(menu => {
      result.push({ ...menu, level })
      if (menu.children && menu.children.length) {
        flatten(menu.children, level + 1)
      }
    })
  }
  flatten(menuList.value)
  return result
})

const buildMenuTree = (list) => {
  const map = {}
  const roots = []

  list.forEach(item => {
    map[item.menuId] = { ...item, children: [] }
  })

  list.forEach(item => {
    if (item.parentId && item.parentId !== '0' && map[item.parentId]) {
      map[item.parentId].children.push(map[item.menuId])
    } else if (!item.parentId || item.parentId === '0') {
      roots.push(map[item.menuId])
    }
  })

  return roots
}

const loadMenus = async () => {
  try {
    const response = await axios.get(`${config.apiBaseUrl}/menu/list`)
    const rawMenuList = response.data || []
    menuList.value = buildMenuTree(rawMenuList)
  } catch (error) {
    ElMessage.error('加载菜单失败')
  }
}

const handleAdd = () => {
  formType.value = 'add'
  dialogTitle.value = '新增菜单'
  formData.value = {
    menuId: '',
    menuName: '',
    menuCode: '',
    parentId: '0',
    routePath: '',
    icon: '',
    sortOrder: 0,
    isVisible: true,
    permission: '',
    component: ''
  }
  dialogVisible.value = true
}

const handleAddChild = (row) => {
  formType.value = 'add'
  dialogTitle.value = `添加子菜单 - ${row.menuName}`
  formData.value = {
    menuId: '',
    menuName: '',
    menuCode: '',
    parentId: row.menuId,
    routePath: '',
    icon: '',
    sortOrder: 0,
    isVisible: true,
    permission: '',
    component: ''
  }
  dialogVisible.value = true
}

const handleEdit = (row) => {
  formType.value = 'edit'
  dialogTitle.value = `编辑菜单 - ${row.menuName}`
  formData.value = { ...row, parentId: row.parentId || '0' }
  dialogVisible.value = true
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要删除菜单"${row.menuName}"吗？`, '提示', {
      type: 'warning'
    })
    await axios.delete(`${config.apiBaseUrl}/menu/${row.menuId}`)
    ElMessage.success('删除成功')
    loadMenus()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    submitLoading.value = true
    try {
      if (formType.value === 'add') {
        await axios.post(`${config.apiBaseUrl}/menu`, formData.value)
        ElMessage.success('创建成功')
      } else {
        await axios.put(`${config.apiBaseUrl}/menu/${formData.value.menuId}`, formData.value)
        ElMessage.success('更新成功')
      }
      dialogVisible.value = false
      loadMenus()
    } catch (error) {
      ElMessage.error(formType.value === 'add' ? '创建失败' : '更新失败')
    } finally {
      submitLoading.value = false
    }
  })
}

const handleDialogClose = () => {
  formRef.value?.resetFields()
}

const handleExport = () => {
  const exportData = JSON.stringify(menuList.value, null, 2)
  const blob = new Blob([exportData], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = `菜单配置_${new Date().toISOString().slice(0, 10)}.json`
  link.click()
  URL.revokeObjectURL(url)
  ElMessage.success('导出成功')
}

const handleResize = () => {
  windowWidth.value = window.innerWidth
}

onMounted(() => {
  loadMenus()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.menu-manage {
  padding: 0;
}

.toolbar {
  margin-bottom: 15px;
  border-radius: 8px;
}

.toolbar-content {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.table-card {
  border-radius: 8px;
}
</style>