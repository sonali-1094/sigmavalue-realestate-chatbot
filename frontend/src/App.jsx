import React, { useState } from 'react'
import ChatWindow from './components/ChatWindow'
import ChatInput from './components/ChatInput'
import SummaryCard from './components/SummaryCard'
import TrendChart from './components/TrendChart'
import DataTable from './components/DataTable'
import axios from 'axios'

export default function App() {
  const [loading, setLoading] = useState(false)
  const [messages, setMessages] = useState([{ id: 1, from: 'bot', text: 'Hello — ask me about a locality (e.g., "Analyze Wakad")' }])
  const [analysis, setAnalysis] = useState(null)

  const sendQuery = async (query) => {
    if (!query) return
    const userMsg = { id: Date.now(), from: 'user', text: query }
    setMessages(m => [...m, userMsg])
    setLoading(true)
    try {
      const res = await axios.post('http://127.0.0.1:8000/api/analyze/', { query })
      const botMsg = { id: Date.now()+1, from: 'bot', text: res.data.summary || 'No summary' }
      setMessages(m => [...m, botMsg])
      setAnalysis(res.data)
    } catch (e) {
      const botMsg = { id: Date.now()+1, from: 'bot', text: 'Error: ' + (e.message || 'unknown') }
      setMessages(m => [...m, botMsg])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen p-6 bg-gradient-to-b from-white to-slate-50">
      <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <div className="bg-white shadow rounded-lg p-4">
            <h1 className="text-2xl font-semibold mb-2">Sigmavalue — Real Estate Chatbot</h1>
            <p className="text-sm text-gray-500 mb-4">Ask about locality trends, price growth, and demand.</p>
            <ChatWindow messages={messages} />
            <ChatInput onSend={sendQuery} loading={loading} />
          </div>
        </div>
        <div className="space-y-4">
          <SummaryCard analysis={analysis} />
          <div className="bg-white shadow rounded-lg p-4">
            <h3 className="font-semibold mb-2">Trends</h3>
            <TrendChart analysis={analysis} />
          </div>
          <div className="bg-white shadow rounded-lg p-4">
            <h3 className="font-semibold mb-2">Filtered Data</h3>
            <DataTable analysis={analysis} />
          </div>
        </div>
      </div>
    </div>
  )
}
