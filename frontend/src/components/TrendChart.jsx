import React from 'react'
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer, Legend } from 'recharts'

export default function TrendChart({ analysis }) {
  if (!analysis || !analysis.chartData) return <div className="text-sm text-gray-500">No chart available</div>

  // Comparison mode: chartData is an object with keys for each locality
  if (analysis.type === 'comparison') {
    const chartData = analysis.chartData
    const locals = Object.keys(chartData)
    if (locals.length === 0) return <div className="text-sm text-gray-500">No chart available</div>

    // Build union of years
    const yearSet = new Set()
    locals.forEach(l => (chartData[l].year || []).forEach(y => yearSet.add(y)))
    const years = Array.from(yearSet).sort()

    // Build dataset where each locality contributes demand_<loc> and price_<loc>
    const data = years.map(y => {
      const row = { year: y }
      locals.forEach(l => {
        const idx = (chartData[l].year || []).indexOf(y)
        row[`demand_${l}`] = idx >= 0 ? chartData[l].demand[idx] : null
        row[`price_${l}`] = idx >= 0 ? chartData[l].price[idx] : null
      })
      return row
    })

    const colors = ['#10b981', '#2563eb', '#f59e0b', '#ef4444']

    return (
      <div style={{ width: '100%', height: 260 }}>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="year" />
            <YAxis />
            <Tooltip />
            <Legend />
            {locals.map((l, i) => (
              <Line key={`d-${l}`} type="monotone" dataKey={`demand_${l}`} name={`${l} demand`} stroke={colors[i % colors.length]} strokeWidth={2} dot={false} />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </div>
    )
  }

  // Price growth or single locality: expect chartData.year, chartData.price, chartData.demand
  if (!analysis.chartData.year) return <div className="text-sm text-gray-500">No chart available</div>
  const data = analysis.chartData.year.map((y, i) => ({ year: y, price: analysis.chartData.price[i], demand: analysis.chartData.demand ? analysis.chartData.demand[i] : null }))

  return (
    <div style={{ width: '100%', height: 220 }}>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="year" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="price" stroke="#2563eb" strokeWidth={2} />
          {analysis.chartData.demand && <Line type="monotone" dataKey="demand" stroke="#10b981" strokeWidth={2} />}
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
