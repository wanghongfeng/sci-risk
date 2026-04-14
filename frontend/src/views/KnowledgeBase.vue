<template>
  <div class="knowledge-base">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>知识沉淀与经验库</span>
          <div class="header-actions">
            <el-button type="primary" size="small" @click="handleCreateKnowledge"><el-icon><Plus /></el-icon>新增知识</el-button>
            <el-button type="success" size="small" @click="handleRefresh"><el-icon><Refresh /></el-icon>刷新</el-button>
          </div>
        </div>
      </template>
      <div v-loading="loading">
        <!-- 搜索和筛选 -->
        <div class="search-container">
          <el-form :inline="true" :model="searchForm" class="search-form">
            <el-form-item label="知识ID"><el-input v-model="searchForm.knowledgeId" placeholder="请输入" clearable style="width: 180px;" /></el-form-item>
            <el-form-item label="知识标题"><el-input v-model="searchForm.title" placeholder="请输入" clearable style="width: 180px;" /></el-form-item>
            <el-form-item label="分类"><el-select v-model="searchForm.category" placeholder="请选择" clearable style="width: 150px;"><el-option label="风险评估" value="risk_assessment" /><el-option label="应对措施" value="measures" /><el-option label="案例分析" value="case_analysis" /><el-option label="最佳实践" value="best_practice" /></el-select></el-form-item>
            <el-form-item label="状态"><el-select v-model="searchForm.status" placeholder="请选择" clearable style="width: 120px;"><el-option label="已发布" value="published" /><el-option label="草稿" value="draft" /></el-select></el-form-item>
            <el-form-item><el-button type="primary" @click="handleSearch"><el-icon><Search /></el-icon>搜索</el-button><el-button @click="resetForm"><el-icon><Refresh /></el-icon>重置</el-button></el-form-item>
          </el-form>
        </div>
        
        <!-- 知识列表 -->
        <el-table :data="knowledgeList" style="width: 100%" border stripe>
          <el-table-column prop="knowledgeId" label="知识ID" width="120" />
          <el-table-column prop="title" label="知识标题" min-width="200" show-overflow-tooltip />
          <el-table-column prop="category" label="分类" width="120"><template #default="scope">{{ getCategoryName(scope.row.category) }}</template></el-table-column>
          <el-table-column prop="author" label="作者" width="120" />
          <el-table-column prop="viewCount" label="浏览量" width="100" align="right" />
          <el-table-column prop="status" label="状态" width="100"><template #default="scope"><el-tag :type="scope.row.status === 'published' ? 'success' : 'info'"> {{ getStatusName(scope.row.status) }}</el-tag></template></el-table-column>
          <el-table-column prop="createTime" label="创建时间" width="180" />
          <el-table-column label="操作" width="220" fixed="right">
            <template #default="scope">
              <el-button type="primary" size="small" @click="handleViewKnowledge(scope.row)"><el-icon><View /></el-icon>查看</el-button>
              <el-button type="warning" size="small" @click="handleEditKnowledge(scope.row)"><el-icon><Edit /></el-icon>编辑</el-button>
              <el-button type="danger" size="small" @click="handleDeleteKnowledge(scope.row)"><el-icon><Delete /></el-icon>删除</el-button>
            </template>
          </el-table-column>
        </el-table>
        <div class="pagination-wrapper"><el-pagination v-model:current-page="pagination.currentPage" v-model:page-size="pagination.pageSize" :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next, jumper" :total="total" @size-change="handleSizeChange" @current-change="handleCurrentChange" /></div>
      </div>
    </el-card>
    
    <!-- 知识对话框 -->
    <el-dialog v-model="knowledgeDialogVisible" :title="knowledgeDialogTitle" width="800px">
      <el-form :model="knowledgeForm" label-width="120px" class="knowledge-form">
        <el-form-item label="知识标题" required><el-input v-model="knowledgeForm.title" placeholder="请输入知识标题" style="width: 100%;" /></el-form-item>
        <el-form-item label="分类" required><el-select v-model="knowledgeForm.category" placeholder="请选择分类" style="width: 100%;"><el-option label="风险评估" value="risk_assessment" /><el-option label="应对措施" value="measures" /><el-option label="案例分析" value="case_analysis" /><el-option label="最佳实践" value="best_practice" /><el-option label="其他" value="other" /></el-select></el-form-item>
        <el-form-item label="作者" required><el-input v-model="knowledgeForm.author" placeholder="请输入作者" style="width: 100%;" /></el-form-item>
        <el-form-item label="内容"><el-input v-model="knowledgeForm.content" type="textarea" :rows="8" placeholder="请输入知识内容" style="width: 100%;" /></el-form-item>
        <el-form-item label="标签"><el-input v-model="knowledgeForm.tags" placeholder="请输入标签，用逗号分隔" style="width: 100%;" /></el-form-item>
        <el-form-item label="状态"><el-select v-model="knowledgeForm.status" placeholder="请选择状态" style="width: 100%;"><el-option label="已发布" value="published" /><el-option label="草稿" value="draft" /></el-select></el-form-item>
      </el-form>
      <template #footer><el-button @click="knowledgeDialogVisible = false">取消</el-button><el-button type="primary" @click="handleSaveKnowledge">保存</el-button></template>
    </el-dialog>
    
    <!-- 知识详情对话框 -->
    <el-dialog v-model="detailDialogVisible" :title="'知识详情 - ' + (currentKnowledge?.title || '')" width="800px">
      <div v-if="currentKnowledge" class="detail-dialog">
        <div class="detail-header">
          <h3>{{ currentKnowledge.title }}</h3>
          <div class="detail-meta">
            <span class="meta-item"><el-tag size="small">{{ getCategoryName(currentKnowledge.category) }}</el-tag></span>
            <span class="meta-item">作者：{{ currentKnowledge.author }}</span>
            <span class="meta-item">浏览量：{{ currentKnowledge.viewCount }}</span>
            <span class="meta-item">创建时间：{{ currentKnowledge.createTime }}</span>
            <span class="meta-item"><el-tag :type="currentKnowledge.status === 'published' ? 'success' : 'info'" size="small">{{ getStatusName(currentKnowledge.status) }}</el-tag></span>
          </div>
        </div>
        
        <div class="detail-content" style="margin-top: 20px; padding: 20px; background: #f9f9f9; border-radius: 8px;">
          {{ currentKnowledge.content }}
        </div>
        
        <div class="detail-tags" style="margin-top: 20px;">
          <span class="tags-label">标签：</span>
          <el-tag v-for="tag in currentKnowledge.tags.split(',')" :key="tag" size="small" style="margin-right: 10px;">{{ tag.trim() }}</el-tag>
        </div>
        
        <!-- 版本历史 -->
        <div class="version-history" style="margin-top: 20px;">
          <h4>版本历史</h4>
          <el-timeline>
            <el-timeline-item v-for="(version, index) in currentKnowledge.versionHistory" :key="index" :timestamp="version.time" :type="version.type">
              <el-card shadow="hover" style="width: 100%;">
                <div class="version-content">
                  <div class="version-title">版本 {{ version.version }}</div>
                  <div class="version-description">{{ version.description }}</div>
                  <div class="version-changes" v-if="version.changes.length > 0">
                    <h5>变更内容：</h5>
                    <ul>
                      <li v-for="(change, i) in version.changes" :key="i">{{ change }}</li>
                    </ul>
                  </div>
                </div>
              </el-card>
            </el-timeline-item>
          </el-timeline>
        </div>
        
        <!-- 评论区 -->
        <div class="comments-section" style="margin-top: 20px;">
          <h4>评论</h4>
          <div class="comments-list" style="max-height: 300px; overflow-y: auto; border: 1px solid #e4e7ed; border-radius: 4px; padding: 10px;">
            <div v-for="(comment, index) in currentKnowledge.comments" :key="index" class="comment-item">
              <div class="comment-header"><span class="comment-user">{{ comment.user }}</span><span class="comment-time">{{ comment.time }}</span></div>
              <div class="comment-content">{{ comment.content }}</div>
            </div>
          </div>
          <div class="comment-input" style="margin-top: 10px;"><el-input v-model="commentContent" type="textarea" :rows="3" placeholder="输入评论内容" style="width: 100%;" /><el-button type="primary" style="margin-top: 10px;" @click="handleAddComment">发表评论</el-button></div>
        </div>
      </div>
      <template #footer>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="handleUpdateVersion">更新版本</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Refresh, Search, View, Edit, Delete } from '@element-plus/icons-vue'

