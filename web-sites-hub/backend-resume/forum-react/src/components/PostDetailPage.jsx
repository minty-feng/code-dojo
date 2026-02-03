import React, { useEffect, useRef } from 'react'
import ChatComponent from './ChatComponent'
import './PostDetailPage.css'

function PostDetailPage({ post, conversations, onDutyUsers, onBack, onAddConversation, allConversations = [] }) {
  const conversationsEndRef = useRef(null)

  useEffect(() => {
    // 滚动到底部
    if (conversationsEndRef.current) {
      conversationsEndRef.current.scrollIntoView({ behavior: 'smooth' })
    }
  }, [conversations])

  const formatTime = (isoString) => {
    const date = new Date(isoString)
    const now = new Date()
    const diff = now - date
    
    if (diff < 60000) return '刚刚'
    if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
    if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
    if (diff < 604800000) return `${Math.floor(diff / 86400000)}天前`
    
    return date.toLocaleDateString('zh-CN')
  }

  const handleExport = () => {
    if (conversations.length === 0) {
      alert('没有对话记录可导出')
      return
    }

    const data = {
      postTitle: post.title,
      postId: post.id,
      exportTime: new Date().toISOString(),
      conversations: conversations
    }

    const jsonStr = JSON.stringify(data, null, 2)
    const blob = new Blob([jsonStr], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `forum-post-${post.id}-${Date.now()}.json`
    a.click()
    URL.revokeObjectURL(url)
  }


  return (
    <div className="post-detail-page">
      <button className="back-btn" onClick={onBack}>
        ← 返回帖子列表
      </button>

      <div className="post-header">
        <h1 className="post-header-title">{post.title}</h1>
        <div className="post-header-meta">
          <div className="post-author">
            <div className="avatar">{post.author.charAt(0)}</div>
            <span>{post.author}</span>
          </div>
          <div className="post-stats">
            <div className="stat-item">💬 {post.replyCount} 回复</div>
            <div className="stat-item">👁️ {post.viewCount} 浏览</div>
            <div className="stat-item">🕒 {formatTime(post.createdAt)}</div>
          </div>
        </div>
      </div>

      <div className="post-detail-chat-section">
        <ChatComponent
          conversations={conversations}
          onSendMessage={(message) => onAddConversation(message)}
          onReceiveMessage={(message) => onAddConversation(message)}
          inputs={{
            post_id: post.id.toString(),
            post_title: post.title,
            mentioned_users: onDutyUsers.map(u => u.name).join(',')
          }}
          onDutyUsers={onDutyUsers}
          currentPostId={post.id}
          currentPostTitle={post.title}
        />
      </div>
    </div>
  )
}

export default PostDetailPage
