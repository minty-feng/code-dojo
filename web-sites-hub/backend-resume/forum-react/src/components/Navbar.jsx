import React from 'react'
import './Navbar.css'

function Navbar({ onNewPost }) {
  return (
    <nav className="navbar">
      <div className="nav-content">
        <div className="logo">💬 技术问答论坛</div>
        <div className="nav-actions">
          <button className="btn-primary" onClick={onNewPost}>
            + 发布新帖
          </button>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