export default {
  name: 'KnowledgeBase',
  components: { Plus, Refresh, Search, View, Edit, Delete },
  setup() {
    const loading = ref(false)
    const knowledgeDialogVisible = ref(false)
    const detailDialogVisible = ref(false)
    const knowledgeDialogTitle = ref('新增知识')
    const currentKnowledge = ref(null)
    const commentContent = ref('')
    
    // 搜索和分页
    const searchForm = reactive({ knowledgeId: '', title: '', category: '', status: '' })
    const pagination = reactive({ currentPage: 1, pageSize: 10 })
    const total = ref(150)
    
    // 知识列表
    const knowledgeList = ref([
      { knowledgeId: 'KNOW001', title: '供应链风险评估方法指南', category: 'risk_assessment', author: '张经理', viewCount: 120, status: 'published', createTime: '2026-04-09 10:00:00' },
      { knowledgeId: 'KNOW002', title: '供应商多元化策略最佳实践', category: 'best_practice', author: '李专家', viewCount: 95, status: 'published', createTime: '2026-04-08 14:00:00' },
      { knowledgeId: 'KNOW003', title: '风险预警机制建设方案', category: 'measures', author: '王工程师', viewCount: 88, status: 'draft', createTime: '2026-04-07 09:00:00' },
      { knowledgeId: 'KNOW004', title: '供应链中断案例分析', category: 'case_analysis', author: '赵分析师', viewCount: 156, status: 'published', createTime: '2026-04-06 16:00:00' }
    ])
    
    // 知识表单
    const knowledgeForm = reactive({
      title: '',
      category: '',
      author: '',
      content: '',
      tags: '',
      status: 'draft'
    })
    
    // 模拟版本历史
    const mockVersionHistory = [
      {
        time: '2026-04-09 10:00:00',
        type: 'primary',
        version: '1.0',
        description: '初始发布',
        changes: ['创建文档', '添加核心内容']
      }
    ]
    
    // 模拟评论
    const mockComments = [
      { user: '用户A', time: '2026-04-09 11:00:00', content: '非常实用的指南，感谢分享！' },
      { user: '用户B', time: '2026-04-09 14:00:00', content: '建议增加更多案例分析' }
    ]
    
    const handleCreateKnowledge = () => {
      knowledgeDialogTitle.value = '新增知识'
      Object.keys(knowledgeForm).forEach(key => {
        knowledgeForm[key] = key === 'status' ? 'draft' : ''
      })
      knowledgeDialogVisible.value = true
    }
    
    const handleEditKnowledge = (knowledge) => {
      knowledgeDialogTitle.value = '编辑知识'
      currentKnowledge.value = knowledge
      Object.assign(knowledgeForm, knowledge)
      knowledgeDialogVisible.value = true
    }
    
    const handleSaveKnowledge = () => {
      if (!knowledgeForm.title) {
        ElMessage.warning('请输入知识标题')
        return
      }
      if (!knowledgeForm.category) {
        ElMessage.warning('请选择分类')
        return
      }
      if (!knowledgeForm.author) {
        ElMessage.warning('请输入作者')
        return
      }
      ElMessage.success('知识保存成功')
      knowledgeDialogVisible.value = false
      // 模拟添加或更新知识
      if (currentKnowledge.value) {
        // 更新现有知识
        const index = knowledgeList.value.findIndex(item => item.knowledgeId === currentKnowledge.value.knowledgeId)
        if (index !== -1) {
          knowledgeList.value[index] = { ...knowledgeForm, knowledgeId: currentKnowledge.value.knowledgeId, createTime: currentKnowledge.value.createTime, viewCount: currentKnowledge.value.viewCount }
        }
      } else {
        // 添加新知识
        const newKnowledge = {
          knowledgeId: 'KNOW' + new Date().getTime(),
          ...knowledgeForm,
          viewCount: 0,
          createTime: new Date().toLocaleString()
        }
        knowledgeList.value.unshift(newKnowledge)
      }
      currentKnowledge.value = null
    }
    
    const handleViewKnowledge = (knowledge) => {
      currentKnowledge.value = {
        ...knowledge,
        versionHistory: mockVersionHistory,
        comments: mockComments
      }
      detailDialogVisible.value = true
      // 模拟增加浏览量
      knowledge.viewCount++
    }
    
    const handleDeleteKnowledge = (knowledge) => {
      ElMessageBox.confirm('确定要删除此知识吗？', '删除知识', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = knowledgeList.value.findIndex(item => item.knowledgeId === knowledge.knowledgeId)
        if (index !== -1) {
          knowledgeList.value.splice(index, 1)
        }
        ElMessage.success('知识删除成功')
      })
    }
    
    const handleUpdateVersion = () => {
      ElMessage.success('版本更新成功')
      // 模拟添加新版本
      currentKnowledge.value.versionHistory.unshift({
        time: new Date().toLocaleString(),
        type: 'warning',
        version: '1.1',
        description: '更新内容',
        changes: ['优化内容结构', '增加新案例']
      })
    }
    
    const handleAddComment = () => {
      if (!commentContent.value) {
        ElMessage.warning('请输入评论内容')
        return
      }
      currentKnowledge.value.comments.push({
        user: '当前用户',
        time: new Date().toLocaleString(),
        content: commentContent.value
      })
      commentContent.value = ''
      ElMessage.success('评论发表成功')
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
        searchForm[key] = ''
      })
    }
    
    const handleSizeChange = (size) => {
      pagination.pageSize = size
    }
    
    const handleCurrentChange = (current) => {
      pagination.currentPage = current
    }
    
    const getCategoryName = (category) => {
      const categoryMap = {
        risk_assessment: '风险评估',
        measures: '应对措施',
        case_analysis: '案例分析',
        best_practice: '最佳实践',
        other: '其他'
      }
      return categoryMap[category] || category
    }
    
    const getStatusName = (status) => {
      switch (status) {
        case 'published': return '已发布'
        case 'draft': return '草稿'
        default: return status
      }
    }
    
    onMounted(() => {
      console.log('知识沉淀与经验库页面加载')
    })
    
    return {
      loading, knowledgeDialogVisible, detailDialogVisible, knowledgeDialogTitle, currentKnowledge, commentContent,
      searchForm, pagination, total, knowledgeList, knowledgeForm,
      handleCreateKnowledge, handleEditKnowledge, handleSaveKnowledge, handleViewKnowledge, handleDeleteKnowledge,
      handleUpdateVersion, handleAddComment, handleRefresh, handleSearch, resetForm, handleSizeChange, handleCurrentChange,
      getCategoryName, getStatusName
    }
  }
}
</script>

