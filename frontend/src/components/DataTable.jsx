import React from 'react'
export default function DataTable({ analysis }) {
  if (!analysis || !analysis.tableData) return <div className="text-sm text-gray-500">No data to show</div>

  // tableData can be either an array (single/locality/growth) or an object (comparison)
  let rows = []
  if (Array.isArray(analysis.tableData)) {
    rows = analysis.tableData
  } else if (typeof analysis.tableData === 'object') {
    // merge all arrays from the object into one list
    Object.values(analysis.tableData).forEach(arr => {
      if (Array.isArray(arr)) rows = rows.concat(arr)
    })
  }

  if (rows.length === 0) return <div className="text-sm text-gray-500">No data to show</div>

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full text-left">
        <thead className="text-xs text-gray-500 uppercase">
          <tr><th className="px-2 py-1">Year</th><th className="px-2 py-1">Area</th><th className="px-2 py-1">Price</th><th className="px-2 py-1">Demand</th><th className="px-2 py-1">Size</th></tr>
        </thead>
        <tbody>
          {rows.map((r, i) => (
            <tr key={i} className="border-t"><td className="px-2 py-1">{r.year}</td><td className="px-2 py-1">{r.area}</td><td className="px-2 py-1">{r.price}</td><td className="px-2 py-1">{r.demand}</td><td className="px-2 py-1">{r.size}</td></tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
