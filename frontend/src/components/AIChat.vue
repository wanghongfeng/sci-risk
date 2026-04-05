<template>
  <div class="ai-chat-widget" :class="{ 'collapsed': isCollapsed }">
    <div class="ai-chat-toggle" @click="toggleChat">
      <span v-if="isCollapsed">AI 助手</span>
      <span v-else>×</span>
    </div>

    <div class="ai-chat-window" v-if="!isCollapsed">
      <div class="ai-chat-header">
        <h3>AI 智能助手</h3>
      </div>

      <div class="ai-chat-messages" ref="messagesRef">
        <div v-if="messages.length === 0" class="ai-chat-empty">
          您好，我是AI智能助手，有什么可以帮您的吗？
        </div>
        <div
          v-for="(msg, index) in messages"
          :key="index"
          :class="['ai-message', msg.role]"
        >
          <div class="ai-message-content">{{ msg.content }}</div>
          <div v-if="msg.role === 'assistant' && msg.agent" class="ai-message-meta">
            来自 {{ msg.agent }}
          </div>
        </div>
        <div v-if="loading" class="ai-message assistant">
          <div class="ai-message-content">思考中...</div>
        </div>
      </div>

      <div class="ai-chat-input">
        <input
          v-model="input"
          @keyup.enter="send"
          placeholder="输入问题后按回车..."
          :disabled="loading"
        />
        <button @click="send" :disabled="loading">
          发送
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import aiService from '../aiService'

const isCollapsed = ref(true)
const input = ref('')
const messages = ref([])
const loading = ref(false)
const messagesRef = ref(null)

const toggleChat = () => {
  isCollapsed.value = !isCollapsed.value
}

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesRef.value) {
      messagesRef.value.scrollTop = messagesRef.value.scrollHeight
    }
  })
}

const send = async () => {
  if (!input.value.trim() || loading.value) return

  const userMessage = input.value
  input.value = ''

  messages.value.push({
    role: 'user',
    content: userMessage
  })
  scrollToBottom()

  try {
    loading.value = true
    const result = await aiService.chat(userMessage)

    messages.value.push({
      role: 'assistant',
      content: result.response,
      agent: result.agent_name
    })
    scrollToBottom()
  } catch (error) {
    messages.value.push({
      role: 'assistant',
      content: `错误: ${error.message}`,
      agent: '系统'
    })
    scrollToBottom()
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.ai-chat-widget {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 9999;
  font-family: Arial, sans-serif;
}

.ai-chat-widget.collapsed .ai-chat-toggle {
  width: auto;
  padding: 12px 20px;
  border-radius: 25px;
}

.ai-chat-toggle {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
  color: white;
  font-size: 16px;
  font-weight: bold;
  transition: all 0.3s ease;
}

.ai-chat-toggle:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
}

.ai-chat-window {
  position: absolute;
  bottom: 70px;
  right: 0;
  width: 380px;
  height: 500px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.ai-chat-header {
  padding: 16px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.ai-chat-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
}

.ai-chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  background: #f7f8fa;
}

.ai-chat-empty {
  text-align: center;
  color: #999;
  padding: 40px 20px;
  font-size: 14px;
}

.ai-message {
  margin-bottom: 12px;
  display: flex;
  flex-direction: column;
}

.ai-message.user {
  align-items: flex-end;
}

.ai-message.assistant {
  align-items: flex-start;
}

.ai-message-content {
  max-width: 80%;
  padding: 10px 14px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.5;
  word-break: break-word;
}

.ai-message.user .ai-message-content {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-bottom-right-radius: 4px;
}

.ai-message.assistant .ai-message-content {
  background: white;
  color: #333;
  border-bottom-left-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.ai-message-meta {
  font-size: 11px;
  color: #999;
  margin-top: 4px;
  padding: 0 4px;
}

.ai-chat-input {
  padding: 12px 16px;
  background: white;
  border-top: 1px solid #eee;
  display: flex;
  gap: 8px;
}

.ai-chat-input input {
  flex: 1;
  padding: 10px 14px;
  border: 1px solid #ddd;
  border-radius: 20px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
}

.ai-chat-input input:focus {
  border-color: #667eea;
}

.ai-chat-input button {
  padding: 10px 18px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 20px;
  font-size: 14px;
  cursor: pointer;
  transition: opacity 0.2s;
}

.ai-chat-input button:hover:not(:disabled) {
  opacity: 0.9;
}

.ai-chat-input button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>