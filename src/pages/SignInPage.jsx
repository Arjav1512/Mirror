import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getUser } from '../utils/api'

function SignInPage() {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    email: ''
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
    setError('')
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const user = await getUser(formData.email)

      if (user) {
        sessionStorage.setItem('mirror_user_id', user.id)
        sessionStorage.setItem('mirror_user_email', user.email)
        sessionStorage.setItem('mirror_user_name', user.name)
        setSuccess(true)
        setTimeout(() => {
          navigate('/')
        }, 2000)
      } else {
        setError('No account found with this email. Please sign up first.')
      }
    } catch (err) {
      setError(err.message || 'Failed to sign in. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  if (success) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 flex items-center justify-center px-4">
        <div className="bg-slate-800 rounded-2xl p-12 max-w-md w-full text-center border border-slate-700">
          <div className="w-16 h-16 bg-green-900/50 rounded-full flex items-center justify-center mx-auto mb-6 border border-green-700">
            <svg className="w-8 h-8 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h3 className="text-2xl font-bold mb-4 text-white">Welcome Back!</h3>
          <p className="text-slate-300">Signed in successfully. Redirecting...</p>
        </div>
      </div>
    )
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

      <div className="container mx-auto max-w-md px-4 py-16">
        <div className="bg-slate-800 rounded-2xl p-8 md:p-12 border border-slate-700">
          <div className="text-center mb-8">
            <h1 className="text-3xl md:text-4xl font-extrabold text-white mb-3">
              Sign In
            </h1>
            <p className="text-slate-300 text-base">
              Welcome back to your reflection journey
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="email" className="block text-sm font-semibold text-white mb-2">
                Email Address
              </label>
              <input
                type="email"
                id="email"
                name="email"
                required
                value={formData.email}
                onChange={handleChange}
                placeholder="your@email.com"
                className="w-full px-4 py-3 border border-slate-600 rounded-lg focus:border-violet-500 focus:ring-2 focus:ring-violet-900 transition-all bg-slate-900 text-white placeholder-slate-400"
              />
            </div>

            {error && (
              <div className="bg-red-900/50 border-l-4 border-red-500 p-4 rounded">
                <p className="text-red-200 text-sm">{error}</p>
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-violet-600 to-violet-500 hover:from-violet-500 hover:to-violet-400 text-white font-semibold py-4 px-6 rounded-lg transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-violet-900/40 hover:shadow-xl hover:shadow-violet-500/30"
            >
              {loading ? (
                <span className="flex items-center justify-center">
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Signing in...
                </span>
              ) : (
                'Sign In'
              )}
            </button>

            <div className="text-center pt-4">
              <p className="text-slate-400 text-sm">
                Don't have an account?{' '}
                <button
                  type="button"
                  onClick={() => navigate('/')}
                  className="text-violet-400 hover:text-violet-300 transition-colors font-medium"
                >
                  Sign up here
                </button>
              </p>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}

export default SignInPage
