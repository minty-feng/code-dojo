import React, { useState } from 'react'
import './MessageContent.css'

function MessageContent({ content }) {
  const [showThink, setShowThink] = useState(false)
  
  // 检测并分离 think 部分和实际内容
  const parseContent = (text) => {
    if (!text) return { thinkContent: '', actualContent: '', hasThink: false }
    
    // 匹配 <think>...</think> 或 <think>...</think> 标签
    const thinkPattern = /<(?:think|redacted_reasoning)[^>]*>([\s\S]*?)<\/(?:think|redacted_reasoning)>/i
    const match = text.match(thinkPattern)
    
    if (match) {
      const thinkContent = match[1].trim()
      const actualContent = text.replace(thinkPattern, '').trim()
      return { thinkContent, actualContent, hasThink: true }
    }
    
    // 如果没有标签，检查是否有 "-------" 分隔符（think 部分通常在这之前）
    const separatorPattern = /-{4,}/
    const separatorMatch = text.match(separatorPattern)
    
    if (separatorMatch) {
      const separatorIndex = separatorMatch.index
      const beforeSeparator = text.substring(0, separatorIndex).trim()
      const afterSeparator = text.substring(separatorIndex + separatorMatch[0].length).trim()
      
      // 如果分隔符前的内容看起来像 think（包含特定关键词或较短），则分离
      const thinkKeywords = ['think', 'reasoning', '分析', '思考', '用户使用了', '基于']
      const isThinkContent = thinkKeywords.some(keyword => 
        beforeSeparator.toLowerCase().includes(keyword.toLowerCase())
      ) || beforeSeparator.length < 200
      
      if (isThinkContent && afterSeparator.length > 0) {
        return { 
          thinkContent: beforeSeparator, 
          actualContent: afterSeparator, 
          hasThink: true 
        }
      }
    }
    
    return { thinkContent: '', actualContent: text, hasThink: false }
  }
  
  const { thinkContent, actualContent, hasThink } = parseContent(content)
  
  // 简单的 markdown 渲染（基础版本，不依赖外部库）
  const renderMarkdown = (text) => {
    if (!text) return ''
    
    // 先保存代码块，避免被其他规则处理
    const codeBlocks = []
    let html = text.replace(/```(\w+)?\n([\s\S]*?)```/g, (match, lang, code) => {
      const placeholder = `__CODE_BLOCK_${codeBlocks.length}__`
      codeBlocks.push({ placeholder, lang: lang || 'text', code: escapeHtml(code.trim()) })
      return placeholder
    })
    
    // 保存行内代码
    const inlineCodes = []
    html = html.replace(/`([^`\n]+)`/g, (match, code) => {
      const placeholder = `__INLINE_CODE_${inlineCodes.length}__`
      inlineCodes.push({ placeholder, code: escapeHtml(code) })
      return placeholder
    })
    
    // 按行处理
    const lines = html.split('\n')
    const result = []
    let currentParagraph = []
    let inList = false
    let listItems = []
    
    const flushParagraph = () => {
      if (currentParagraph.length > 0) {
        result.push(`<p>${currentParagraph.join(' ')}</p>`)
        currentParagraph = []
      }
    }
    
    const flushList = () => {
      if (listItems.length > 0) {
        result.push(`<ul>${listItems.join('')}</ul>`)
        listItems = []
        inList = false
      }
    }
    
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i]
      const trimmed = line.trim()
      
      // 代码块占位符
      if (trimmed.startsWith('__CODE_BLOCK_')) {
        flushParagraph()
        flushList()
        const blockIndex = parseInt(trimmed.match(/\d+/)[0])
        result.push(`<pre><code class="language-${codeBlocks[blockIndex].lang}">${codeBlocks[blockIndex].code}</code></pre>`)
        continue
      }
      
      // 标题
      if (trimmed.match(/^#### /)) {
        flushParagraph()
        flushList()
        result.push(`<h4>${trimmed.substring(5)}</h4>`)
        continue
      }
      if (trimmed.match(/^### /)) {
        flushParagraph()
        flushList()
        result.push(`<h3>${trimmed.substring(4)}</h3>`)
        continue
      }
      if (trimmed.match(/^## /)) {
        flushParagraph()
        flushList()
        result.push(`<h2>${trimmed.substring(3)}</h2>`)
        continue
      }
      if (trimmed.match(/^# /)) {
        flushParagraph()
        flushList()
        result.push(`<h1>${trimmed.substring(2)}</h1>`)
        continue
      }
      
      // 列表
      const unorderedMatch = trimmed.match(/^[\*\-\+] (.*)$/)
      const orderedMatch = trimmed.match(/^(\d+)\. (.*)$/)
      if (unorderedMatch || orderedMatch) {
        flushParagraph()
        if (!inList) {
          inList = true
        }
        const content = unorderedMatch ? unorderedMatch[1] : orderedMatch[2]
        listItems.push(`<li>${content}</li>`)
        continue
      }
      
      // 如果当前不是列表项，但之前有列表，先输出列表
      if (inList && trimmed !== '') {
        flushList()
      }
      
      // 引用
      if (trimmed.match(/^> /)) {
        flushParagraph()
        flushList()
        result.push(`<blockquote>${trimmed.substring(2)}</blockquote>`)
        continue
      }
      
      // 空行
      if (trimmed === '') {
        flushParagraph()
        continue
      }
      
      // 普通文本
      currentParagraph.push(trimmed)
    }
    
    // 处理剩余内容
    flushParagraph()
    flushList()
    
    html = result.join('\n')
    
    // 处理粗体和斜体（避免在代码中处理）
    html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    html = html.replace(/__([^_]+)__/g, '<strong>$1</strong>')
    html = html.replace(/(?<!\*)\*([^*\s][^*]*?[^*\s])\*(?!\*)/g, '<em>$1</em>')
    html = html.replace(/(?<!_)_([^_\s][^_]*?[^_\s])_(?!_)/g, '<em>$1</em>')
    
    // 处理链接
    html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>')
    
    // 处理图片
    html = html.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<img src="$2" alt="$1" />')
    
    // 恢复行内代码
    inlineCodes.forEach(({ placeholder, code }) => {
      html = html.replace(new RegExp(placeholder.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g'), `<code>${code}</code>`)
    })
    
    // 清理空段落
    html = html.replace(/<p><\/p>/g, '')
    html = html.replace(/<p>\s*<\/p>/g, '')
    
    return html || '<p></p>'
  }
  
  const escapeHtml = (text) => {
    const div = document.createElement('div')
    div.textContent = text
    return div.innerHTML
  }
  
  return (
    <div className="message-content">
      {hasThink && thinkContent && (
        <div className="think-section">
          <button 
            className="think-toggle"
            onClick={() => setShowThink(!showThink)}
            type="button"
          >
            <span className="think-icon">
              {showThink ? (
                <svg width="12" height="12" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M2 4L6 8L10 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              ) : (
                <svg width="12" height="12" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M4 2L8 6L4 10" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              )}
            </span>
            <span className="think-label">思考过程</span>
            {!showThink && <span className="think-preview">（点击展开）</span>}
          </button>
          {showThink && (
            <div className="think-content">
              <pre>{thinkContent}</pre>
            </div>
          )}
        </div>
      )}
      <div 
        className="message-actual-content"
        dangerouslySetInnerHTML={{ __html: renderMarkdown(actualContent) }}
      />
    </div>
  )
}

export default MessageContent
