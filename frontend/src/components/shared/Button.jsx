import React from 'react'

const styles = {
  base: {
    display: 'inline-flex',
    alignItems: 'center',
    gap: '6px',
    padding: '8px 16px',
    borderRadius: '6px',
    fontSize: '14px',
    fontWeight: '500',
    transition: 'all 0.18s ease',
    cursor: 'pointer',
    border: 'none',
  }
}

export default function Button({ children, variant = 'primary', size = 'md', onClick, disabled, style }) {
  const variants = {
    primary: {
      background: '#f0e040',
      color: '#0f0f0f',
    },
    secondary: {
      background: '#242424',
      color: '#f0ede8',
      border: '1px solid #2e2e2e',
    },
    danger: {
      background: 'rgba(255,85,85,0.15)',
      color: '#ff5555',
      border: '1px solid rgba(255,85,85,0.3)',
    },
    ghost: {
      background: 'transparent',
      color: '#888',
      border: '1px solid #2e2e2e',
    }
  }

  const sizes = {
    sm: { padding: '5px 10px', fontSize: '12px' },
    md: { padding: '8px 16px', fontSize: '14px' },
    lg: { padding: '11px 22px', fontSize: '15px' },
  }

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      style={{
        ...styles.base,
        ...variants[variant],
        ...sizes[size],
        opacity: disabled ? 0.5 : 1,
        cursor: disabled ? 'not-allowed' : 'pointer',
        ...style
      }}
    >
      {children}
    </button>
  )
}