import { useMemo } from 'react'

function BiasInsights({ entries }) {
  const biasData = useMemo(() => {
    if (!entries || entries.length === 0) return { total: 0, byType: {}, recentBiases: [] }

    const allBiases = entries.flatMap(entry =>
      (entry.biases || []).map(bias => ({
        ...bias,
        entryDate: entry.timestamp
      }))
    )

    const byType = allBiases.reduce((acc, bias) => {
      acc[bias.bias_type] = (acc[bias.bias_type] || 0) + 1
      return acc
    }, {})

    const recentBiases = allBiases
      .sort((a, b) => new Date(b.entryDate) - new Date(a.entryDate))
      .slice(0, 5)

    return {
      total: allBiases.length,
      byType,
      recentBiases
    }
  }, [entries])

  const biasDescriptions = {
    'Catastrophizing': {
      icon: '🌪️',
      color: 'text-red-400',
      borderColor: 'border-red-700/50',
      bgColor: 'bg-red-900/20',
      tip: 'Ask yourself: What evidence supports this worst-case scenario? What are other possible outcomes?'
    },
    'Black-and-white Thinking': {
      icon: '⚖️',
      color: 'text-yellow-400',
      borderColor: 'border-yellow-700/50',
      bgColor: 'bg-yellow-900/20',
      tip: 'Consider: What middle ground exists? Can multiple things be partially true?'
    },
    'Emotional Reasoning': {
      icon: '💭',
      color: 'text-blue-400',
      borderColor: 'border-blue-700/50',
      bgColor: 'bg-blue-900/20',
      tip: 'Reflect: Am I confusing feelings with facts? What objective evidence exists?'
    },
    'Fortune Telling': {
      icon: '🔮',
      color: 'text-purple-400',
      borderColor: 'border-purple-700/50',
      bgColor: 'bg-purple-900/20',
      tip: 'Challenge: Can I really predict the future? What has happened in similar situations before?'
    },
    'Overgeneralization': {
      icon: '🔁',
      color: 'text-orange-400',
      borderColor: 'border-orange-700/50',
      bgColor: 'bg-orange-900/20',
      tip: 'Question: Is this pattern universal, or just one instance? What are the exceptions?'
    }
  }

  if (biasData.total === 0) {
    return (
      <div className="text-center py-12">
        <div className="w-16 h-16 bg-slate-700 rounded-full flex items-center justify-center mx-auto mb-4">
          <span className="text-3xl">🧠</span>
        </div>
        <p className="text-slate-400 mb-2">No biases detected yet</p>
        <p className="text-slate-500 text-sm">Keep journaling to unlock insights about your thinking patterns</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-white mb-2">Cognitive Bias Detection</h3>
        <p className="text-sm text-slate-400">Patterns in your thinking that may not reflect reality</p>
      </div>

      <div className="grid grid-cols-1 gap-3">
        {Object.entries(biasData.byType)
          .sort((a, b) => b[1] - a[1])
          .map(([biasType, count]) => {
            const info = biasDescriptions[biasType] || biasDescriptions['Catastrophizing']
            return (
              <div
                key={biasType}
                className={`${info.bgColor} border ${info.borderColor} rounded-lg p-4`}
              >
                <div className="flex items-start gap-3">
                  <span className="text-2xl">{info.icon}</span>
                  <div className="flex-1">
                    <div className="flex items-center justify-between mb-2">
                      <h4 className={`font-semibold ${info.color}`}>{biasType}</h4>
                      <span className="text-sm text-slate-400">
                        Detected {count} {count === 1 ? 'time' : 'times'}
                      </span>
                    </div>
                    <p className="text-sm text-slate-300">{info.tip}</p>
                  </div>
                </div>
              </div>
            )
          })}
      </div>

      <div className="bg-slate-900 rounded-lg p-6 border border-slate-700">
        <h4 className="font-semibold text-white mb-4 flex items-center gap-2">
          <span>📌</span>
          Recent Detections
        </h4>
        <div className="space-y-3">
          {biasData.recentBiases.map((bias, index) => {
            const info = biasDescriptions[bias.bias_type] || biasDescriptions['Catastrophizing']
            return (
              <div
                key={index}
                className="border-l-2 border-violet-500 pl-4 py-2"
              >
                <div className="flex items-center gap-2 mb-1">
                  <span>{info.icon}</span>
                  <span className={`font-medium text-sm ${info.color}`}>
                    {bias.bias_type}
                  </span>
                  <span className="text-xs text-slate-500">
                    {new Date(bias.entryDate).toLocaleDateString()}
                  </span>
                </div>
                <p className="text-sm text-slate-400">{bias.explanation}</p>
              </div>
            )
          })}
        </div>
      </div>

      <div className="bg-violet-900/20 border border-violet-700/50 rounded-lg p-4">
        <div className="flex items-start gap-3">
          <span className="text-xl">💡</span>
          <div>
            <h4 className="font-semibold text-white mb-1">Self-Awareness Growth</h4>
            <p className="text-sm text-slate-300">
              You've identified {biasData.total} cognitive biases across {entries.length} entries.
              Recognizing these patterns is the first step to changing them. Keep reflecting!
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default BiasInsights
