import { useMemo } from 'react'

function EmotionalTimeline({ entries }) {
  const timelineData = useMemo(() => {
    if (!entries || entries.length === 0) return []

    return entries
      .slice()
      .reverse()
      .map((entry, index) => ({
        date: new Date(entry.timestamp).toLocaleDateString('en-US', {
          month: 'short',
          day: 'numeric'
        }),
        valence: entry.valence || 0,
        sentiment: entry.sentiment_score || 0,
        index
      }))
  }, [entries])

  const getEmotionColor = (valence) => {
    if (valence > 0.3) return 'bg-green-500'
    if (valence > 0) return 'bg-blue-500'
    if (valence > -0.3) return 'bg-yellow-500'
    return 'bg-red-500'
  }

  const getEmotionLabel = (valence) => {
    if (valence > 0.3) return 'Positive'
    if (valence > 0) return 'Slightly Positive'
    if (valence > -0.3) return 'Neutral/Mixed'
    return 'Negative'
  }

  if (timelineData.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="w-16 h-16 bg-slate-700 rounded-full flex items-center justify-center mx-auto mb-4">
          <span className="text-3xl">📊</span>
        </div>
        <p className="text-slate-400 mb-2">No timeline data yet</p>
        <p className="text-slate-500 text-sm">Create entries to see your emotional journey</p>
      </div>
    )
  }

  const maxHeight = 120
  const minValence = Math.min(...timelineData.map(d => d.valence))
  const maxValence = Math.max(...timelineData.map(d => d.valence))
  const range = maxValence - minValence || 1

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold text-white">Emotional Timeline</h3>
          <p className="text-sm text-slate-400">Track your emotional patterns over time</p>
        </div>
        <div className="flex items-center gap-4 text-xs">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-green-500 rounded"></div>
            <span className="text-slate-400">Positive</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-yellow-500 rounded"></div>
            <span className="text-slate-400">Neutral</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-red-500 rounded"></div>
            <span className="text-slate-400">Negative</span>
          </div>
        </div>
      </div>

      <div className="relative">
        <div className="absolute left-0 right-0 top-1/2 h-px bg-slate-700"></div>

        <div className="flex items-end justify-around gap-2 pb-4" style={{ minHeight: `${maxHeight + 60}px` }}>
          {timelineData.map((point, index) => {
            const normalizedHeight = ((point.valence - minValence) / range) * maxHeight
            const heightFromCenter = (point.valence / 1) * (maxHeight / 2)

            return (
              <div key={index} className="flex flex-col items-center gap-2 flex-1 max-w-[60px]">
                <div className="relative flex flex-col items-center justify-end" style={{ height: `${maxHeight}px` }}>
                  <div
                    className={`w-full rounded-t-lg transition-all ${getEmotionColor(point.valence)}`}
                    style={{
                      height: `${Math.max(Math.abs(heightFromCenter), 10)}px`,
                      marginTop: point.valence >= 0 ? 'auto' : '0',
                      marginBottom: point.valence < 0 ? 'auto' : '0'
                    }}
                    title={`${point.date}: ${getEmotionLabel(point.valence)} (${point.valence.toFixed(2)})`}
                  ></div>
                </div>
                <span className="text-xs text-slate-400 text-center">{point.date}</span>
              </div>
            )
          })}
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
        <div className="bg-slate-900 rounded-lg p-4 border border-slate-700">
          <p className="text-xs text-slate-400 mb-1">Average Mood</p>
          <p className="text-2xl font-bold text-violet-400">
            {(timelineData.reduce((sum, d) => sum + d.valence, 0) / timelineData.length).toFixed(2)}
          </p>
        </div>
        <div className="bg-slate-900 rounded-lg p-4 border border-slate-700">
          <p className="text-xs text-slate-400 mb-1">Positive Days</p>
          <p className="text-2xl font-bold text-green-400">
            {timelineData.filter(d => d.valence > 0.2).length}
          </p>
        </div>
        <div className="bg-slate-900 rounded-lg p-4 border border-slate-700">
          <p className="text-xs text-slate-400 mb-1">Neutral Days</p>
          <p className="text-2xl font-bold text-yellow-400">
            {timelineData.filter(d => d.valence >= -0.2 && d.valence <= 0.2).length}
          </p>
        </div>
        <div className="bg-slate-900 rounded-lg p-4 border border-slate-700">
          <p className="text-xs text-slate-400 mb-1">Challenging Days</p>
          <p className="text-2xl font-bold text-red-400">
            {timelineData.filter(d => d.valence < -0.2).length}
          </p>
        </div>
      </div>
    </div>
  )
}

export default EmotionalTimeline
