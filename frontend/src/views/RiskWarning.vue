<template>
  <div class="risk-warning">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>风险预警管理</span>
          <div class="header-actions">
            <el-button type="primary" size="small" @click="handleAddRule"><el-icon><Plus /></el-icon>新增规则</el-button>
            <el-button type="success" size="small" @click="handleRefresh"><el-icon><Refresh /></el-icon>刷新</el-button>
          </div>
        </div>
      </template>
      <div v-loading="loading">
        <!-- 标签页 -->
        <el-tabs v-model="activeTab" @tab-change="handleTabChange">
          <el-tab-pane label="预警规则" name="rules" />
          <el-tab-pane label="预警推送" name="push" />
          <el-tab-pane label="预警处理" name="process" />
          <el-tab-pane label="预警督办" name="supervise" />
        </el-tabs>
        
        <!-- 预警规则 -->
        <div v-if="activeTab === 'rules'" class="tab-content">
          <div class="search-container">
            <el-form :inline="true" :model="ruleSearch" class="search-form">
              <el-form-item label="规则名称"><el-input v-model="ruleSearch.name" placeholder="请输入" clearable style="width: 180px;" /></el-form-item>
              <el-form-item label="规则类型"><el-select v-model="ruleSearch.type" placeholder="请选择" clearable style="width: 120px;"><el-option label="阈值规则" value="threshold" /><el-option label="趋势规则" value="trend" /><el-option label="关联规则" value="correlation" /></el-select></el-form-item>
              <el-form-item label="状态"><el-select v-model="ruleSearch.status" placeholder="请选择" clearable style="width: 120px;"><el-option label="启用" value="enabled" /><el-option label="禁用" value="disabled" /></el-select></el-form-item>
              <el-form-item><el-button type="primary" @click="handleRuleSearch"><el-icon><Search /></el-icon>搜索</el-button><el-button @click="resetRuleForm"><el-icon><Refresh /></el-icon>重置</el-button></el-form-item>
            </el-form>
          </div>
          <el-table :data="ruleList" style="width: 100%" border stripe>
            <el-table-column prop="ruleId" label="规则ID" width="120" />
            <el-table-column prop="ruleName" label="规则名称" min-width="200" show-overflow-tooltip />
            <el-table-column prop="ruleType" label="规则类型" width="120"><template #default="scope">{{ getRuleTypeName(scope.row.ruleType) }}</template></el-table-column>
            <el-table-column prop="description" label="规则描述" min-width="250" show-overflow-tooltip />
            <el-table-column prop="threshold" label="阈值" width="100" align="right" />
            <el-table-column prop="status" label="状态" width="100"><template #default="scope"><el-tag :type="scope.row.status === 'enabled' ? 'success' : 'danger'"> {{ scope.row.status === 'enabled' ? '启用' : '禁用' }}</el-tag></template></el-table-column>
            <el-table-column prop="createTime" label="创建时间" width="180" />
            <el-table-column label="操作" width="280" fixed="right">
              <template #default="scope">
                <el-button type="primary" size="small" @click="handleEditRule(scope.row)" style="margin-right: 5px;">
                  <el-icon><Edit /></el-icon>编辑
                </el-button>
                <el-button v-if="scope.row.status === 'enabled'" type="warning" size="small" @click="handleDisableRule(scope.row)" style="margin-right: 5px;">
                  <el-icon><Switch /></el-icon>禁用
                </el-button>
                <el-button v-else type="success" size="small" @click="handleEnableRule(scope.row)" style="margin-right: 5px;">
                  <el-icon><Switch /></el-icon>启用
                </el-button>
                <el-button type="danger" size="small" @click="handleDeleteRule(scope.row)">
                  <el-icon><Delete /></el-icon>删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
          <div class="pagination-wrapper"><el-pagination v-model:current-page="rulePagination.currentPage" v-model:page-size="rulePagination.pageSize" :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next, jumper" :total="ruleTotal" @size-change="handleRuleSizeChange" @current-change="handleRuleCurrentChange" /></div>
        </div>
        
        <!-- 预警推送 -->
        <div v-if="activeTab === 'push'" class="tab-content">
          <div class="search-container">
            <el-form :inline="true" :model="pushSearch" class="search-form">
              <el-form-item label="预警ID"><el-input v-model="pushSearch.warningId" placeholder="请输入" clearable style="width: 180px;" /></el-form-item>
              <el-form-item label="推送方式"><el-select v-model="pushSearch.pushType" placeholder="请选择" clearable style="width: 120px;"><el-option label="邮件" value="email" /><el-option label="短信" value="sms" /><el-option label="系统消息" value="system" /><el-option label="微信" value="wechat" /></el-select></el-form-item>
              <el-form-item label="推送状态"><el-select v-model="pushSearch.status" placeholder="请选择" clearable style="width: 120px;"><el-option label="成功" value="success" /><el-option label="失败" value="failed" /><el-option label="待推送" value="pending" /></el-select></el-form-item>
              <el-form-item><el-button type="primary" @click="handlePushSearch"><el-icon><Search /></el-icon>搜索</el-button><el-button @click="resetPushForm"><el-icon><Refresh /></el-icon>重置</el-button></el-form-item>
            </el-form>
          </div>
          <el-table :data="pushList" style="width: 100%" border stripe>
            <el-table-column prop="pushId" label="推送ID" width="120" />
            <el-table-column prop="warningId" label="预警ID" width="120" />
            <el-table-column prop="pushType" label="推送方式" width="100"><template #default="scope">{{ getPushTypeName(scope.row.pushType) }}</template></el-table-column>
            <el-table-column prop="recipient" label="接收人" min-width="150" show-overflow-tooltip />
            <el-table-column prop="content" label="推送内容" min-width="250" show-overflow-tooltip />
            <el-table-column prop="status" label="状态" width="100"><template #default="scope"><el-tag :type="scope.row.status === 'success' ? 'success' : scope.row.status === 'failed' ? 'danger' : 'warning'"> {{ getPushStatusName(scope.row.status) }}</el-tag></template></el-table-column>
            <el-table-column prop="pushTime" label="推送时间" width="180" />
            <el-table-column label="操作" width="120" fixed="right"><template #default="scope"><el-button v-if="scope.row.status === 'failed'" type="primary" size="small" @click="handleRetryPush(scope.row)"><el-icon><Refresh /></el-icon>重试</el-button></template></el-table-column>
          </el-table>
          <div class="pagination-wrapper"><el-pagination v-model:current-page="pushPagination.currentPage" v-model:page-size="pushPagination.pageSize" :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next, jumper" :total="pushTotal" @size-change="handlePushSizeChange" @current-change="handlePushCurrentChange" /></div>
        </div>
        
        <!-- 预警处理 -->
        <div v-if="activeTab === 'process'" class="tab-content">
          <div class="search-container">
            <el-form :inline="true" :model="processSearch" class="search-form">
              <el-form-item label="预警ID"><el-input v-model="processSearch.warningId" placeholder="请输入" clearable style="width: 180px;" /></el-form-item>
              <el-form-item label="风险等级"><el-select v-model="processSearch.riskLevel" placeholder="请选择" clearable style="width: 120px;"><el-option label="高风险" value="high" /><el-option label="中风险" value="medium" /><el-option label="低风险" value="low" /></el-select></el-form-item>
              <el-form-item label="处理状态"><el-select v-model="processSearch.status" placeholder="请选择" clearable style="width: 120px;"><el-option label="待处理" value="pending" /><el-option label="处理中" value="processing" /><el-option label="已处理" value="processed" /><el-option label="已关闭" value="closed" /></el-select></el-form-item>
              <el-form-item><el-button type="primary" @click="handleProcessSearch"><el-icon><Search /></el-icon>搜索</el-button><el-button @click="resetProcessForm"><el-icon><Refresh /></el-icon>重置</el-button></el-form-item>
            </el-form>
          </div>
          <el-table :data="processList" style="width: 100%" border stripe>
            <el-table-column prop="warningId" label="预警ID" width="120" />
            <el-table-column prop="riskName" label="风险名称" min-width="200" show-overflow-tooltip />
            <el-table-column prop="riskLevel" label="风险等级" width="100"><template #default="scope"><el-tag :type="scope.row.riskLevel === 'high' ? 'danger' : scope.row.riskLevel === 'medium' ? 'warning' : 'success'"> {{ getRiskLevelName(scope.row.riskLevel) }}</el-tag></template></el-table-column>
            <el-table-column prop="description" label="风险描述" min-width="250" show-overflow-tooltip />
            <el-table-column prop="createTime" label="创建时间" width="180" />
            <el-table-column prop="status" label="状态" width="100"><template #default="scope"><el-tag :type="scope.row.status === 'pending' ? 'warning' : scope.row.status === 'processing' ? 'info' : scope.row.status === 'processed' ? 'success' : 'danger'"> {{ getProcessStatusName(scope.row.status) }}</el-tag></template></el-table-column>
            <el-table-column prop="handler" label="处理人" width="120" />
            <el-table-column label="操作" width="150" fixed="right"><template #default="scope"><el-button type="primary" size="small" @click="handleProcessWarning(scope.row)"><el-icon><View /></el-icon>处理</el-button></template></el-table-column>
          </el-table>
          <div class="pagination-wrapper"><el-pagination v-model:current-page="processPagination.currentPage" v-model:page-size="processPagination.pageSize" :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next, jumper" :total="processTotal" @size-change="handleProcessSizeChange" @current-change="handleProcessCurrentChange" /></div>
        </div>
        
        <!-- 预警督办 -->
        <div v-if="activeTab === 'supervise'" class="tab-content">
          <div class="search-container">
            <el-form :inline="true" :model="superviseSearch" class="search-form">
              <el-form-item label="督办ID"><el-input v-model="superviseSearch.superviseId" placeholder="请输入" clearable style="width: 180px;" /></el-form-item>
              <el-form-item label="预警ID"><el-input v-model="superviseSearch.warningId" placeholder="请输入" clearable style="width: 180px;" /></el-form-item>
              <el-form-item label="督办状态"><el-select v-model="superviseSearch.status" placeholder="请选择" clearable style="width: 120px;"><el-option label="待督办" value="pending" /><el-option label="督办中" value="supervising" /><el-option label="已完成" value="completed" /></el-select></el-form-item>
              <el-form-item><el-button type="primary" @click="handleSuperviseSearch"><el-icon><Search /></el-icon>搜索</el-button><el-button @click="resetSuperviseForm"><el-icon><Refresh /></el-icon>重置</el-button></el-form-item>
            </el-form>
          </div>
          <el-table :data="superviseList" style="width: 100%" border stripe>
            <el-table-column prop="superviseId" label="督办ID" width="120" />
            <el-table-column prop="warningId" label="预警ID" width="120" />
            <el-table-column prop="warningName" label="预警名称" min-width="200" show-overflow-tooltip />
            <el-table-column prop="supervisor" label="督办人" width="120" />
            <el-table-column prop="deadline" label="截止时间" width="180" />
            <el-table-column prop="status" label="状态" width="100"><template #default="scope"><el-tag :type="scope.row.status === 'pending' ? 'warning' : scope.row.status === 'supervising' ? 'info' : 'success'"> {{ getSuperviseStatusName(scope.row.status) }}</el-tag></template></el-table-column>
            <el-table-column prop="createTime" label="创建时间" width="180" />
            <el-table-column label="操作" width="150" fixed="right"><template #default="scope"><el-button type="primary" size="small" @click="handleViewSupervise(scope.row)"><el-icon><View /></el-icon>查看</el-button></template></el-table-column>
          </el-table>
          <div class="pagination-wrapper"><el-pagination v-model:current-page="supervisePagination.currentPage" v-model:page-size="supervisePagination.pageSize" :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next, jumper" :total="superviseTotal" @size-change="handleSuperviseSizeChange" @current-change="handleSuperviseCurrentChange" /></div>
        </div>
      </div>
    </el-card>
    
    <!-- 规则编辑对话框 -->
    <el-dialog v-model="ruleDialogVisible" :title="ruleDialogTitle" width="600px">
      <el-form :model="ruleForm" label-width="120px" class="rule-form">
        <el-form-item label="规则名称" required><el-input v-model="ruleForm.ruleName" placeholder="请输入规则名称" style="width: 100%;" /></el-form-item>
        <el-form-item label="规则类型" required><el-select v-model="ruleForm.ruleType" placeholder="请选择规则类型" style="width: 100%;"><el-option label="阈值规则" value="threshold" /><el-option label="趋势规则" value="trend" /><el-option label="关联规则" value="correlation" /></el-select></el-form-item>
        <el-form-item label="规则描述"><el-input v-model="ruleForm.description" type="textarea" :rows="3" placeholder="请输入规则描述" style="width: 100%;" /></el-form-item>
        <el-form-item label="阈值" required><el-input-number v-model="ruleForm.threshold" :min="0" :max="100" style="width: 100%;" /></el-form-item>
        <el-form-item label="状态"><el-switch v-model="ruleForm.status" active-value="enabled" inactive-value="disabled" /></el-form-item>
      </el-form>
      <template #footer><el-button @click="ruleDialogVisible = false">取消</el-button><el-button type="primary" @click="handleSaveRule">保存</el-button></template>
    </el-dialog>
    
    <!-- 预警处理对话框 -->
    <el-dialog v-model="processDialogVisible" :title="'处理预警 - ' + (currentWarning?.warningId || '')" width="800px">
      <div v-if="currentWarning" class="process-dialog">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="预警ID">{{ currentWarning.warningId }}</el-descriptions-item>
          <el-descriptions-item label="风险名称">{{ currentWarning.riskName }}</el-descriptions-item>
          <el-descriptions-item label="风险等级">{{ getRiskLevelName(currentWarning.riskLevel) }}</el-descriptions-item>
          <el-descriptions-item label="风险描述">{{ currentWarning.description }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ currentWarning.createTime }}</el-descriptions-item>
          <el-descriptions-item label="当前状态">{{ getProcessStatusName(currentWarning.status) }}</el-descriptions-item>
        </el-descriptions>
        <el-form :model="processForm" label-width="120px" class="process-form" style="margin-top: 20px;">
          <el-form-item label="处理意见" required><el-input v-model="processForm.remark" type="textarea" :rows="4" placeholder="请输入处理意见" style="width: 100%;" /></el-form-item>
          <el-form-item label="处理状态" required><el-select v-model="processForm.status" placeholder="请选择处理状态" style="width: 100%;"><el-option label="处理中" value="processing" /><el-option label="已处理" value="processed" /><el-option label="已关闭" value="closed" /></el-select></el-form-item>
          <el-form-item label="处理人" required><el-input v-model="processForm.handler" placeholder="请输入处理人" style="width: 100%;" /></el-form-item>
        </el-form>
      </div>
      <template #footer><el-button @click="processDialogVisible = false">取消</el-button><el-button type="primary" @click="handleSubmitProcess">提交处理</el-button></template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, Refresh, Search, Edit, Switch, Delete, View } from '@element-plus/icons-vue'

