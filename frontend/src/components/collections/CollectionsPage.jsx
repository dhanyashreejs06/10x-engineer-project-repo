import React, { useState, useEffect } from 'react'
import { collectionsApi, promptsApi } from '../../api/client'
import Modal from '../shared/Modal'
import Button from '../shared/Button'
import { LoadingScreen, EmptyState, ErrorMessage } from '../shared/Loading'

function CollectionCard({ collection, promptCount, onDelete, onClick, selected }) {
  const [hovered, setHovered] = useState(false)

  return (
    <div
      onClick={onClick}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      style={{
        background: selected ? '#1f1f1f' : hovered ? '#1c1c1c' : '#1a1a1a',
        border: `1px solid ${selected ? '#f0e040' : hovered ? '#3a3a3a' : '#2e2e2e'}`,
        borderRadius: '12px',
        padding: '20px',
        cursor: 'pointer',
        transition: 'all 0.18s ease',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        gap: '12px',
        animation: 'fadeIn 0.3s ease'
      }}
    >
      <div style={{ flex: 1 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '6px' }}>
          <span style={{ fontSize: '18px' }}>📁</span>
          <h3 style={{ fontSize: '15px', fontWeight: '600', color: '#f0ede8' }}>{collection.name}</h3>
        </div>
        {collection.description && (
          <p style={{ fontSize: '13px', color: '#888', lineHeight: '1.5' }}>{collection.description}</p>
        )}
        <p style={{ fontSize: '12px', color: '#555', marginTop: '8px' }}>
          {promptCount} prompt{promptCount !== 1 ? 's' : ''}
        </p>
      </div>

      <div style={{ opacity: hovered || selected ? 1 : 0, transition: 'opacity 0.18s ease' }}>
        <Button size="sm" variant="danger" onClick={(e) => { e.stopPropagation(); onDelete(collection) }}>
          ✕
        </Button>
      </div>
    </div>
  )
}

