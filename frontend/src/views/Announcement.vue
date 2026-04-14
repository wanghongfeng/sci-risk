<template>
  <div class="announcement">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>公告与帮助中心</span>
          <div class="header-actions">
            <el-button type="primary" size="small" @click="handleCreateAnnouncement"><el-icon><Plus /></el-icon>发布公告</el-button>
            <el-button type="success" size="small" @click="handleRefresh"><el-icon><Refresh /></el-icon>刷新</el-button>
          </div>
        </div>
      </template>
      <div v-loading="loading">
        <el-tabs v-model="activeTab" @tab-change="handleTabChange">
          <!-- 公告管理 -->
          <el-tab-pane label="公告管理" name="announcement">
            <!-- 搜索和筛选 -->
            <div class="search-container">
              <el-form :inline="true" :model="searchForm" class="search-form">
                <el-form-item label="公告标题"><el-input v-model="searchForm.title" placeholder="请输入" clearable style="width: 250px;" /></el-form-item>
                <el-form-item label="发布状态"><el-select v-model="searchForm.status" placeholder="请选择" clearable style="width: 120px;"><el-option label="发布" value="published" /><el-option label="草稿" value="draft" /></el-select></el-form-item>
                <el-form-item label="发布时间"><el-date-picker v-model="searchForm.timeRange" type="daterange" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" style="width: 300px;" /></el-form-item>
                <el-form-item><el-button type="primary" @click="handleSearch"><el-icon><Search /></el-icon>搜索</el-button><el-button @click="resetForm"><el-icon><Refresh /></el-icon>重置</el-button></el-form-item>
              </el-form>
            </div>
            
            <!-- 公告列表 -->
            <el-table :data="announcementList" style="width: 100%" border stripe>
              <el-table-column prop="announcementId" label="公告ID" width="120" />
              <el-table-column prop="title" label="公告标题" min-width="300" show-overflow-tooltip />
              <el-table-column prop="author" label="发布人" width="120" />
              <el-table-column prop="publishTime" label="发布时间" width="180" />
              <el-table-column prop="status" label="状态" width="100"><template #default="scope"><el-tag :type="scope.row.status === 'published' ? 'success' : 'info'"> {{ getStatusName(scope.row.status) }}</el-tag></template></el-table-column>
              <el-table-column prop="viewCount" label="浏览量" width="100" align="right" />
              <el-table-column label="操作" width="220" fixed="right">
                <template #default="scope">
                  <el-button type="primary" size="small" @click="handleViewAnnouncement(scope.row)"><el-icon><View /></el-icon>查看</el-button>
                  <el-button type="warning" size="small" @click="handleEditAnnouncement(scope.row)"><el-icon><Edit /></el-icon>编辑</el-button>
                  <el-button type="danger" size="small" @click="handleDeleteAnnouncement(scope.row)"><el-icon><Delete /></el-icon>删除</el-button>
                </template>
              </el-table-column>
            </el-table>
            <div class="pagination-wrapper"><el-pagination v-model:current-page="pagination.currentPage" v-model:page-size="pagination.pageSize" :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next, jumper" :total="total" @size-change="handleSizeChange" @current-change="handleCurrentChange" /></div>
          </el-tab-pane>
          
          <!-- 帮助中心 -->
          <el-tab-pane label="帮助中心" name="help">
            <div class="help-center">
              <el-card shadow="hover" style="margin-bottom: 20px;">
                <template #header>
                  <div class="help-header">
                    <span>常见问题</span>
                  </div>
                </template>
                <div class="faq-list">
                  <el-collapse v-model="activeFaqNames">
                    <el-collapse-item v-for="faq in faqList" :key="faq.id" :title="faq.question" :name="faq.id">
                      <div class="faq-answer">{{ faq.answer }}</div>
                    </el-collapse-item>
                  </el-collapse>
                </div>
              </el-card>
              
              <el-card shadow="hover">
                <template #header>
                  <div class="help-header">
                    <span>使用指南</span>
                  </div>
                </template>
                <div class="guide-list">
                  <el-card v-for="guide in guideList" :key="guide.id" shadow="hover" style="margin-bottom: 15px;">
                    <div class="guide-item">
                      <h4>{{ guide.title }}</h4>
                      <p class="guide-description">{{ guide.description }}</p>
                      <el-button type="primary" size="small" @click="handleViewGuide(guide)">查看详情</el-button>
                    </div>
                  </el-card>
                </div>
              </el-card>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
    </el-card>
    
    <!-- 公告对话框 -->
    <el-dialog v-model="announcementDialogVisible" :title="announcementDialogTitle" width="800px">
      <el-form :model="announcementForm" label-width="120px" class="announcement-form">
        <el-form-item label="公告标题" required><el-input v-model="announcementForm.title" placeholder="请输入公告标题" style="width: 100%;" /></el-form-item>
        <el-form-item label="公告内容" required><el-input v-model="announcementForm.content" type="textarea" :rows="8" placeholder="请输入公告内容" style="width: 100%;" /></el-form-item>
        <el-form-item label="发布人"><el-input v-model="announcementForm.author" placeholder="请输入发布人" style="width: 100%;" /></el-form-item>
        <el-form-item label="状态"><el-select v-model="announcementForm.status" placeholder="请选择状态" style="width: 100%;"><el-option label="发布" value="published" /><el-option label="草稿" value="draft" /></el-select></el-form-item>
      </el-form>
      <template #footer><el-button @click="announcementDialogVisible = false">取消</el-button><el-button type="primary" @click="handleSaveAnnouncement">保存</el-button></template>
    </el-dialog>
    
    <!-- 公告详情对话框 -->
    <el-dialog v-model="detailDialogVisible" :title="'公告详情 - ' + (currentAnnouncement?.title || '')" width="800px">
      <div v-if="currentAnnouncement" class="detail-dialog">
        <div class="announcement-detail">
          <h3>{{ currentAnnouncement.title }}</h3>
          <div class="announcement-meta">
            <span>发布人: {{ currentAnnouncement.author }}</span>
            <span>发布时间: {{ currentAnnouncement.publishTime }}</span>
            <span>浏览量: {{ currentAnnouncement.viewCount }}</span>
          </div>
          <div class="announcement-content">{{ currentAnnouncement.content }}</div>
        </div>
      </div>
      <template #footer><el-button @click="detailDialogVisible = false">关闭</el-button></template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Refresh, Search, View, Edit, Delete } from '@element-plus/icons-vue'

