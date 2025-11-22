import React from 'react'
import axios from 'axios'

export default function SummaryCard({ analysis }) {
  if (!analysis) {
    return (<div className="bg-white shadow rounded-lg p-4"><h3 className="font-semibold">Summary</h3><p className="text-sm text-gray-500">No analysis yet — ask a query.</p></div>)
  }

  const download = async () => {
    try {
      // Determine areas to request: prefer analysis.localities, else infer from tableData
      let areas = []
      if (analysis.localities && Array.isArray(analysis.localities) && analysis.localities.length) {
        areas = analysis.localities
      } else if (analysis.tableData) {
        if (Array.isArray(analysis.tableData)) {
          areas = Array.from(new Set(analysis.tableData.map(r => r.area)))
        } else if (typeof analysis.tableData === 'object') {
          areas = Object.keys(analysis.tableData)
        }
      }

      const res = await axios.post('http://127.0.0.1:8000/api/download/', { areas }, { responseType: 'blob' })
      const blob = new Blob([res.data], { type: 'text/csv' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'sample_real_estate.csv'
      document.body.appendChild(a)
      a.click()
      a.remove()
      window.URL.revokeObjectURL(url)
    } catch (err) {
      console.error('Download failed', err)
      alert('Download failed')
    }
  }

  return (
    <div className="bg-white shadow rounded-lg p-4">
      <h3 className="font-semibold">Summary</h3>
      <p className="mt-2 text-sm text-gray-700">{analysis.summary}</p>
      <div className="mt-3 text-xs text-gray-500">Rows returned: {Array.isArray(analysis.tableData) ? analysis.tableData.length : (analysis.tableData ? Object.keys(analysis.tableData).reduce((sum,k)=> sum + analysis.tableData[k].length,0) : 0)}</div>
      <div className="mt-3">
        <button onClick={download} className="bg-blue-600 text-white px-3 py-1 rounded">Download Data</button>
      </div>
    </div>
  )
}
