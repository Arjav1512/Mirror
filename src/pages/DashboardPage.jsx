import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

function DashboardPage() {
  const navigate = useNavigate()
  const [user, setUser] = useState(null)
  const [journalEntry, setJournalEntry] = useState('')
  const [entries, setEntries] = useState([])
  const [submitting, setSubmitting] = useState(false)
  const [successMessage, setSuccessMessage] = useState('')

  useEffect(() => {
    const userId = sessionStorage.getItem('mirror_user_id')
    const userEmail = sessionStorage.getItem('mirror_user_email')
    const userName = sessionStorage.getItem('mirror_user_name')

    if (!userId) {
      navigate('/')
      return
    }

    setUser({ id: userId, email: userEmail, name: userName })

    const savedEntries = JSON.parse(localStorage.getItem(`mirror_entries_${userId}`) || '[]')
    setEntries(savedEntries)
  }, [navigate])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!journalEntry.trim()) return

    setSubmitting(true)

    const newEntry = {
      id: Date.now(),
      content: journalEntry,
      timestamp: new Date().toISOString(),
      userId: user.id
    }

    const updatedEntries = [newEntry, ...entries]
    setEntries(updatedEntries)
    localStorage.setItem(`mirror_entries_${user.id}`, JSON.stringify(updatedEntries))

    setJournalEntry('')
    setSuccessMessage('Entry saved successfully!')
    setSubmitting(false)

    setTimeout(() => setSuccessMessage(''), 3000)
  }

  const handleSignOut = () => {
    sessionStorage.clear()
    navigate('/')
  }

  const formatDate = (timestamp) => {
    return new Date(timestamp).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  if (!user) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 flex items-center justify-center">
        <div className="text-white text-xl">Loading...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950">
      <nav className="sticky top-0 z-50 bg-slate-900/95 backdrop-blur-sm border-b border-slate-700/50">
        <div className="container mx-auto px-4 md:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-2">
              <span className="text-3xl">🧠</span>
              <span className="text-xl font-bold text-white">Mirror</span>
            </div>
            <div className="flex items-center gap-4">
              <span className="text-slate-300 text-sm hidden md:block">
                Welcome, {user.name}
              </span>
              <button
                onClick={handleSignOut}
                className="text-slate-300 hover:text-violet-400 transition-colors font-medium text-sm"
              >
                Sign Out
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="container mx-auto max-w-6xl px-4 py-8 md:py-12">
        <div className="mb-8">
          <h1 className="text-3xl md:text-4xl font-bold text-white mb-2">Your Journal</h1>
          <p className="text-slate-300">Reflect on your thoughts and track your emotional journey</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-10 h-10 bg-violet-900/50 rounded-lg flex items-center justify-center">
                <span className="text-xl">📝</span>
              </div>
              <h3 className="text-lg font-semibold text-white">Total Entries</h3>
            </div>
            <p className="text-3xl font-bold text-violet-400">{entries.length}</p>
          </div>

          <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-10 h-10 bg-blue-900/50 rounded-lg flex items-center justify-center">
                <span className="text-xl">🔥</span>
              </div>
              <h3 className="text-lg font-semibold text-white">Streak</h3>
            </div>
            <p className="text-3xl font-bold text-blue-400">
              {entries.length > 0 ? '1' : '0'} day
            </p>
          </div>

          <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-10 h-10 bg-green-900/50 rounded-lg flex items-center justify-center">
                <span className="text-xl">✨</span>
              </div>
              <h3 className="text-lg font-semibold text-white">Insights</h3>
            </div>
            <p className="text-sm text-slate-300 mt-2">Keep writing to unlock patterns</p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-slate-800 rounded-2xl p-6 md:p-8 border border-slate-700">
            <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
              <span>✍️</span>
              New Entry
            </h2>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="entry" className="block text-sm font-semibold text-white mb-2">
                  How are you feeling today?
                </label>
                <textarea
                  id="entry"
                  rows={10}
                  value={journalEntry}
                  onChange={(e) => setJournalEntry(e.target.value)}
                  placeholder="Write your thoughts here... What's on your mind? How did your day go?"
                  className="w-full px-4 py-3 border border-slate-600 rounded-lg focus:border-violet-500 focus:ring-2 focus:ring-violet-900 transition-all bg-slate-900 text-white placeholder-slate-400 resize-none"
                  required
                />
                <p className="text-xs text-slate-400 mt-2">
                  {journalEntry.length} characters
                </p>
              </div>

              {successMessage && (
                <div className="bg-green-900/20 border border-green-700/50 rounded-lg p-4">
                  <p className="text-green-400 text-sm flex items-center gap-2">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
                    </svg>
                    {successMessage}
                  </p>
                </div>
              )}

              <button
                type="submit"
                disabled={submitting || !journalEntry.trim()}
                className="w-full bg-gradient-to-r from-violet-600 to-violet-500 hover:from-violet-500 hover:to-violet-400 text-white font-semibold py-4 px-6 rounded-lg transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-violet-900/40 hover:shadow-xl hover:shadow-violet-500/30"
              >
                {submitting ? 'Saving...' : 'Save Entry'}
              </button>
            </form>
          </div>

          <div className="bg-slate-800 rounded-2xl p-6 md:p-8 border border-slate-700">
            <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
              <span>📖</span>
              Recent Entries
            </h2>

            {entries.length === 0 ? (
              <div className="text-center py-12">
                <div className="w-16 h-16 bg-slate-700 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-3xl">📝</span>
                </div>
                <p className="text-slate-400 mb-2">No entries yet</p>
                <p className="text-slate-500 text-sm">Start your reflection journey by writing your first entry</p>
              </div>
            ) : (
              <div className="space-y-4 max-h-[600px] overflow-y-auto">
                {entries.map((entry) => (
                  <div
                    key={entry.id}
                    className="bg-slate-900 rounded-lg p-4 border border-slate-700 hover:border-violet-700/50 transition-colors"
                  >
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-xs text-slate-400">
                        {formatDate(entry.timestamp)}
                      </span>
                    </div>
                    <p className="text-slate-300 text-sm line-clamp-3">
                      {entry.content}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        <div className="mt-8 bg-violet-900/20 border border-violet-700/50 rounded-xl p-6">
          <div className="flex items-start gap-4">
            <div className="w-12 h-12 bg-violet-900/50 rounded-lg flex items-center justify-center flex-shrink-0">
              <span className="text-2xl">💡</span>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-white mb-2">Coming Soon: AI-Powered Insights</h3>
              <p className="text-slate-300 text-sm leading-relaxed">
                We're working on bringing sentiment analysis, bias detection, and personalized emotional insights to your web dashboard.
                For now, your entries are being saved securely in your browser.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default DashboardPage
