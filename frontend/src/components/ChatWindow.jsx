import React, { useRef, useEffect } from 'react'
export default function ChatWindow({ messages = [] }) {
  const endRef = useRef(null)
  useEffect(() => { endRef.current?.scrollIntoView({ behavior: 'smooth' }) }, [messages])
  return (
    <div className="h-80 overflow-y-auto p-3 border rounded mb-3 bg-slate-50">
      {messages.map(m => (
        <div key={m.id} className={'mb-3 flex ' + (m.from === 'user' ? 'justify-end' : 'justify-start')}>
          <div className={(m.from === 'user' ? 'bg-blue-600 text-white' : 'bg-white text-slate-800') + ' max-w-[80%] p-3 rounded-lg shadow'}>
            <div className="text-sm">{m.text}</div>
          </div>
        </div>
      ))}
      <div ref={endRef} />
    </div>
  )
}
