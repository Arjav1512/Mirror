import { useNavigate } from 'react-router-dom'

function PrivacyPage() {
  const navigate = useNavigate()

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
          <h1 className="text-4xl font-bold text-white mb-6">Privacy Policy</h1>
          <p className="text-slate-400 text-sm mb-8">Last updated: November 10, 2025</p>

          <div className="space-y-6 text-slate-300">
            <section>
              <h2 className="text-2xl font-semibold text-white mb-3">Your Privacy Matters</h2>
              <p className="leading-relaxed">
                At Mirror, we take your privacy seriously. This policy explains how we collect, use, and protect your personal information.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-white mb-3">Information We Collect</h2>
              <ul className="list-disc list-inside space-y-2 leading-relaxed">
                <li>Account information: email, name, and profile details</li>
                <li>Journal entries and emotional data you choose to record</li>
                <li>Usage data to improve our service</li>
              </ul>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-white mb-3">How We Use Your Data</h2>
              <ul className="list-disc list-inside space-y-2 leading-relaxed">
                <li>To provide personalized self-reflection insights</li>
                <li>To improve our AI analysis and recommendations</li>
                <li>To communicate important updates about your account</li>
              </ul>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-white mb-3">Data Security</h2>
              <p className="leading-relaxed">
                We use industry-standard encryption to protect your data. All journal entries are stored securely and are never shared with third parties without your explicit consent.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-white mb-3">Your Rights</h2>
              <p className="leading-relaxed">
                You have the right to access, modify, or delete your data at any time. Contact us at arjav.jain1512@icloud.com for any privacy concerns.
              </p>
            </section>
          </div>
        </div>
      </div>
    </div>
  )
}

export default PrivacyPage
