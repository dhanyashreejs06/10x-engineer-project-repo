import React, { useState, useEffect, useCallback } from 'react'
import { promptsApi, collectionsApi } from '../../api/client'
import PromptCard from './PromptCard'
import PromptForm from './PromptForm'
import Modal from '../shared/Modal'
import Button from '../shared/Button'
import { LoadingScreen, SkeletonCard, EmptyState, ErrorMessage } from '../shared/Loading'

export default function PromptsPage() {
  const [prompts, setPrompts] = useState([])
  const [collections, setCollections] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [search, setSearch] = useState('')
  const [filterCollection, setFilterCollection] = useState('')
  const [filterTag, setFilterTag] = useState('')

  // Modal state
  const [showCreate, setShowCreate] = useState(false)
  const [editPrompt, setEditPrompt] = useState(null)
  const [deletePrompt, setDeletePrompt] = useState(null)
  const [formLoading, setFormLoading] = useState(false)
  const [formError, setFormError] = useState(null)

  const fetchData = useCallback(async () => {
    try {
      setError(null)
      setLoading(true)
      const [promptsRes, collectionsRes] = await Promise.all([
        promptsApi.list({ search, collection_id: filterCollection, tag: filterTag }),
        collectionsApi.list()
      ])
      setPrompts(promptsRes.prompts)
      setCollections(collectionsRes.collections)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }, [search, filterCollection, filterTag])

  useEffect(() => { fetchData() }, [fetchData])

  // Create
  const handleCreate = async (data) => {
    try {
      setFormLoading(true)
      setFormError(null)
      await promptsApi.create(data)
      setShowCreate(false)
      fetchData()
    } catch (e) {
      setFormError(e.message)
    } finally {
      setFormLoading(false)
    }
  }

  // Edit
  const handleEdit = async (data) => {
    try {
      setFormLoading(true)
      setFormError(null)
      await promptsApi.update(editPrompt.id, data)
      setEditPrompt(null)
      fetchData()
    } catch (e) {
      setFormError(e.message)
    } finally {
      setFormLoading(false)
    }
  }

  // Delete
  const handleDelete = async () => {
    try {
      await promptsApi.delete(deletePrompt.id)
      setDeletePrompt(null)
      fetchData()
    } catch (e) {
      setError(e.message)
    }
  }

  const getCollection = (id) => collections.find(c => c.id === id)

  const inputStyle = {
    background: '#1a1a1a',
    border: '1px solid #2e2e2e',
    borderRadius: '6px',
    padding: '8px 12px',
    color: '#f0ede8',
    fontSize: '14px',
    width: '100%'
  }

  return (
    <div>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '28px', flexWrap: 'wrap', gap: '12px' }}>
        <div>
          <h1 style={{ fontFamily: 'var(--font-display)', fontSize: '32px', fontWeight: '400', marginBottom: '4px' }}>
            Prompts
          </h1>
          <p style={{ color: '#888', fontSize: '14px' }}>
            {prompts.length} prompt{prompts.length !== 1 ? 's' : ''}
          </p>
        </div>
        <Button variant="primary" onClick={() => { setShowCreate(true); setFormError(null) }}>
          + New Prompt
        </Button>
      </div>

      {/* Filters */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr auto auto', gap: '10px', marginBottom: '24px' }}>
        <input
          placeholder="Search prompts..."
          value={search}
          onChange={e => setSearch(e.target.value)}
          style={inputStyle}
        />
        <select
          value={filterCollection}
          onChange={e => setFilterCollection(e.target.value)}
          style={{ ...inputStyle, width: 'auto', cursor: 'pointer' }}
        >
          <option value="">All collections</option>
          {collections.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
        </select>
        <input
          placeholder="Filter by tag..."
          value={filterTag}
          onChange={e => setFilterTag(e.target.value)}
          style={{ ...inputStyle, width: '140px' }}
        />
      </div>

      {/* Error */}
      {error && <div style={{ marginBottom: '20px' }}><ErrorMessage message={error} onRetry={fetchData} /></div>}

      {/* Content */}
      {loading ? (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '16px' }}>
          {[1,2,3,4,5,6].map(i => <SkeletonCard key={i} />)}
        </div>
      ) : prompts.length === 0 ? (
        <EmptyState
          icon="✦"
          title={search || filterTag ? 'No prompts match your search' : 'No prompts yet'}
          description={search || filterTag ? 'Try different search terms' : 'Create your first prompt to get started'}
          action={!search && !filterTag && <Button variant="primary" onClick={() => setShowCreate(true)}>+ New Prompt</Button>}
        />
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '16px' }}>
          {prompts.map(p => (
            <PromptCard
              key={p.id}
              prompt={p}
              collection={getCollection(p.collection_id)}
              onEdit={(p) => { setEditPrompt(p); setFormError(null) }}
              onDelete={setDeletePrompt}
            />
          ))}
        </div>
      )}

      {/* Create Modal */}
      <Modal isOpen={showCreate} onClose={() => setShowCreate(false)} title="New Prompt">
        <PromptForm
          collections={collections}
          onSubmit={handleCreate}
          onCancel={() => setShowCreate(false)}
          loading={formLoading}
          error={formError}
        />
      </Modal>

      {/* Edit Modal */}
      <Modal isOpen={!!editPrompt} onClose={() => setEditPrompt(null)} title="Edit Prompt">
        <PromptForm
          prompt={editPrompt}
          collections={collections}
          onSubmit={handleEdit}
          onCancel={() => setEditPrompt(null)}
          loading={formLoading}
          error={formError}
        />
      </Modal>

      {/* Delete Confirm Modal */}
      <Modal isOpen={!!deletePrompt} onClose={() => setDeletePrompt(null)} title="Delete Prompt" width="400px">
        <p style={{ color: '#888', marginBottom: '24px', lineHeight: '1.6' }}>
          Are you sure you want to delete <strong style={{ color: '#f0ede8' }}>"{deletePrompt?.title}"</strong>? This cannot be undone.
        </p>
        <div style={{ display: 'flex', gap: '10px', justifyContent: 'flex-end' }}>
          <Button variant="ghost" onClick={() => setDeletePrompt(null)}>Cancel</Button>
          <Button variant="danger" onClick={handleDelete}>Delete</Button>
        </div>
      </Modal>
    </div>
  )
}