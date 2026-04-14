<template>
  <div class="system-config">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>系统参数配置</span>
          <div class="header-actions">
            <el-button type="primary" size="small" @click="handleSaveConfig"><el-icon><Check /></el-icon>保存配置</el-button>
            <el-button type="success" size="small" @click="handleRefresh"><el-icon><Refresh /></el-icon>刷新</el-button>
          </div>
        </div>
      </template>
      <div v-loading="loading">
        <el-tabs v-model="activeTab" @tab-change="handleTabChange">
          <!-- 基本配置 -->
          <el-tab-pane label="基本配置" name="basic">
            <el-card shadow="hover" style="margin-bottom: 20px;">
              <el-form :model="configForm.basic" label-width="150px" class="config-form">
                <el-form-item label="系统名称"><el-input v-model="configForm.basic.systemName" placeholder="请输入系统名称" style="width: 100%;" /></el-form-item>
                <el-form-item label="系统版本"><el-input v-model="configForm.basic.systemVersion" placeholder="请输入系统版本" style="width: 100%;" /></el-form-item>
                <el-form-item label="系统描述"><el-input v-model="configForm.basic.systemDescription" type="textarea" :rows="3" placeholder="请输入系统描述" style="width: 100%;" /></el-form-item>
                <el-form-item label="系统管理员"><el-input v-model="configForm.basic.systemAdmin" placeholder="请输入系统管理员" style="width: 100%;" /></el-form-item>
                <el-form-item label="联系邮箱"><el-input v-model="configForm.basic.contactEmail" type="email" placeholder="请输入联系邮箱" style="width: 100%;" /></el-form-item>
                <el-form-item label="数据备份频率"><el-select v-model="configForm.basic.backupFrequency" placeholder="请选择" style="width: 100%;"><el-option label="每天" value="daily" /><el-option label="每周" value="weekly" /><el-option label="每月" value="monthly" /></el-select></el-form-item>
              </el-form>
            </el-card>
          </el-tab-pane>
          
          <!-- 邮件配置 -->
          <el-tab-pane label="邮件配置" name="email">
            <el-card shadow="hover" style="margin-bottom: 20px;">
              <el-form :model="configForm.email" label-width="150px" class="config-form">
                <el-form-item label="SMTP服务器"><el-input v-model="configForm.email.smtpServer" placeholder="请输入SMTP服务器地址" style="width: 100%;" /></el-form-item>
                <el-form-item label="SMTP端口"><el-input v-model="configForm.email.smtpPort" type="number" placeholder="请输入SMTP端口" style="width: 100%;" /></el-form-item>
                <el-form-item label="发件人邮箱"><el-input v-model="configForm.email.senderEmail" type="email" placeholder="请输入发件人邮箱" style="width: 100%;" /></el-form-item>
                <el-form-item label="发件人名称"><el-input v-model="configForm.email.senderName" placeholder="请输入发件人名称" style="width: 100%;" /></el-form-item>
                <el-form-item label="SMTP用户名"><el-input v-model="configForm.email.smtpUsername" placeholder="请输入SMTP用户名" style="width: 100%;" /></el-form-item>
                <el-form-item label="SMTP密码"><el-input v-model="configForm.email.smtpPassword" type="password" placeholder="请输入SMTP密码" style="width: 100%;" /></el-form-item>
                <el-form-item label="使用SSL"><el-switch v-model="configForm.email.useSsl" /></el-form-item>
                <el-form-item><el-button type="primary" @click="handleTestEmail">测试邮件发送</el-button></el-form-item>
              </el-form>
            </el-card>
          </el-tab-pane>
          
          <!-- API配置 -->
          <el-tab-pane label="API配置" name="api">
            <el-card shadow="hover" style="margin-bottom: 20px;">
              <el-form :model="configForm.api" label-width="150px" class="config-form">
                <el-form-item label="API基础URL"><el-input v-model="configForm.api.baseUrl" placeholder="请输入API基础URL" style="width: 100%;" /></el-form-item>
                <el-form-item label="API密钥"><el-input v-model="configForm.api.apiKey" type="password" placeholder="请输入API密钥" style="width: 100%;" /></el-form-item>
                <el-form-item label="请求超时时间"><el-input v-model="configForm.api.timeout" type="number" placeholder="请输入请求超时时间（秒）" style="width: 100%;" /></el-form-item>
                <el-form-item label="最大重试次数"><el-input v-model="configForm.api.maxRetries" type="number" placeholder="请输入最大重试次数" style="width: 100%;" /></el-form-item>
                <el-form-item label="启用API日志"><el-switch v-model="configForm.api.enableApiLog" /></el-form-item>
              </el-form>
            </el-card>
          </el-tab-pane>
          
          <!-- 安全配置 -->
          <el-tab-pane label="安全配置" name="security">
            <el-card shadow="hover" style="margin-bottom: 20px;">
              <el-form :model="configForm.security" label-width="150px" class="config-form">
                <el-form-item label="密码最小长度"><el-input v-model="configForm.security.passwordMinLength" type="number" placeholder="请输入密码最小长度" style="width: 100%;" /></el-form-item>
                <el-form-item label="密码复杂度要求"><el-select v-model="configForm.security.passwordComplexity" placeholder="请选择" style="width: 100%;"><el-option label="低" value="low" /><el-option label="中" value="medium" /><el-option label="高" value="high" /></el-select></el-form-item>
                <el-form-item label="会话超时时间"><el-input v-model="configForm.security.sessionTimeout" type="number" placeholder="请输入会话超时时间（分钟）" style="width: 100%;" /></el-form-item>
                <el-form-item label="启用双因素认证"><el-switch v-model="configForm.security.enable2fa" /></el-form-item>
                <el-form-item label="登录失败锁定次数"><el-input v-model="configForm.security.loginFailLockCount" type="number" placeholder="请输入登录失败锁定次数" style="width: 100%;" /></el-form-item>
                <el-form-item label="锁定时间"><el-input v-model="configForm.security.lockTime" type="number" placeholder="请输入锁定时间（分钟）" style="width: 100%;" /></el-form-item>
              </el-form>
            </el-card>
          </el-tab-pane>
          
          <!-- 通知配置 -->
          <el-tab-pane label="通知配置" name="notification">
            <el-card shadow="hover" style="margin-bottom: 20px;">
              <el-form :model="configForm.notification" label-width="150px" class="config-form">
                <el-form-item label="启用邮件通知"><el-switch v-model="configForm.notification.enableEmail" /></el-form-item>
                <el-form-item label="启用短信通知"><el-switch v-model="configForm.notification.enableSms" /></el-form-item>
                <el-form-item label="启用系统通知"><el-switch v-model="configForm.notification.enableSystem" /></el-form-item>
                <el-form-item label="通知频率" v-if="configForm.notification.enableEmail"><el-select v-model="configForm.notification.emailFrequency" placeholder="请选择" style="width: 100%;"><el-option label="实时" value="realtime" /><el-option label="每小时" value="hourly" /><el-option label="每天" value="daily" /></el-select></el-form-item>
                <el-form-item label="短信服务提供商" v-if="configForm.notification.enableSms"><el-select v-model="configForm.notification.smsProvider" placeholder="请选择" style="width: 100%;"><el-option label="阿里云" value="aliyun" /><el-option label="腾讯云" value="tencent" /><el-option label="华为云" value="huawei" /></el-select></el-form-item>
              </el-form>
            </el-card>
          </el-tab-pane>
        </el-tabs>
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Check, Refresh } from '@element-plus/icons-vue'

