import { useNavigate } from 'react-router-dom'
import { useState } from 'react'

function ContactPage() {
  const navigate = useNavigate()
  const [formSubmitted, setFormSubmitted] = useState(false)

  const handleSubmit = (e) => {
    e.preventDefault()
    setFormSubmitted(true)
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950">
      <nav className="sticky top-0 z-50 bg-slate-900/95 backdrop-blur-sm border-b border-slate-700/50">
        <div className="container mx-auto px-4 md:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <button
              onClick={() => navigate('/')}
              className="flex items-center gap-2 hover:opacity-80 transition-opacity"
            >
              <span className="text-3xl">🧠</span>
              <span className="text-xl font-bold text-white">Mirror</span>
            </button>
            <button
              onClick={() => navigate('/')}
              className="text-slate-300 hover:text-violet-400 transition-colors font-medium text-sm"
            >
              Back to Home
            </button>
          </div>
        </div>
      </nav>

      <div className="container mx-auto max-w-4xl px-4 py-16">
        <div className="bg-slate-800 rounded-2xl p-8 md:p-12 border border-slate-700">
          <h1 className="text-4xl font-bold text-white mb-6">Contact Us</h1>
          <p className="text-slate-300 mb-8">
            Have questions or feedback? We'd love to hear from you.
          </p>

          {formSubmitted ? (
            <div className="bg-green-900/20 border border-green-700/50 rounded-lg p-6 text-center">
              <div className="w-16 h-16 bg-green-900/50 rounded-full flex items-center justify-center mx-auto mb-4 border border-green-700">
                <svg className="w-8 h-8 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Message Sent!</h3>
              <p className="text-slate-300 mb-4">Thank you for reaching out. We'll get back to you soon.</p>
              <button
                onClick={() => setFormSubmitted(false)}
                className="text-violet-400 hover:text-violet-300 transition-colors text-sm"
              >
                Send another message
              </button>
            </div>
          ) : (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                <div className="bg-slate-900 rounded-lg p-6 border border-slate-700">
                  <h3 className="text-lg font-semibold text-white mb-2">Email</h3>
                  <a href="mailto:arjav.jain1512@icloud.com" className="text-violet-400 hover:text-violet-300 transition-colors">
                    arjav.jain1512@icloud.com
                  </a>
                </div>
                <div className="bg-slate-900 rounded-lg p-6 border border-slate-700">
                  <h3 className="text-lg font-semibold text-white mb-2">Response Time</h3>
                  <p className="text-slate-300">Within 24-48 hours</p>
                </div>
              </div>

              <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <label htmlFor="name" className="block text-sm font-semibold text-white mb-2">
                    Name
                  </label>
                  <input
                    type="text"
                    id="name"
                    required
                    className="w-full px-4 py-3 border border-slate-600 rounded-lg focus:border-violet-500 focus:ring-2 focus:ring-violet-900 transition-all bg-slate-900 text-white placeholder-slate-400"
                    placeholder="Your name"
                  />
                </div>

                <div>
                  <label htmlFor="email" className="block text-sm font-semibold text-white mb-2">
                    Email
                  </label>
                  <input
                    type="email"
                    id="email"
                    required
                    className="w-full px-4 py-3 border border-slate-600 rounded-lg focus:border-violet-500 focus:ring-2 focus:ring-violet-900 transition-all bg-slate-900 text-white placeholder-slate-400"
                    placeholder="your@email.com"
                  />
                </div>

                <div>
                  <label htmlFor="message" className="block text-sm font-semibold text-white mb-2">
                    Message
                  </label>
                  <textarea
                    id="message"
                    rows={6}
                    required
                    className="w-full px-4 py-3 border border-slate-600 rounded-lg focus:border-violet-500 focus:ring-2 focus:ring-violet-900 transition-all bg-slate-900 text-white placeholder-slate-400 resize-none"
                    placeholder="How can we help you?"
                  />
                </div>

                <button
                  type="submit"
                  className="w-full bg-gradient-to-r from-violet-600 to-violet-500 hover:from-violet-500 hover:to-violet-400 text-white font-semibold py-4 px-6 rounded-lg transition-all duration-300 shadow-lg shadow-violet-900/40 hover:shadow-xl hover:shadow-violet-500/30"
                >
                  Send Message
                </button>
              </form>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default ContactPage