export default {
  name: 'RiskWarning',
  components: { Plus, Refresh, Search, Edit, Switch, Delete, View },
  setup() {
    const loading = ref(false)
    const activeTab = ref('rules')
    const ruleDialogVisible = ref(false)
    const processDialogVisible = ref(false)
    const ruleDialogTitle = ref('新增规则')
    const currentWarning = ref(null)
    
    // 规则相关
    const ruleSearch = reactive({ name: '', type: '', status: '' })
    const rulePagination = reactive({ currentPage: 1, pageSize: 10 })
    const ruleTotal = ref(50)
    const ruleList = ref([
      { ruleId: 'RULE001', ruleName: '核心芯片供应风险阈值', ruleType: 'threshold', description: '当核心芯片供应商风险得分超过80时触发预警', threshold: 80, status: 'enabled', createTime: '2026-04-01 10:00:00' },
      { ruleId: 'RULE002', ruleName: '原材料价格上涨趋势', ruleType: 'trend', description: '当原材料价格连续3个月上涨超过10%时触发预警', threshold: 10, status: 'enabled', createTime: '2026-03-15 14:00:00' },
      { ruleId: 'RULE003', ruleName: '地缘政治风险关联', ruleType: 'correlation', description: '当地缘政治风险与供应链节点重合时触发预警', threshold: 70, status: 'disabled', createTime: '2026-03-01 09:00:00' },
      { ruleId: 'RULE004', ruleName: '物流延迟风险', ruleType: 'threshold', description: '当物流延迟率超过15%时触发预警', threshold: 15, status: 'enabled', createTime: '2026-02-20 16:00:00' },
      { ruleId: 'RULE005', ruleName: '供应商财务风险', ruleType: 'threshold', description: '当供应商财务风险得分超过75时触发预警', threshold: 75, status: 'enabled', createTime: '2026-02-10 11:00:00' }
    ])
    const ruleForm = reactive({ ruleName: '', ruleType: 'threshold', description: '', threshold: 0, status: 'enabled' })
    
    // 推送相关
    const pushSearch = reactive({ warningId: '', pushType: '', status: '' })
    const pushPagination = reactive({ currentPage: 1, pageSize: 10 })
    const pushTotal = ref(100)
    const pushList = ref([
      { pushId: 'PUSH001', warningId: 'WARN001', pushType: 'email', recipient: 'zhang.san@haier.com', content: '核心芯片供应风险预警：供应商A风险得分85', status: 'success', pushTime: '2026-04-09 10:00:00' },
      { pushId: 'PUSH002', warningId: 'WARN001', pushType: 'sms', recipient: '13800138000', content: '核心芯片供应风险预警，请及时处理', status: 'success', pushTime: '2026-04-09 10:00:00' },
      { pushId: 'PUSH003', warningId: 'WARN002', pushType: 'system', recipient: 'system_admin', content: '原材料价格上涨趋势预警', status: 'success', pushTime: '2026-04-08 14:00:00' },
      { pushId: 'PUSH004', warningId: 'WARN003', pushType: 'wechat', recipient: 'wang.wu', content: '地缘政治风险关联预警', status: 'failed', pushTime: '2026-04-07 09:00:00' },
      { pushId: 'PUSH005', warningId: 'WARN004', pushType: 'email', recipient: 'li.si@haier.com', content: '物流延迟风险预警', status: 'pending', pushTime: '2026-04-06 16:00:00' }
    ])
    
    // 处理相关
    const processSearch = reactive({ warningId: '', riskLevel: '', status: '' })
    const processPagination = reactive({ currentPage: 1, pageSize: 10 })
    const processTotal = ref(80)
    const processList = ref([
      { warningId: 'WARN001', riskName: '核心芯片供应短缺', riskLevel: 'high', description: '核心芯片供应商A生产能力不足，风险得分85', createTime: '2026-04-09 10:00:00', status: 'pending', handler: '' },
      { warningId: 'WARN002', riskName: '原材料价格上涨', riskLevel: 'medium', description: '主要原材料价格连续3个月上涨12%', createTime: '2026-04-08 14:00:00', status: 'processing', handler: '张三' },
      { warningId: 'WARN003', riskName: '地缘政治风险关联', riskLevel: 'high', description: '中东地区冲突可能影响能源供应', createTime: '2026-04-07 09:00:00', status: 'processed', handler: '李四' },
      { warningId: 'WARN004', riskName: '物流延迟', riskLevel: 'medium', description: '物流延迟率达到18%', createTime: '2026-04-06 16:00:00', status: 'closed', handler: '王五' },
      { warningId: 'WARN005', riskName: '供应商财务风险', riskLevel: 'high', description: '供应商B财务风险得分78', createTime: '2026-04-05 11:00:00', status: 'pending', handler: '' }
    ])
    const processForm = reactive({ remark: '', status: 'processing', handler: '' })
    
    // 督办相关
    const superviseSearch = reactive({ superviseId: '', warningId: '', status: '' })
    const supervisePagination = reactive({ currentPage: 1, pageSize: 10 })
    const superviseTotal = ref(30)
    const superviseList = ref([
      { superviseId: 'SUP001', warningId: 'WARN001', warningName: '核心芯片供应短缺', supervisor: '赵总', deadline: '2026-04-15 18:00:00', status: 'supervising', createTime: '2026-04-09 10:00:00' },
      { superviseId: 'SUP002', warningId: 'WARN003', warningName: '地缘政治风险关联', supervisor: '钱总', deadline: '2026-04-12 18:00:00', status: 'completed', createTime: '2026-04-07 09:00:00' },
      { superviseId: 'SUP003', warningId: 'WARN005', warningName: '供应商财务风险', supervisor: '孙总', deadline: '2026-04-10 18:00:00', status: 'pending', createTime: '2026-04-05 11:00:00' }
    ])
    
    const handleAddRule = () => {
      ruleDialogTitle.value = '新增规则'
      Object.keys(ruleForm).forEach(key => {
        ruleForm[key] = key === 'ruleType' ? 'threshold' : key === 'status' ? 'enabled' : ''
      })
      ruleForm.threshold = 0
      ruleDialogVisible.value = true
    }
    
    const handleEditRule = (rule) => {
      ruleDialogTitle.value = '编辑规则'
      Object.assign(ruleForm, rule)
      ruleDialogVisible.value = true
    }
    
    const handleSaveRule = () => {
      if (!ruleForm.ruleName) {
        ElMessage.warning('请输入规则名称')
        return
      }
      ElMessage.success('保存成功')
      ruleDialogVisible.value = false
    }
    
    const handleEnableRule = (rule) => {
      ElMessage.confirm('确定要启用此规则吗？', '启用规则', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        rule.status = 'enabled'
        ElMessage.success('启用成功')
      })
    }
    
    const handleDisableRule = (rule) => {
      ElMessage.confirm('确定要禁用此规则吗？', '禁用规则', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        rule.status = 'disabled'
        ElMessage.success('禁用成功')
      })
    }
    
    const handleDeleteRule = (rule) => {
      ElMessage.confirm('确定要删除此规则吗？', '删除规则', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'danger'
      }).then(() => {
        const index = ruleList.value.findIndex(item => item.ruleId === rule.ruleId)
        if (index !== -1) {
          ruleList.value.splice(index, 1)
          ElMessage.success('删除成功')
        }
      })
    }
    
    const handleRetryPush = (push) => {
      ElMessage.success('重试推送成功')
      push.status = 'success'
    }
    
    const handleProcessWarning = (warning) => {
      currentWarning.value = warning
      processForm.remark = ''
      processForm.status = warning.status === 'pending' ? 'processing' : warning.status
      processForm.handler = warning.handler || ''
      processDialogVisible.value = true
    }
    
    const handleSubmitProcess = () => {
      if (!processForm.remark) {
        ElMessage.warning('请输入处理意见')
        return
      }
      if (!processForm.handler) {
        ElMessage.warning('请输入处理人')
        return
      }
      ElMessage.success('处理提交成功')
      processDialogVisible.value = false
    }
    
    const handleViewSupervise = (supervise) => {
      ElMessage.info('查看督办详情功能开发中')
    }
    
    const handleRefresh = () => {
      loading.value = true
      setTimeout(() => {
        ElMessage.success('刷新成功')
        loading.value = false
      }, 1000)
    }
    
    const handleTabChange = (tab) => {
      activeTab.value = tab
    }
    
    const getRuleTypeName = (type) => {
      switch (type) {
        case 'threshold': return '阈值规则'
        case 'trend': return '趋势规则'
        case 'correlation': return '关联规则'
        default: return type
      }
    }
    
    const getPushTypeName = (type) => {
      switch (type) {
        case 'email': return '邮件'
        case 'sms': return '短信'
        case 'system': return '系统消息'
        case 'wechat': return '微信'
        default: return type
      }
    }
    
    const getPushStatusName = (status) => {
      switch (status) {
        case 'success': return '成功'
        case 'failed': return '失败'
        case 'pending': return '待推送'
        default: return status
      }
    }
    
    const getRiskLevelName = (level) => {
      switch (level) {
        case 'high': return '高风险'
        case 'medium': return '中风险'
        case 'low': return '低风险'
        default: return level
      }
    }
    
    const getProcessStatusName = (status) => {
      switch (status) {
        case 'pending': return '待处理'
        case 'processing': return '处理中'
        case 'processed': return '已处理'
        case 'closed': return '已关闭'
        default: return status
      }
    }
    
    const getSuperviseStatusName = (status) => {
      switch (status) {
        case 'pending': return '待督办'
        case 'supervising': return '督办中'
        case 'completed': return '已完成'
        default: return status
      }
    }
    
    const handleRuleSearch = () => {
      ElMessage.info('搜索功能开发中')
    }
    
    const resetRuleForm = () => {
      Object.keys(ruleSearch).forEach(key => {
        ruleSearch[key] = ''
      })
    }
    
    const handleRuleSizeChange = (size) => {
      rulePagination.pageSize = size
    }
    
    const handleRuleCurrentChange = (current) => {
      rulePagination.currentPage = current
    }
    
    const handlePushSearch = () => {
      ElMessage.info('搜索功能开发中')
    }
    
    const resetPushForm = () => {
      Object.keys(pushSearch).forEach(key => {
        pushSearch[key] = ''
      })
    }
    
    const handlePushSizeChange = (size) => {
      pushPagination.pageSize = size
    }
    
    const handlePushCurrentChange = (current) => {
      pushPagination.currentPage = current
    }
    
    const handleProcessSearch = () => {
      ElMessage.info('搜索功能开发中')
    }
    
    const resetProcessForm = () => {
      Object.keys(processSearch).forEach(key => {
        processSearch[key] = ''
      })
    }
    
    const handleProcessSizeChange = (size) => {
      processPagination.pageSize = size
    }
    
    const handleProcessCurrentChange = (current) => {
      processPagination.currentPage = current
    }
    
    const handleSuperviseSearch = () => {
      ElMessage.info('搜索功能开发中')
    }
    
    const resetSuperviseForm = () => {
      Object.keys(superviseSearch).forEach(key => {
        superviseSearch[key] = ''
      })
    }
    
    const handleSuperviseSizeChange = (size) => {
      supervisePagination.pageSize = size
    }
    
    const handleSuperviseCurrentChange = (current) => {
      supervisePagination.currentPage = current
    }
    
    onMounted(() => {
      console.log('风险预警管理页面加载')
    })
    
    return {
      loading, activeTab, ruleDialogVisible, processDialogVisible, ruleDialogTitle, currentWarning,
      ruleSearch, rulePagination, ruleTotal, ruleList, ruleForm,
      pushSearch, pushPagination, pushTotal, pushList,
      processSearch, processPagination, processTotal, processList, processForm,
      superviseSearch, supervisePagination, superviseTotal, superviseList,
      handleAddRule, handleEditRule, handleSaveRule, handleEnableRule, handleDisableRule, handleDeleteRule,
      handleRetryPush, handleProcessWarning, handleSubmitProcess, handleViewSupervise,
      handleRefresh, handleTabChange, getRuleTypeName, getPushTypeName, getPushStatusName,
      getRiskLevelName, getProcessStatusName, getSuperviseStatusName,
      handleRuleSearch, resetRuleForm, handleRuleSizeChange, handleRuleCurrentChange,
      handlePushSearch, resetPushForm, handlePushSizeChange, handlePushCurrentChange,
      handleProcessSearch, resetProcessForm, handleProcessSizeChange, handleProcessCurrentChange,
      handleSuperviseSearch, resetSuperviseForm, handleSuperviseSizeChange, handleSuperviseCurrentChange
    }
  }
}
</script>

<style scoped>
.risk-warning {
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
.tab-content {
  margin-top: 20px;
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
.rule-form {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
}
.process-dialog {
  padding: 10px;
}
.process-form {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
}
</style>
