import React, { useState } from 'react'
import Button from '../shared/Button'

export default function PromptCard({ prompt, collection, onEdit, onDelete }) {
  const [hovered, setHovered] = useState(false)
  const [copied, setCopied] = useState(false)

  const handleCopy = async (e) => {
    e.stopPropagation()
    await navigator.clipboard.writeText(prompt.content)
    setCopied(true)
    setTimeout(() => setCopied(false), 1500)
  }

  const formatDate = (iso) => {
    return new Date(iso).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
  }

  return (
    <div
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      style={{
        background: hovered ? '#1f1f1f' : '#1a1a1a',
        border: `1px solid ${hovered ? '#3a3a3a' : '#2e2e2e'}`,
        borderRadius: '12px',
        padding: '20px',
        transition: 'all 0.18s ease',
        display: 'flex',
        flexDirection: 'column',
        gap: '12px',
        animation: 'fadeIn 0.3s ease',
        cursor: 'default'
      }}
    >
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '12px' }}>
        <h3 style={{
          fontSize: '15px', fontWeight: '600',
          color: '#f0ede8', lineHeight: '1.4',
          flex: 1
        }}>
          {prompt.title}
        </h3>
        <div style={{ display: 'flex', gap: '6px', opacity: hovered ? 1 : 0, transition: 'opacity 0.18s ease', flexShrink: 0 }}>
          <Button size="sm" variant="ghost" onClick={handleCopy}>
            {copied ? '✓' : '⎘'}
          </Button>
          <Button size="sm" variant="ghost" onClick={() => onEdit(prompt)}>✎</Button>
          <Button size="sm" variant="danger" onClick={() => onDelete(prompt)}>✕</Button>
        </div>
      </div>

      {/* Description */}
      {prompt.description && (
        <p style={{ fontSize: '13px', color: '#888', lineHeight: '1.5' }}>
          {prompt.description}
        </p>
      )}

      {/* Content Preview */}
      <p style={{
        fontSize: '13px', color: '#555',
        lineHeight: '1.6',
        display: '-webkit-box',
        WebkitLineClamp: 3,
        WebkitBoxOrient: 'vertical',
        overflow: 'hidden',
        fontFamily: 'monospace',
        background: '#111',
        padding: '10px 12px',
        borderRadius: '6px',
        border: '1px solid #222'
      }}>
        {prompt.content}
      </p>

      {/* Tags */}
      {prompt.tags && prompt.tags.length > 0 && (
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
          {prompt.tags.map(tag => (
            <span key={tag} style={{
              background: 'rgba(240,224,64,0.08)',
              border: '1px solid rgba(240,224,64,0.2)',
              color: '#f0e040',
              padding: '2px 8px',
              borderRadius: '100px',
              fontSize: '11px',
              fontWeight: '500'
            }}>
              {tag}
            </span>
          ))}
        </div>
      )}

      {/* Footer */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '4px' }}>
        {collection ? (
          <span style={{
            fontSize: '11px', color: '#888',
            background: '#242424',
            padding: '3px 8px',
            borderRadius: '100px',
            border: '1px solid #2e2e2e'
          }}>
            📁 {collection.name}
          </span>
        ) : <span />}
        <span style={{ fontSize: '11px', color: '#555' }}>
          {formatDate(prompt.created_at)}
        </span>
      </div>
    </div>
  )
}