export default {
  name: 'SystemConfig',
  components: { Check, Refresh },
  setup() {
    const loading = ref(false)
    const activeTab = ref('basic')
    
    // 配置表单
    const configForm = reactive({
      basic: {
        systemName: '海尔外部风险管理系统',
        systemVersion: '1.0.0',
        systemDescription: '海尔集团外部风险识别、评估、处置和学习的综合管理系统',
        systemAdmin: 'admin',
        contactEmail: 'admin@haier.com',
        backupFrequency: 'daily'
      },
      email: {
        smtpServer: 'smtp.example.com',
        smtpPort: 587,
        senderEmail: 'system@haier.com',
        senderName: '海尔风险管理系统',
        smtpUsername: 'system',
        smtpPassword: 'password',
        useSsl: true
      },
      api: {
        baseUrl: 'http://localhost:8080/api',
        apiKey: 'your-api-key',
        timeout: 30,
        maxRetries: 3,
        enableApiLog: true
      },
      security: {
        passwordMinLength: 8,
        passwordComplexity: 'medium',
        sessionTimeout: 30,
        enable2fa: false,
        loginFailLockCount: 5,
        lockTime: 30
      },
      notification: {
        enableEmail: true,
        enableSms: false,
        enableSystem: true,
        emailFrequency: 'realtime',
        smsProvider: 'aliyun'
      }
    })
    
    const handleSaveConfig = () => {
      loading.value = true
      setTimeout(() => {
        ElMessage.success('配置保存成功')
        loading.value = false
      }, 1000)
    }
    
    const handleRefresh = () => {
      loading.value = true
      setTimeout(() => {
        ElMessage.success('配置刷新成功')
        loading.value = false
      }, 1000)
    }
    
    const handleTestEmail = () => {
      ElMessage.info('邮件发送测试功能开发中')
    }
    
    const handleTabChange = (tab) => {
      console.log('切换到标签页:', tab)
    }
    
    onMounted(() => {
      console.log('系统参数配置页面加载')
    })
    
    return {
      loading, activeTab, configForm,
      handleSaveConfig, handleRefresh, handleTestEmail, handleTabChange
    }
  }
}
</script>

<style scoped>
.system-config {
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
.config-form {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
}
</style>
