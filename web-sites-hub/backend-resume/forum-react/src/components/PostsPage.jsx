import React from 'react'
import './PostsPage.css'

function PostsPage({ posts, onDutyUsers, onOpenPost, selectedPostId = null }) {
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

  const totalReplies = posts.reduce((sum, post) => sum + post.replyCount, 0)
  const activeUsers = onDutyUsers.filter(u => u.active).length

  return (
    <div className="forum-layout">
      <div className="posts-container">
        <div className="posts-header">
          <h1>最新帖子</h1>
        </div>
        <div className="filter-tabs">
          <button className="tab active">全部</button>
          <button className="tab">最新</button>
          <button className="tab">热门</button>
          <button className="tab">我的</button>
        </div>
        <div className="posts-list">
          {posts.length === 0 ? (
            <div className="empty-posts">
              <p>还没有帖子，快来发布第一个吧！</p>
            </div>
          ) : (
            posts.map(post => (
              <div 
                key={post.id} 
                className={`post-item ${selectedPostId === post.id ? 'selected' : ''}`} 
                onClick={() => onOpenPost(post.id)}
              >
                <div className="post-title">
                  {post.title}
                  {post.isNew && <span className="post-badge new">新</span>}
                  {post.replyCount > 10 && <span className="post-badge hot">热门</span>}
                </div>
                <div className="post-meta">
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
            ))
          )}
        </div>
      </div>

      <div className="sidebar">
        <div className="sidebar-card">
          <h3>👥 值班同学</h3>
          <ul className="on-duty-list">
            {onDutyUsers.map(user => (
              <li key={user.id} className={`on-duty-item ${user.active ? 'active' : ''}`}>
                <div className="on-duty-avatar">{user.avatar}</div>
                <div className="on-duty-info">
                  <div className="on-duty-name">{user.name}</div>
                  <div className="on-duty-role">{user.role}</div>
                </div>
                {user.active && <div className="on-duty-status"></div>}
              </li>
            ))}
          </ul>
        </div>

        <div className="sidebar-card">
          <h3>📊 论坛统计</h3>
          <div className="stats-list">
            <div className="stat-row">
              <strong>{posts.length}</strong>
              <span>总帖子数</span>
            </div>
            <div className="stat-row">
              <strong>{totalReplies}</strong>
              <span>总回复数</span>
            </div>
            <div className="stat-row">
              <strong>{activeUsers}</strong>
              <span>在线用户</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default PostsPage
