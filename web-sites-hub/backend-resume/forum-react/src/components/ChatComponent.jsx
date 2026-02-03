import React, { useState, useRef, useEffect } from 'react'
import MessageContent from './MessageContent'
import './ChatComponent.css'

const API_URL = 'http://agenthub.intra.xiaojukeji.com/v1/chat-messages'
const API_KEY = 'app-GdVMAxRyH3Mj9N72piy1aAgR'

function ChatComponent({ 
  conversations = [], // 已有对话列表
  onSendMessage, 
  onReceiveMessage,
  inputs = {},
  onDutyUsers = [],
  conversationId: initialConversationId = '',
  currentPostId = null,
  currentPostTitle = null
}) {
  const [inputValue, setInputValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [conversationId, setConversationId] = useState(initialConversationId)
  const [parentMessageId, setParentMessageId] = useState(null)
  const messagesEndRef = useRef(null)
  const abortControllerRef = useRef(null)

  const userId = localStorage.getItem('forum_user_id') || `user-${Date.now()}`

  useEffect(() => {
    if (!localStorage.getItem('forum_user_id')) {
      localStorage.setItem('forum_user_id', userId)
    }
  }, [userId])

  useEffect(() => {
    scrollToBottom()
  }, [conversations])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const handleSendMessage = async (query) => {
    if (!query.trim() || isLoading) return
    
    // 防止重复调用
    setIsLoading(true)

    const userMessage = {
      type: 'user',
      content: query,
      timestamp: new Date().toISOString()
    }

    setInputValue('')

    // 通知父组件用户消息
    if (onSendMessage) {
      onSendMessage(userMessage)
    }

    // 取消之前的请求（如果有）
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
    }
    
    // 创建新的 AbortController 用于取消请求
    abortControllerRef.current = new AbortController()

    try {
      // 构建请求体，API 要求必须有 user 字段
      const requestBody = {
        response_mode: 'streaming',
        conversation_id: conversationId || '',
        files: [],
        inputs: inputs || {},
        user: userId,
        query: query
      }
      
      // 只在有值时才添加 parent_message_id
      if (parentMessageId) {
        requestBody.parent_message_id = parentMessageId
      }
      
      console.log('Sending request to:', API_URL)
      console.log('Request body:', JSON.stringify(requestBody, null, 2))
      
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${API_KEY}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody),
        signal: abortControllerRef.current.signal
      })

      if (!response.ok) {
        const errorText = await response.text()
        console.error('API Error:', response.status, errorText)
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`)
      }

      // 检查响应类型
      const contentType = response.headers.get('content-type')
      if (!contentType || !contentType.includes('text/event-stream')) {
        console.warn('Unexpected content-type:', contentType)
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let assistantMessage = {
        type: 'assistant',
        content: '',
        timestamp: new Date().toISOString(),
        messageId: null,
        taskId: null
      }

      // 不在这里通知，等收到第一个 message 事件再通知，避免重复

      let buffer = ''
      
      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        
        // SSE 格式：每个事件以 data: 开头，以 \n\n 结尾
        const lines = buffer.split('\n')
        buffer = lines.pop() || '' // 保留最后一行（可能不完整）
        
        for (const line of lines) {
          if (!line.trim() || !line.startsWith('data: ')) continue
          
          const data = line.slice(6).trim()
          if (!data || data === '[DONE]') continue

          try {
            const json = JSON.parse(data)
            // 完整显示 AI 接口返回信息
            console.log('AI Response Event:', JSON.stringify(json, null, 2))
            
            switch (json.event) {
              case 'message':
                // LLM 返回文本块事件，累积 answer
                if (json.answer) {
                  assistantMessage.content += json.answer
                  if (json.message_id) assistantMessage.messageId = json.message_id
                  if (json.task_id) assistantMessage.taskId = json.task_id
                  if (json.conversation_id) {
                    setConversationId(json.conversation_id)
                  }
                  if (onReceiveMessage) {
                    onReceiveMessage({ ...assistantMessage })
                  }
                }
                break

              case 'message_file':
                if (json.type === 'image' && json.url) {
                  assistantMessage.content += `\n![图片](${json.url})\n`
                  if (onReceiveMessage) {
                    onReceiveMessage({ ...assistantMessage })
                  }
                }
                break

              case 'message_end':
                if (json.conversation_id) {
                  setConversationId(json.conversation_id)
                }
                if (json.message_id) {
                  assistantMessage.messageId = json.message_id
                  setParentMessageId(json.message_id)
                }
                if (json.task_id) {
                  assistantMessage.taskId = json.task_id
                }
                // 显示完整的元数据
                if (json.metadata) {
                  console.log('Message Metadata:', JSON.stringify(json.metadata, null, 2))
                }
                if (onReceiveMessage) {
                  onReceiveMessage({ ...assistantMessage })
                }
                break

              case 'message_replace':
                if (json.answer) {
                  assistantMessage.content = json.answer
                  if (onReceiveMessage) {
                    onReceiveMessage({ ...assistantMessage })
                  }
                }
                break

              case 'error':
                throw new Error(json.message || 'API error')

              case 'ping':
                break

              default:
                console.log('Other event:', json.event, json)
            }
          } catch (e) {
            if (e instanceof SyntaxError) {
              console.error('Error parsing SSE JSON:', e, 'Data:', data)
            } else {
              throw e
            }
          }
        }
      }
      
      // 处理剩余的 buffer
      if (buffer.trim() && buffer.startsWith('data: ')) {
        const data = buffer.slice(6).trim()
        if (data && data !== '[DONE]') {
          try {
            const json = JSON.parse(data)
            console.log('Final AI Response:', JSON.stringify(json, null, 2))
            if (json.event === 'message' && json.answer) {
              assistantMessage.content += json.answer
              if (onReceiveMessage) {
                onReceiveMessage({ ...assistantMessage })
              }
            }
          } catch (e) {
            console.error('Error parsing final buffer:', e)
          }
        }
      }
    } catch (error) {
      if (error.name === 'AbortError') {
        console.log('Request aborted')
      } else {
        console.error('Error sending message:', error)
        console.error('Error details:', {
          name: error.name,
          message: error.message,
          stack: error.stack
        })
        const errorMessage = {
          type: 'assistant',
          content: `❌ 错误: ${error.message}\n\n请检查：\n1. API Key 是否正确\n2. 网络连接是否正常\n3. 查看浏览器控制台获取更多信息`,
          timestamp: new Date().toISOString(),
          error: true
        }
        if (onReceiveMessage) {
          onReceiveMessage(errorMessage)
        }
      }
    } finally {
      setIsLoading(false)
      abortControllerRef.current = null
    }
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    e.stopPropagation() // 防止事件冒泡导致重复提交
    if (!inputValue.trim() || isLoading) return
    handleSendMessage(inputValue)
  }

  const handleNewConversation = () => {
    // 新对话时重置 conversationId 和 parentMessageId
    setConversationId('')
    setParentMessageId(null)
  }

  const handleQuickPrompt = (prompt) => {
    handleSendMessage(prompt)
  }

  useEffect(() => {
    return () => {
      // 组件卸载时取消请求
      if (abortControllerRef.current) {
        abortControllerRef.current.abort()
      }
    }
  }, [])

  return (
    <div className="chat-component">
      <div className="chat-header">
        <div className="chat-header-left">
          <h3>💬 群聊讨论</h3>
          {currentPostTitle && (
            <div className="chat-post-badge">
              📌 {currentPostTitle}
            </div>
          )}
        </div>
        <div className="chat-header-right">
          <button 
            className="chat-btn-icon" 
            onClick={handleNewConversation}
            title="新对话"
          >
            ➕
          </button>
        </div>
      </div>

      <div className="chat-toolbar">
        <button 
          className="chat-toolbar-btn"
          onClick={() => handleQuickPrompt('请帮我解答这个问题')}
          disabled={isLoading}
        >
          快速提问
        </button>
        {onDutyUsers.map(user => (
          <button
            key={user.id}
            className="chat-toolbar-btn"
            onClick={() => handleQuickPrompt(`@${user.name} 请帮忙看看这个问题`)}
            disabled={isLoading}
          >
            @{user.name}
          </button>
        ))}
      </div>

      <div className="chat-messages">
        {conversations.length === 0 ? (
          <div className="chat-empty">
            <p>开始对话...</p>
            <p style={{ fontSize: '0.85rem', color: '#999', marginTop: '0.5rem' }}>
              {currentPostTitle ? `正在讨论: ${currentPostTitle}` : '输入问题或使用快捷按钮'}
            </p>
          </div>
        ) : (
          conversations.map((msg, index) => {
            // 检查是否是最后一条消息且正在加载
            const isLastMessage = index === conversations.length - 1
            const isStreaming = isLoading && isLastMessage && msg.type === 'assistant' && !msg.error
            
            return (
              <div key={msg.id || index} className={`chat-message ${msg.type} ${msg.error ? 'error' : ''}`}>
                <div className="chat-message-header">
                  <div>
                    <span>{msg.type === 'user' ? '👤 用户' : '🤖 助手'}</span>
                    {msg.postTitle && (
                      <span className="chat-message-post-tag">📌 {msg.postTitle}</span>
                    )}
                  </div>
                  <span className="chat-message-time">
                    {new Date(msg.timestamp).toLocaleTimeString('zh-CN', { 
                      hour: '2-digit', 
                      minute: '2-digit' 
                    })}
                  </span>
                </div>
                <div className="chat-message-content">
                  {msg.content ? (
                    <MessageContent content={msg.content} />
                  ) : (
                    isStreaming ? '正在输入...' : ''
                  )}
                </div>
              </div>
            )
          })
        )}
        {isLoading && conversations.length > 0 && (
          <div className="chat-loading">
            <span className="loading-dots">●</span>
            <span className="loading-dots">●</span>
            <span className="loading-dots">●</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form className="chat-input-form" onSubmit={handleSubmit}>
        <input
          type="text"
          className="chat-input"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="输入问题..."
          disabled={isLoading}
          maxLength={500}
        />
        <button 
          type="submit" 
          className="chat-send-btn"
          disabled={!inputValue.trim() || isLoading}
        >
          发送
        </button>
      </form>
    </div>
  )
}

export default ChatComponent
