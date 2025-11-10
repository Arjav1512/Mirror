import { useNavigate } from 'react-router-dom'

function TermsPage() {
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
          <h1 className="text-4xl font-bold text-white mb-6">Terms of Service</h1>
          <p className="text-slate-400 text-sm mb-8">Last updated: November 10, 2025</p>

          <div className="space-y-6 text-slate-300">
            <section>
              <h2 className="text-2xl font-semibold text-white mb-3">Acceptance of Terms</h2>
              <p className="leading-relaxed">
                By accessing and using Mirror, you accept and agree to be bound by these Terms of Service. If you do not agree, please do not use our service.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-white mb-3">Use of Service</h2>
              <ul className="list-disc list-inside space-y-2 leading-relaxed">
                <li>You must be at least 18 years old to use Mirror</li>
                <li>You are responsible for maintaining the confidentiality of your account</li>
                <li>You agree to use the service for personal, non-commercial purposes</li>
                <li>You will not misuse or attempt to harm the service</li>
              </ul>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-white mb-3">Content Ownership</h2>
              <p className="leading-relaxed">
                You retain all rights to the content you create on Mirror. We do not claim ownership of your journal entries or personal reflections.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-white mb-3">Service Limitations</h2>
              <p className="leading-relaxed">
                Mirror is a self-reflection tool and is not a substitute for professional mental health services. We do not provide medical advice or therapy.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-white mb-3">Termination</h2>
              <p className="leading-relaxed">
                We reserve the right to suspend or terminate accounts that violate these terms. You may delete your account at any time.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-white mb-3">Contact</h2>
              <p className="leading-relaxed">
                For questions about these terms, contact us at mirror2025@gmail.com
              </p>
            </section>
          </div>
        </div>
      </div>
    </div>
  )
}

export default TermsPage
