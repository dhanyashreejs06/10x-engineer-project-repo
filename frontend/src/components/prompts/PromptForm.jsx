import React, { useState, useEffect } from 'react'
import Button from '../shared/Button'
import { ErrorMessage } from '../shared/Loading'

export default function PromptForm({ prompt, collections, onSubmit, onCancel, loading, error }) {
  const [form, setForm] = useState({
    title: '',
    content: '',
    description: '',
    collection_id: '',
    tags: ''
  })

  useEffect(() => {
    if (prompt) {
      setForm({
        title: prompt.title || '',
        content: prompt.content || '',
        description: prompt.description || '',
        collection_id: prompt.collection_id || '',
        tags: (prompt.tags || []).join(', ')
      })
    }
  }, [prompt])

  const handleChange = (e) => {
    setForm(f => ({ ...f, [e.target.name]: e.target.value }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    onSubmit({
      title: form.title,
      content: form.content,
      description: form.description || null,
      collection_id: form.collection_id || null,
      tags: form.tags ? form.tags.split(',').map(t => t.trim()).filter(Boolean) : []
    })
  }

  const inputStyle = {
    width: '100%',
    background: '#0f0f0f',
    border: '1px solid #2e2e2e',
    borderRadius: '6px',
    padding: '10px 12px',
    color: '#f0ede8',
    fontSize: '14px',
    transition: 'border-color 0.18s ease'
  }

  const labelStyle = {
    display: 'block',
    fontSize: '12px',
    fontWeight: '500',
    color: '#888',
    marginBottom: '6px',
    textTransform: 'uppercase',
    letterSpacing: '0.05em'
  }

  return (
    <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '18px' }}>
      {error && <ErrorMessage message={error} />}

      {/* Title */}
      <div>
        <label style={labelStyle}>Title *</label>
        <input
          name="title"
          value={form.title}
          onChange={handleChange}
          required
          placeholder="e.g. Code Review Assistant"
          style={inputStyle}
        />
      </div>

      {/* Content */}
      <div>
        <label style={labelStyle}>Prompt Content *</label>
        <textarea
          name="content"
          value={form.content}
          onChange={handleChange}
          required
          rows={6}
          placeholder="Write your prompt here... Use {{variable}} for template variables."
          style={{ ...inputStyle, resize: 'vertical', lineHeight: '1.6' }}
        />
      </div>

      {/* Description */}
      <div>
        <label style={labelStyle}>Description</label>
        <input
          name="description"
          value={form.description}
          onChange={handleChange}
          placeholder="Short description (optional)"
          style={inputStyle}
        />
      </div>

      {/* Collection */}
      <div>
        <label style={labelStyle}>Collection</label>
        <select
          name="collection_id"
          value={form.collection_id}
          onChange={handleChange}
          style={{ ...inputStyle, cursor: 'pointer' }}
        >
          <option value="">No collection</option>
          {collections.map(c => (
            <option key={c.id} value={c.id}>{c.name}</option>
          ))}
        </select>
      </div>

      {/* Tags */}
      <div>
        <label style={labelStyle}>Tags</label>
        <input
          name="tags"
          value={form.tags}
          onChange={handleChange}
          placeholder="python, review, ai (comma separated)"
          style={inputStyle}
        />
      </div>

      {/* Actions */}
      <div style={{ display: 'flex', gap: '10px', justifyContent: 'flex-end', paddingTop: '4px' }}>
        <Button variant="ghost" onClick={onCancel} type="button">Cancel</Button>
        <Button variant="primary" type="submit" disabled={loading}>
          {loading ? 'Saving...' : prompt ? 'Update Prompt' : 'Create Prompt'}
        </Button>
      </div>
    </form>
  )
}