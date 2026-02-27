import React, { useState } from 'react'
import PromptsPage from './components/prompts/PromptsPage'
import CollectionsPage from './components/collections/CollectionsPage'

export default function App() {
  const [page, setPage] = useState('prompts')

  return (
    <div style={{ minHeight: '100vh', background: 'var(--bg)' }}>
      {/* Sidebar */}
      <nav style={{
        position: 'fixed', top: 0, left: 0, bottom: 0,
        width: '220px',
        background: '#111',
        borderRight: '1px solid #1e1e1e',
        display: 'flex', flexDirection: 'column',
        padding: '0',
        zIndex: 100
      }}>
        {/* Logo */}
        <div style={{ padding: '28px 24px 24px', borderBottom: '1px solid #1e1e1e' }}>
          <h1 style={{
            fontFamily: 'var(--font-display)',
            fontSize: '22px', fontWeight: '400',
            color: '#f0ede8',
            letterSpacing: '-0.02em'
          }}>
            Prompt<span style={{ color: '#f0e040' }}>Lab</span>
          </h1>
          <p style={{ fontSize: '11px', color: '#555', marginTop: '4px' }}>AI Prompt Manager</p>
        </div>

        {/* Nav Links */}
        <div style={{ padding: '16px 12px', flex: 1 }}>
          {[
            { id: 'prompts', label: 'Prompts', icon: '✦' },
            { id: 'collections', label: 'Collections', icon: '📁' }
          ].map(item => (
            <button
              key={item.id}
              onClick={() => setPage(item.id)}
              style={{
                width: '100%', textAlign: 'left',
                display: 'flex', alignItems: 'center', gap: '10px',
                padding: '10px 12px',
                borderRadius: '8px',
                background: page === item.id ? 'rgba(240,224,64,0.08)' : 'transparent',
                color: page === item.id ? '#f0e040' : '#888',
                border: page === item.id ? '1px solid rgba(240,224,64,0.15)' : '1px solid transparent',
                fontSize: '14px', fontWeight: '500',
                cursor: 'pointer',
                transition: 'all 0.18s ease',
                marginBottom: '4px'
              }}
            >
              <span style={{ fontSize: '12px' }}>{item.icon}</span>
              {item.label}
            </button>
          ))}
        </div>

        {/* Footer */}
        <div style={{ padding: '16px 24px', borderTop: '1px solid #1e1e1e' }}>
          <p style={{ fontSize: '11px', color: '#444' }}>Week 3 Project</p>
        </div>
      </nav>

      {/* Main Content */}
      <main style={{
        marginLeft: '220px',
        padding: '40px',
        minHeight: '100vh',
        maxWidth: '1200px'
      }}>
        {page === 'prompts' && <PromptsPage />}
        {page === 'collections' && <CollectionsPage />}
      </main>

      {/* Mobile responsive styles */}
      <style>{`
        @media (max-width: 768px) {
          nav {
            position: fixed !important;
            top: auto !important;
            bottom: 0 !important;
            left: 0 !important;
            right: 0 !important;
            width: 100% !important;
            height: 60px !important;
            flex-direction: row !important;
            border-right: none !important;
            border-top: 1px solid #1e1e1e !important;
            padding: 0 !important;
          }
          nav > div:first-child { display: none !important; }
          nav > div:last-child { display: none !important; }
          nav > div:nth-child(2) {
            display: flex !important;
            flex-direction: row !important;
            width: 100% !important;
            padding: 8px 16px !important;
            gap: 8px !important;
            align-items: center !important;
            justify-content: center !important;
          }
          nav > div:nth-child(2) button {
            flex: 1 !important;
            justify-content: center !important;
          }
          main {
            margin-left: 0 !important;
            padding: 20px 16px 80px !important;
          }
        }
      `}</style>
    </div>
  )
}