export default {
  name: 'Announcement',
  components: { Plus, Refresh, Search, View, Edit, Delete },
  setup() {
    const loading = ref(false)
    const activeTab = ref('announcement')
    const announcementDialogVisible = ref(false)
    const detailDialogVisible = ref(false)
    const announcementDialogTitle = ref('发布公告')
    const currentAnnouncement = ref(null)
    const activeFaqNames = ref(['1'])
    
    // 搜索和分页
    const searchForm = reactive({ title: '', status: '', timeRange: [] })
    const pagination = reactive({ currentPage: 1, pageSize: 10 })
    const total = ref(30)
    
    // 公告列表
    const announcementList = ref([
      { announcementId: 'ANN001', title: '系统升级通知', author: 'admin', content: '尊敬的用户，系统将于2026年4月10日凌晨2:00-4:00进行升级维护，请提前做好相关准备。', publishTime: '2026-04-09 10:00:00', status: 'published', viewCount: 120 },
      { announcementId: 'ANN002', title: '风险评估功能上线', author: 'admin', content: '新的风险评估功能已上线，支持更详细的风险分析和报告生成。', publishTime: '2026-04-08 14:00:00', status: 'published', viewCount: 85 },
      { announcementId: 'ANN003', title: '用户培训通知', author: 'admin', content: '将于2026年4月15日举办系统使用培训，欢迎大家参加。', publishTime: '2026-04-07 09:00:00', status: 'published', viewCount: 60 },
      { announcementId: 'ANN004', title: '功能优化计划', author: 'admin', content: '下一阶段将对风险分析模块进行优化，提升系统性能。', publishTime: '2026-04-06 16:00:00', status: 'draft', viewCount: 0 }
    ])
    
    // 公告表单
    const announcementForm = reactive({
      title: '',
      content: '',
      author: 'admin',
      status: 'published'
    })
    
    // 常见问题
    const faqList = ref([
      { id: '1', question: '如何进行风险评估？', answer: '进入风险感知模块，点击风险评估功能，按照系统提示填写相关信息即可完成风险评估。' },
      { id: '2', question: '如何导出风险报告？', answer: '在风险分析报告页面，点击导出按钮，选择导出格式即可下载风险报告。' },
      { id: '3', question: '如何配置预警规则？', answer: '进入协同处置模块的预警管理页面，点击新增规则，设置规则条件和阈值。' },
      { id: '4', question: '如何查看系统日志？', answer: '进入系统管理模块的日志审计页面，可以查看和搜索系统操作日志。' },
      { id: '5', question: '如何备份系统数据？', answer: '进入系统管理模块的数据备份与恢复页面，点击创建备份按钮即可。' }
    ])
    
    // 使用指南
    const guideList = ref([
      { id: '1', title: '系统快速入门', description: '系统基本操作指南，帮助新用户快速上手。' },
      { id: '2', title: '风险评估操作手册', description: '详细介绍风险评估的操作流程和注意事项。' },
      { id: '3', title: '预警规则配置指南', description: '指导用户如何配置和管理预警规则。' },
      { id: '4', title: '任务工单管理说明', description: '任务工单的创建、分配和跟踪操作指南。' },
      { id: '5', title: '系统管理员手册', description: '系统管理员的权限管理和系统配置指南。' }
    ])
    
    const handleCreateAnnouncement = () => {
      announcementDialogTitle.value = '发布公告'
      Object.keys(announcementForm).forEach(key => {
        announcementForm[key] = key === 'author' ? 'admin' : key === 'status' ? 'published' : ''
      })
      currentAnnouncement.value = null
      announcementDialogVisible.value = true
    }
    
    const handleEditAnnouncement = (announcement) => {
      announcementDialogTitle.value = '编辑公告'
      currentAnnouncement.value = announcement
      Object.assign(announcementForm, announcement)
      announcementDialogVisible.value = true
    }
    
    const handleSaveAnnouncement = () => {
      if (!announcementForm.title) {
        ElMessage.warning('请输入公告标题')
        return
      }
      if (!announcementForm.content) {
        ElMessage.warning('请输入公告内容')
        return
      }
      ElMessage.success('公告保存成功')
      announcementDialogVisible.value = false
      // 模拟添加或更新公告
      if (currentAnnouncement.value) {
        // 更新现有公告
        const index = announcementList.value.findIndex(item => item.announcementId === currentAnnouncement.value.announcementId)
        if (index !== -1) {
          announcementList.value[index] = { ...announcementForm, announcementId: currentAnnouncement.value.announcementId, publishTime: currentAnnouncement.value.publishTime, viewCount: currentAnnouncement.value.viewCount }
        }
      } else {
        // 添加新公告
        const newAnnouncement = {
          announcementId: 'ANN' + new Date().getTime(),
          ...announcementForm,
          publishTime: new Date().toLocaleString(),
          viewCount: 0
        }
        announcementList.value.unshift(newAnnouncement)
      }
      currentAnnouncement.value = null
    }
    
    const handleViewAnnouncement = (announcement) => {
      currentAnnouncement.value = announcement
      detailDialogVisible.value = true
    }
    
    const handleDeleteAnnouncement = (announcement) => {
      ElMessageBox.confirm('确定要删除此公告吗？', '删除公告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = announcementList.value.findIndex(item => item.announcementId === announcement.announcementId)
        if (index !== -1) {
          announcementList.value.splice(index, 1)
        }
        ElMessage.success('公告删除成功')
      })
    }
    
    const handleViewGuide = (guide) => {
      ElMessage.info('查看指南功能开发中')
    }
    
    const handleRefresh = () => {
      loading.value = true
      setTimeout(() => {
        ElMessage.success('刷新成功')
        loading.value = false
      }, 1000)
    }
    
    const handleSearch = () => {
      ElMessage.info('搜索功能开发中')
    }
    
    const resetForm = () => {
      Object.keys(searchForm).forEach(key => {
        searchForm[key] = key === 'timeRange' ? [] : ''
      })
    }
    
    const handleSizeChange = (size) => {
      pagination.pageSize = size
    }
    
    const handleCurrentChange = (current) => {
      pagination.currentPage = current
    }
    
    const handleTabChange = (tab) => {
      console.log('切换到标签页:', tab)
    }
    
    const getStatusName = (status) => {
      switch (status) {
        case 'published': return '发布'
        case 'draft': return '草稿'
        default: return status
      }
    }
    
    onMounted(() => {
      console.log('公告与帮助中心页面加载')
    })
    
    return {
      loading, activeTab, announcementDialogVisible, detailDialogVisible, announcementDialogTitle, currentAnnouncement, activeFaqNames,
      searchForm, pagination, total, announcementList, announcementForm, faqList, guideList,
      handleCreateAnnouncement, handleEditAnnouncement, handleSaveAnnouncement, handleViewAnnouncement, handleDeleteAnnouncement,
      handleViewGuide, handleRefresh, handleSearch, resetForm,
      handleSizeChange, handleCurrentChange, handleTabChange, getStatusName
    }
  }
}
</script>

<style scoped>
.announcement {
  padding: 20px;
}
.page-card {
  margin-bottom: 20px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.header-actions {
  display: flex;
  gap: 10px;
}
.search-container {
  margin-bottom: 20px;
}
.search-form {
  background: #f9f9f9;
  padding: 15px;
  border-radius: 8px;
}
.pagination-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
.announcement-form {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
}
.detail-dialog {
  padding: 10px;
}
.announcement-detail {
  padding: 20px;
}
.announcement-detail h3 {
  margin-bottom: 15px;
  color: #303133;
}
.announcement-meta {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
  color: #909399;
  font-size: 14px;
}
.announcement-content {
  line-height: 1.6;
  color: #303133;
}
.help-center {
  padding: 10px;
}
.help-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.faq-list {
  margin-top: 15px;
}
.faq-answer {
  padding: 15px;
  background: #f9f9f9;
  border-radius: 4px;
  margin-top: 10px;
}
.guide-list {
  margin-top: 15px;
}
.guide-item {
  padding: 15px;
}
.guide-item h4 {
  margin-bottom: 10px;
  color: #303133;
}
.guide-description {
  margin-bottom: 15px;
  color: #606266;
  line-height: 1.5;
}
</style>