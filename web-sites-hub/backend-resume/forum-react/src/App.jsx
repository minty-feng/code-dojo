import React, { useState, useEffect } from 'react'
import Navbar from './components/Navbar'
import PostsPage from './components/PostsPage'
import PostDetailPage from './components/PostDetailPage'
import ChatComponent from './components/ChatComponent'
import './App.css'

function App() {
  const [currentPage, setCurrentPage] = useState('forum') // 'forum' | 'post-detail'
  const [currentPostId, setCurrentPostId] = useState(null) // 当前选中的帖子ID，用于筛选对话
  const [posts, setPosts] = useState([])
  const [allConversations, setAllConversations] = useState([]) // 所有对话，类似群聊
  const [onDutyUsers] = useState([
    { id: 1, name: '张三', role: '前端工程师', avatar: '张', active: true },
    { id: 2, name: '李四', role: '后端工程师', avatar: '李', active: true },
    { id: 3, name: '王五', role: '全栈工程师', avatar: '王', active: false },
    { id: 4, name: '赵六', role: 'DevOps', avatar: '赵', active: true }
  ])

  // 加载数据
  useEffect(() => {
    const savedPosts = localStorage.getItem('forum_posts')
    const savedConversations = localStorage.getItem('forum_all_conversations')
    
    if (savedPosts) {
      setPosts(JSON.parse(savedPosts))
    } else {
      // 初始化示例数据
      const initialPosts = [
        {
          id: 1,
          title: '如何配置 AgentKit SDK？',
          author: '小明',
          createdAt: new Date(Date.now() - 3600000).toISOString(),
          replyCount: 5,
          viewCount: 23,
          isNew: false
        },
        {
          id: 2,
          title: '论坛系统使用指南',
          author: '小红',
          createdAt: new Date(Date.now() - 7200000).toISOString(),
          replyCount: 12,
          viewCount: 45,
          isNew: false
        }
      ]
      setPosts(initialPosts)
      localStorage.setItem('forum_posts', JSON.stringify(initialPosts))
    }
    
    if (savedConversations) {
      setAllConversations(JSON.parse(savedConversations))
    }

    // 保存用户ID
    if (!localStorage.getItem('forum_user_id')) {
      localStorage.setItem('forum_user_id', `user-${Date.now()}`)
    }
  }, [])

  // 保存帖子
  const savePosts = () => {
    localStorage.setItem('forum_posts', JSON.stringify(posts))
  }

  // 保存所有对话
  const saveConversations = () => {
    localStorage.setItem('forum_all_conversations', JSON.stringify(allConversations))
  }

  // 选择帖子（用于筛选对话）
  const handleSelectPost = (postId) => {
    if (currentPostId === postId) {
      // 如果点击的是当前选中的帖子，则取消选择
      setCurrentPostId(null)
      setCurrentPage('forum')
    } else {
      const post = posts.find(p => p.id === postId)
      if (!post) return

      // 更新浏览量
      const updatedPosts = posts.map(p => 
        p.id === postId ? { ...p, viewCount: p.viewCount + 1 } : p
      )
      setPosts(updatedPosts)
      localStorage.setItem('forum_posts', JSON.stringify(updatedPosts))

      setCurrentPostId(postId)
      setCurrentPage('post-detail')
    }
  }

  // 返回论坛主页
  const handleBackToForum = () => {
    setCurrentPage('forum')
    setCurrentPostId(null)
  }

  // 创建新帖子
  const handleNewPost = () => {
    const title = prompt('请输入帖子标题:')
    if (!title) return

    const author = prompt('请输入您的名字:', '匿名用户') || '匿名用户'
    const newPost = {
      id: Date.now(),
      title: title,
      author: author,
      createdAt: new Date().toISOString(),
      replyCount: 0,
      viewCount: 0,
      isNew: true
    }

    const updatedPosts = [newPost, ...posts]
    setPosts(updatedPosts)
    savePosts()

    // 自动选中新帖子
    setTimeout(() => {
      handleSelectPost(newPost.id)
    }, 100)
  }

  // 添加对话记录（群聊模式）
  const handleAddConversation = (conversation, postId = null) => {
    // 如果没有指定 postId，使用当前选中的帖子
    const targetPostId = postId || currentPostId
    
    // 添加 postId 到对话记录中
    const conversationWithPost = {
      ...conversation,
      postId: targetPostId,
      postTitle: targetPostId ? posts.find(p => p.id === targetPostId)?.title : null,
      id: Date.now() // 添加唯一ID
    }

    const updatedConversations = [...allConversations, conversationWithPost]
    setAllConversations(updatedConversations)
    saveConversations()

    // 更新帖子回复数
    if (conversation.type === 'user' && targetPostId) {
      const updatedPosts = posts.map(p => 
        p.id === targetPostId ? { ...p, replyCount: p.replyCount + 1 } : p
      )
      setPosts(updatedPosts)
      savePosts()
    }
  }

  // 获取显示的对话列表（如果选中了帖子，则筛选该帖子的对话）
  const getDisplayConversations = () => {
    if (currentPostId) {
      return allConversations.filter(conv => conv.postId === currentPostId)
    }
    return allConversations
  }

  // 获取在线值班同学
  const getActiveOnDutyUsers = () => {
    return onDutyUsers.filter(u => u.active)
  }

  return (
    <div className="app">
      <Navbar onNewPost={handleNewPost} />
      
      <div className="main-container">
        {currentPage === 'forum' && (
          <div className="forum-chat-layout">
            <div className="forum-posts-section">
              <PostsPage
                posts={posts}
                onDutyUsers={onDutyUsers}
                onOpenPost={handleSelectPost}
                selectedPostId={currentPostId}
              />
            </div>
            <div className="forum-chat-section">
              <ChatComponent
                conversations={getDisplayConversations()}
                onSendMessage={(message) => handleAddConversation(message, currentPostId)}
                onReceiveMessage={(message) => handleAddConversation(message, currentPostId)}
                inputs={currentPostId ? {
                  post_id: currentPostId.toString(),
                  post_title: posts.find(p => p.id === currentPostId)?.title || '',
                  mentioned_users: getActiveOnDutyUsers().map(u => u.name).join(',')
                } : {
                  mentioned_users: getActiveOnDutyUsers().map(u => u.name).join(',')
                }}
                onDutyUsers={getActiveOnDutyUsers()}
                currentPostId={currentPostId}
                currentPostTitle={currentPostId ? posts.find(p => p.id === currentPostId)?.title : null}
              />
            </div>
          </div>
        )}
        
        {currentPage === 'post-detail' && currentPostId && (
          <PostDetailPage
            post={posts.find(p => p.id === currentPostId)}
            conversations={getDisplayConversations()}
            onDutyUsers={getActiveOnDutyUsers()}
            onBack={handleBackToForum}
            onAddConversation={(message) => handleAddConversation(message, currentPostId)}
            allConversations={allConversations}
          />
        )}
      </div>
    </div>
  )
}

export default App
