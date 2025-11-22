import React, { useState } from 'react'
export default function ChatInput({ onSend, loading }) {
  const [text, setText] = useState('')
  const submit = (e) => { e.preventDefault(); if (!text.trim()) return; onSend(text.trim()); setText('') }
  return (
    <form onSubmit={submit} className="mt-2 flex gap-2">
      <input value={text} onChange={e => setText(e.target.value)} placeholder='e.g., "Analyze Wakad"' className="flex-1 border rounded px-3 py-2 focus:outline-none" disabled={loading} />
      <button type="submit" className="bg-blue-600 text-white px-4 rounded" disabled={loading}>{loading ? '...' : 'Send'}</button>
    </form>
  )
}
