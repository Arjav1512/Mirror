import { useState } from 'react'
import { signupUser } from '../utils/api'

function SignupForm({ onSuccess, showSuccess }) {
  // Enhanced form data for comprehensive user profiling
  const [formData, setFormData] = useState({
    email: '',
    name: '',
    ageGroup: '',
    occupation: '',
    journalingExperience: '',
    primaryGoal: '',
    emotionalChallenges: '',
    preferredReflectionTime: ''
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

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
      sessionStorage.setItem('mirror_user_name', formData.name)
      const response = await signupUser(formData)
      if (response.success) {
        onSuccess(response)
      } else {
        setError(response.error || 'Something went wrong')
      }
    } catch (err) {
      setError(err.message || 'Failed to submit form. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  if (showSuccess) {
    return (
      <section id="signup-form" className="py-24 px-4 bg-slate-900">
        <div className="container mx-auto max-w-2xl">
          <div className="bg-slate-800 rounded-2xl card-shadow p-12 text-center border border-slate-700">
            <div className="w-16 h-16 bg-green-900/50 rounded-full flex items-center justify-center mx-auto mb-6 border border-green-700">
              <svg className="w-8 h-8 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <h3 className="text-2xl font-bold mb-4 text-white">Welcome to Mirror!</h3>
            <p className="text-slate-300 mb-6">Your profile has been created successfully!</p>
            <div className="bg-violet-900/20 border border-violet-700/50 rounded-lg p-6 mt-6">
              <p className="text-slate-300 mb-4">The full journaling experience with AI analysis is available when you run Mirror locally.</p>
              <p className="text-sm text-slate-400">This is a demo of the landing page and signup flow. The complete app includes sentiment analysis, bias detection, and emotional insights.</p>
            </div>
          </div>
        </div>
      </section>
    )
  }

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  return (
    <section id="signup-form" className="py-24 px-4 bg-slate-900">
      <div className="container mx-auto max-w-2xl">
        {/* Back button */}
        <button
          onClick={scrollToTop}
          className="mb-6 flex items-center gap-2 text-slate-300 hover:text-violet-400 transition-colors duration-200 group"
        >
          <svg className="w-5 h-5 transform group-hover:-translate-x-1 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          <span className="font-medium">Back to top</span>
        </button>
        
        <div className="bg-slate-800 rounded-2xl card-shadow p-8 md:p-12 border border-slate-700">
          <div className="text-center mb-8">
            <h2 className="text-3xl md:text-4xl font-extrabold text-white mb-3">
              Create Your Profile
            </h2>
            <p className="text-slate-300 text-base">
              Help us personalize your self-reflection journey
            </p>
            <p className="text-slate-400 text-sm mt-2">
              Takes 2-3 minutes • All information is kept private
            </p>
          </div>
          {/* Comprehensive user profiling form with informative questions */}
          <form onSubmit={handleSubmit} className="space-y-8">
            
            {/* Section 1: Personal Information */}
            <div className="space-y-6">
              <div className="flex items-center gap-3">
                <span className="text-2xl">👤</span>
                <h3 className="text-lg font-semibold text-white">Personal Information</h3>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Name */}
              <div>
                <label htmlFor="name" className="block text-sm font-semibold text-white mb-2">
                  Full Name <span className="text-red-400">*</span>
                </label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  required
                  value={formData.name}
                  onChange={handleChange}
                  placeholder="John Doe"
                  className="w-full px-4 py-3 border border-slate-600 rounded-lg focus:border-violet-500 focus:ring-2 focus:ring-violet-900 transition-all bg-slate-900 text-white placeholder-slate-400 hover:shadow-lg hover:shadow-violet-900/20"
                />
              </div>

              {/* Email */}
              <div>
                <label htmlFor="email" className="block text-sm font-semibold text-white mb-2">
                  Email Address <span className="text-red-400">*</span>
                </label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  required
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="your@email.com"
                  className="w-full px-4 py-3 border border-slate-600 rounded-lg focus:border-violet-500 focus:ring-2 focus:ring-violet-900 transition-all bg-slate-900 text-white placeholder-slate-400 hover:shadow-lg hover:shadow-violet-900/20"
                />
              </div>
            </div>
            </div>

            {/* Section 2: Demographics & Background */}
            <div className="space-y-6">
              <div className="flex items-center gap-3">
                <span className="text-2xl">📊</span>
                <h3 className="text-lg font-semibold text-white">Demographics & Background</h3>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Age Group */}
              <div>
                <label htmlFor="ageGroup" className="block text-sm font-semibold text-white mb-2">
                  Age Group <span className="text-red-400">*</span>
                </label>
                <select
                  id="ageGroup"
                  name="ageGroup"
                  required
                  value={formData.ageGroup}
                  onChange={handleChange}
                  className="w-full px-4 py-3 border border-slate-600 rounded-lg focus:border-violet-500 focus:ring-2 focus:ring-violet-900 transition-all bg-slate-900 text-white hover:shadow-lg hover:shadow-violet-900/20"
                >
                  <option value="">Select age group</option>
                  <option value="18-24">18-24 years</option>
                  <option value="25-34">25-34 years</option>
                  <option value="35-44">35-44 years</option>
                  <option value="45-54">45-54 years</option>
                  <option value="55-64">55-64 years</option>
                  <option value="65+">65+ years</option>
                </select>
              </div>

              {/* Occupation */}
              <div>
                <label htmlFor="occupation" className="block text-sm font-semibold text-white mb-2">
                  Occupation <span className="text-red-400">*</span>
                </label>
                <select
                  id="occupation"
                  name="occupation"
                  required
                  value={formData.occupation}
                  onChange={handleChange}
                  className="w-full px-4 py-3 border border-slate-600 rounded-lg focus:border-violet-500 focus:ring-2 focus:ring-violet-900 transition-all bg-slate-900 text-white hover:shadow-lg hover:shadow-violet-900/20"
                >
                  <option value="">Select occupation</option>
                  <option value="student">Student</option>
                  <option value="professional">Working Professional</option>
                  <option value="entrepreneur">Entrepreneur</option>
                  <option value="creative">Creative/Artist</option>
                  <option value="healthcare">Healthcare Worker</option>
                  <option value="educator">Educator/Teacher</option>
                  <option value="retired">Retired</option>
                  <option value="homemaker">Homemaker</option>
                  <option value="other">Other</option>
                </select>
              </div>
            </div>
            </div>

            {/* Section 3: Reflection Goals */}
            <div className="space-y-6">
              <div className="flex items-center gap-3">
                <span className="text-2xl">🎯</span>
                <h3 className="text-lg font-semibold text-white">Your Reflection Goals</h3>
              </div>
            
            {/* Journaling Experience */}
            <div>
              <label htmlFor="journalingExperience" className="block text-sm font-semibold text-white mb-2">
                Journaling Experience <span className="text-red-400">*</span>
              </label>
              <select
                id="journalingExperience"
                name="journalingExperience"
                required
                value={formData.journalingExperience}
                onChange={handleChange}
                className="w-full px-4 py-3 border border-slate-600 rounded-lg focus:border-violet-500 focus:ring-2 focus:ring-violet-900 transition-all bg-slate-900 text-white hover:shadow-lg hover:shadow-violet-900/20"
              >
                <option value="">How often do you journal?</option>
                <option value="never">Never journaled before</option>
                <option value="beginner">Tried a few times</option>
                <option value="occasional">Occasionally (few times a month)</option>
                <option value="regular">Regularly (few times a week)</option>
                <option value="daily">Daily practice</option>
              </select>
            </div>

            {/* Primary Goal */}
            <div>
              <label htmlFor="primaryGoal" className="block text-sm font-semibold text-white mb-2">
                What's your primary goal? <span className="text-red-400">*</span>
              </label>
              <select
                id="primaryGoal"
                name="primaryGoal"
                required
                value={formData.primaryGoal}
                onChange={handleChange}
                className="w-full px-4 py-3 border border-slate-600 rounded-lg focus:border-violet-500 focus:ring-2 focus:ring-violet-900 transition-all bg-slate-900 text-white hover:shadow-lg hover:shadow-violet-900/20"
              >
                <option value="">What brings you to Mirror?</option>
                <option value="emotional-awareness">Better emotional awareness</option>
                <option value="stress-management">Stress & anxiety management</option>
                <option value="personal-growth">Personal growth & development</option>
                <option value="mental-health">Mental health tracking</option>
                <option value="relationship-insights">Relationship insights</option>
                <option value="habit-tracking">Habit & behavior tracking</option>
                <option value="creative-expression">Creative self-expression</option>
                <option value="therapy-supplement">Supplement to therapy</option>
              </select>
            </div>

            {/* Emotional Challenges */}
            <div>
              <label htmlFor="emotionalChallenges" className="block text-sm font-semibold text-white mb-2">
                What emotional patterns are you hoping to understand?
              </label>
              <textarea
                id="emotionalChallenges"
                name="emotionalChallenges"
                rows={4}
                value={formData.emotionalChallenges}
                onChange={handleChange}
                placeholder="E.g., recurring anxiety, mood swings, procrastination patterns, relationship difficulties..."
                className="w-full px-4 py-3 border border-slate-600 rounded-lg focus:border-violet-500 focus:ring-2 focus:ring-violet-900 transition-all resize-none bg-slate-900 text-white placeholder-slate-400 hover:shadow-lg hover:shadow-violet-900/20"
              />
              <p className="text-xs text-slate-400 mt-1">Optional but helps us personalize your experience</p>
            </div>

            {/* Preferred Reflection Time */}
            <div>
              <label htmlFor="preferredReflectionTime" className="block text-sm font-semibold text-white mb-2">
                When do you prefer to reflect? <span className="text-red-400">*</span>
              </label>
              <select
                id="preferredReflectionTime"
                name="preferredReflectionTime"
                required
                value={formData.preferredReflectionTime}
                onChange={handleChange}
                className="w-full px-4 py-3 border border-slate-600 rounded-lg focus:border-violet-500 focus:ring-2 focus:ring-violet-900 transition-all bg-slate-900 text-white hover:shadow-lg hover:shadow-violet-900/20"
              >
                <option value="">Select your preferred time</option>
                <option value="morning">Morning (Start my day)</option>
                <option value="afternoon">Afternoon (Midday check-in)</option>
                <option value="evening">Evening (Wind down)</option>
                <option value="night">Night (Before bed)</option>
                <option value="flexible">Flexible/Varies</option>
              </select>
            </div>
            </div>

            {error && (
              <div className="bg-red-900/50 border-l-4 border-red-500 p-4 rounded">
                <p className="text-red-200 text-sm">{error}</p>
              </div>
            )}

            <div className="pt-2">
              {/* Enhanced gradient button as requested: #7c3aed to #8b5cf6 */}
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
                    Processing...
                  </span>
                ) : (
                  'Start Reflecting'
                )}
              </button>
              
              {/* Privacy note below form for transparency */}
              <p className="text-center text-xs text-slate-400 mt-6 leading-relaxed">
                🔒 Your privacy matters. We use minimal data collection and never share your personal information. All journal entries are encrypted and stored securely.
              </p>
            </div>
          </form>
        </div>
      </div>
    </section>
  )
}

export default SignupForm