<style scoped>
.knowledge-base {
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
.knowledge-form {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
}
.detail-dialog {
  padding: 10px;
}
.detail-header {
  text-align: center;
  margin-bottom: 20px;
}
.detail-header h3 {
  margin-bottom: 10px;
}
.detail-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  justify-content: center;
  font-size: 14px;
  color: #606266;
}
.meta-item {
  display: inline-block;
}
.detail-content {
  margin-top: 20px;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 8px;
  line-height: 1.6;
}
.detail-tags {
  margin-top: 20px;
  font-size: 14px;
}
.tags-label {
  margin-right: 10px;
  color: #606266;
}
.version-history {
  margin-top: 20px;
}
.version-content {
  padding: 10px;
}
.version-title {
  font-weight: bold;
  margin-bottom: 5px;
}
.version-description {
  margin-bottom: 10px;
  font-size: 14px;
}
.version-changes {
  margin-top: 10px;
  font-size: 14px;
}
.version-changes h5 {
  margin-bottom: 5px;
  font-size: 14px;
}
.version-changes ul {
  margin: 0;
  padding-left: 20px;
}
.version-changes li {
  margin-bottom: 3px;
}
.comments-section {
  margin-top: 20px;
}
.comments-list {
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  padding: 10px;
}
.comment-item {
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid #f0f0f0;
}
.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
  font-size: 14px;
}
.comment-user {
  font-weight: bold;
}
.comment-time {
  color: #909399;
}
.comment-content {
  font-size: 14px;
  line-height: 1.5;
}
.comment-input {
  margin-top: 10px;
}
</style>