export default function CollectionsPage() {
  const [collections, setCollections] = useState([])
  const [prompts, setPrompts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [selected, setSelected] = useState(null)
  const [showCreate, setShowCreate] = useState(false)
  const [deleteTarget, setDeleteTarget] = useState(null)
  const [formLoading, setFormLoading] = useState(false)
  const [form, setForm] = useState({ name: '', description: '' })
  const [formError, setFormError] = useState(null)

  const fetchData = async () => {
    try {
      setError(null)
      setLoading(true)
      const [colRes, promptRes] = await Promise.all([
        collectionsApi.list(),
        promptsApi.list()
      ])
      setCollections(colRes.collections)
      setPrompts(promptRes.prompts)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { fetchData() }, [])

  const handleCreate = async (e) => {
    e.preventDefault()
    try {
      setFormLoading(true)
      setFormError(null)
      await collectionsApi.create(form)
      setShowCreate(false)
      setForm({ name: '', description: '' })
      fetchData()
    } catch (e) {
      setFormError(e.message)
    } finally {
      setFormLoading(false)
    }
  }

  const handleDelete = async () => {
    try {
      await collectionsApi.delete(deleteTarget.id)
      if (selected?.id === deleteTarget.id) setSelected(null)
      setDeleteTarget(null)
      fetchData()
    } catch (e) {
      setError(e.message)
    }
  }

  const getPromptCount = (colId) => prompts.filter(p => p.collection_id === colId).length
  const selectedPrompts = selected ? prompts.filter(p => p.collection_id === selected.id) : []

  const inputStyle = {
    width: '100%',
    background: '#0f0f0f',
    border: '1px solid #2e2e2e',
    borderRadius: '6px',
    padding: '10px 12px',
    color: '#f0ede8',
    fontSize: '14px'
  }

  return (
    <div>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '28px', flexWrap: 'wrap', gap: '12px' }}>
        <div>
          <h1 style={{ fontFamily: 'var(--font-display)', fontSize: '32px', fontWeight: '400', marginBottom: '4px' }}>
            Collections
          </h1>
          <p style={{ color: '#888', fontSize: '14px' }}>{collections.length} collection{collections.length !== 1 ? 's' : ''}</p>
        </div>
        <Button variant="primary" onClick={() => { setShowCreate(true); setFormError(null) }}>
          + New Collection
        </Button>
      </div>

      {error && <div style={{ marginBottom: '20px' }}><ErrorMessage message={error} onRetry={fetchData} /></div>}

      {loading ? <LoadingScreen /> : (
        <div style={{ display: 'grid', gridTemplateColumns: selected ? '1fr 1fr' : '1fr', gap: '16px' }}>
          {/* Collections List */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {collections.length === 0 ? (
              <EmptyState
                icon="📁"
                title="No collections yet"
                description="Group your prompts into collections for better organization"
                action={<Button variant="primary" onClick={() => setShowCreate(true)}>+ New Collection</Button>}
              />
            ) : collections.map(c => (
              <CollectionCard
                key={c.id}
                collection={c}
                promptCount={getPromptCount(c.id)}
                onDelete={setDeleteTarget}
                onClick={() => setSelected(selected?.id === c.id ? null : c)}
                selected={selected?.id === c.id}
              />
            ))}
          </div>

          {/* Selected Collection Prompts */}
          {selected && (
            <div style={{ animation: 'fadeIn 0.2s ease' }}>
              <h2 style={{ fontFamily: 'var(--font-display)', fontSize: '20px', fontWeight: '400', marginBottom: '16px', color: '#888' }}>
                {selected.name}
              </h2>
              {selectedPrompts.length === 0 ? (
                <EmptyState icon="✦" title="No prompts in this collection" description="Create a prompt and assign it to this collection" />
              ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                  {selectedPrompts.map(p => (
                    <div key={p.id} style={{
                      background: '#1a1a1a', border: '1px solid #2e2e2e',
                      borderRadius: '8px', padding: '14px 16px'
                    }}>
                      <p style={{ fontSize: '14px', fontWeight: '500', marginBottom: '4px' }}>{p.title}</p>
                      {p.description && <p style={{ fontSize: '12px', color: '#888' }}>{p.description}</p>}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* Create Modal */}
      <Modal isOpen={showCreate} onClose={() => setShowCreate(false)} title="New Collection" width="440px">
        <form onSubmit={handleCreate} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {formError && <ErrorMessage message={formError} />}
          <div>
            <label style={{ display: 'block', fontSize: '12px', color: '#888', marginBottom: '6px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Name *
            </label>
            <input
              required value={form.name}
              onChange={e => setForm(f => ({ ...f, name: e.target.value }))}
              placeholder="e.g. Development, Marketing..."
              style={inputStyle}
            />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '12px', color: '#888', marginBottom: '6px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Description
            </label>
            <input
              value={form.description}
              onChange={e => setForm(f => ({ ...f, description: e.target.value }))}
              placeholder="Optional description"
              style={inputStyle}
            />
          </div>
          <div style={{ display: 'flex', gap: '10px', justifyContent: 'flex-end' }}>
            <Button variant="ghost" type="button" onClick={() => setShowCreate(false)}>Cancel</Button>
            <Button variant="primary" type="submit" disabled={formLoading}>
              {formLoading ? 'Creating...' : 'Create Collection'}
            </Button>
          </div>
        </form>
      </Modal>

      {/* Delete Modal */}
      <Modal isOpen={!!deleteTarget} onClose={() => setDeleteTarget(null)} title="Delete Collection" width="400px">
        <p style={{ color: '#888', marginBottom: '8px', lineHeight: '1.6' }}>
          Are you sure you want to delete <strong style={{ color: '#f0ede8' }}>"{deleteTarget?.name}"</strong>?
        </p>
        <p style={{ color: '#ff5555', fontSize: '13px', marginBottom: '24px' }}>
          ⚠ All prompts in this collection will also be deleted.
        </p>
        <div style={{ display: 'flex', gap: '10px', justifyContent: 'flex-end' }}>
          <Button variant="ghost" onClick={() => setDeleteTarget(null)}>Cancel</Button>
          <Button variant="danger" onClick={handleDelete}>Delete Collection</Button>
        </div>
      </Modal>
    </div>
  )
}