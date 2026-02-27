import React, { useEffect } from 'react'

export default function Modal({ isOpen, onClose, title, children, width = '520px' }) {
  useEffect(() => {
    const handler = (e) => { if (e.key === 'Escape') onClose() }
    if (isOpen) document.addEventListener('keydown', handler)
    return () => document.removeEventListener('keydown', handler)
  }, [isOpen, onClose])

  if (!isOpen) return null

  return (
    <div
      onClick={onClose}
      style={{
        position: 'fixed', inset: 0,
        background: 'rgba(0,0,0,0.75)',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        zIndex: 1000, padding: '16px',
        backdropFilter: 'blur(4px)',
        animation: 'fadeIn 0.2s ease'
      }}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        style={{
          background: '#1a1a1a',
          border: '1px solid #2e2e2e',
          borderRadius: '14px',
          width: '100%',
          maxWidth: width,
          maxHeight: '90vh',
          overflowY: 'auto',
          animation: 'fadeIn 0.25s ease'
        }}
      >
        {/* Header */}
        <div style={{
          display: 'flex', alignItems: 'center', justifyContent: 'space-between',
          padding: '20px 24px',
          borderBottom: '1px solid #2e2e2e'
        }}>
          <h2 style={{ fontFamily: 'var(--font-display)', fontSize: '20px', fontWeight: '400' }}>
            {title}
          </h2>
          <button
            onClick={onClose}
            style={{
              background: 'none', border: 'none', color: '#888',
              fontSize: '20px', cursor: 'pointer', lineHeight: 1,
              padding: '4px', borderRadius: '4px'
            }}
          >×</button>
        </div>

        {/* Content */}
        <div style={{ padding: '24px' }}>
          {children}
        </div>
      </div>
    </div>
  )
}