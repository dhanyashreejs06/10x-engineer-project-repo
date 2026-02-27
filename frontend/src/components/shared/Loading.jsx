import React from 'react'

export function Spinner({ size = 24, color = '#f0e040' }) {
  return (
    <div style={{
      width: size, height: size,
      border: `2px solid rgba(240,224,64,0.2)`,
      borderTop: `2px solid ${color}`,
      borderRadius: '50%',
      animation: 'spin 0.7s linear infinite',
      display: 'inline-block'
    }} />
  )
}

export function LoadingScreen() {
  return (
    <div style={{
      display: 'flex', flexDirection: 'column',
      alignItems: 'center', justifyContent: 'center',
      gap: '16px', padding: '80px 0'
    }}>
      <Spinner size={36} />
      <p style={{ color: '#888', fontSize: '14px' }}>Loading...</p>
    </div>
  )
}

export function SkeletonCard() {
  return (
    <div style={{
      background: '#1a1a1a',
      border: '1px solid #2e2e2e',
      borderRadius: '12px',
      padding: '20px',
      animation: 'pulse 1.5s ease infinite'
    }}>
      <div style={{ height: '16px', background: '#2e2e2e', borderRadius: '4px', marginBottom: '12px', width: '60%' }} />
      <div style={{ height: '12px', background: '#2e2e2e', borderRadius: '4px', marginBottom: '8px' }} />
      <div style={{ height: '12px', background: '#2e2e2e', borderRadius: '4px', width: '80%' }} />
    </div>
  )
}

export function EmptyState({ icon = '✦', title, description, action }) {
  return (
    <div style={{
      display: 'flex', flexDirection: 'column',
      alignItems: 'center', justifyContent: 'center',
      gap: '12px', padding: '80px 20px',
      textAlign: 'center'
    }}>
      <div style={{ fontSize: '40px', opacity: 0.3 }}>{icon}</div>
      <h3 style={{ color: '#888', fontWeight: '500', fontSize: '16px' }}>{title}</h3>
      {description && <p style={{ color: '#555', fontSize: '14px', maxWidth: '300px' }}>{description}</p>}
      {action && <div style={{ marginTop: '8px' }}>{action}</div>}
    </div>
  )
}

export function ErrorMessage({ message, onRetry }) {
  return (
    <div style={{
      background: 'rgba(255,85,85,0.08)',
      border: '1px solid rgba(255,85,85,0.2)',
      borderRadius: '8px',
      padding: '16px 20px',
      display: 'flex', alignItems: 'center',
      justifyContent: 'space-between', gap: '12px'
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        <span style={{ fontSize: '16px' }}>⚠</span>
        <span style={{ color: '#ff5555', fontSize: '14px' }}>{message}</span>
      </div>
      {onRetry && (
        <button
          onClick={onRetry}
          style={{
            background: 'none', border: '1px solid rgba(255,85,85,0.3)',
            color: '#ff5555', borderRadius: '6px',
            padding: '4px 10px', fontSize: '12px', cursor: 'pointer'
          }}
        >Retry</button>
      )}
    </div>
  )
}