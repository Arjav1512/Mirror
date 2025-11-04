import { memo } from 'react'

function HowItWorks() {
  const features = [
    {
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
        </svg>
      ),
      title: 'Emotional Timeline',
      description: 'Track your emotional journey over time with deep sentiment analysis. Visualize patterns, detect mood shifts, and understand your emotional volatility.'
    },
    {
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
        </svg>
      ),
      title: 'You in 7 Days',
      description: 'Every week, receive an AI-generated summary of your dominant emotions, recurring themes, and behavioral patterns with specific examples.'
    },
    {
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
        </svg>
      ),
      title: 'Bias Detection',
      description: 'Identify cognitive distortions like catastrophizing, black-and-white thinking, and emotional reasoning. Track your growth in self-awareness.'
    },
    {
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
        </svg>
      ),
      title: 'Pattern Recognition',
      description: 'Discover hidden connections between your thoughts, emotions, and behaviors across all your entries.'
    },
    {
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
        </svg>
      ),
      title: 'Privacy First',
      description: 'All processing happens locally. Your data stays yours—no external transmission except optional AI features.'
    }
  ]

  return (
    // Enhanced responsive padding and spacing for all screen sizes
    <section className="py-16 md:py-24 px-4 md:px-6 bg-slate-900">
      <div className="container mx-auto max-w-6xl">
        {/* Responsive heading with proper hierarchy */}
        <div className="text-center mb-12 md:mb-16">
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-white mb-4 px-4">
            How It Works
          </h2>
          <p className="text-slate-300 text-base md:text-lg max-w-3xl mx-auto px-4 leading-relaxed">
            Mirror uses advanced AI to analyze your journal entries and reveal insights you might miss
          </p>
        </div>
        
        {/* Responsive grid: 1 col mobile, 2 col tablet, 3 col desktop */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8">
          {features.map((feature, index) => (
            <div
              key={index}
              // Optimized hover effects - smoother and faster
              className="bg-slate-800 p-6 md:p-8 rounded-2xl card-shadow transition-all duration-200 border border-slate-700 hover:border-violet-500/80 hover:shadow-lg hover:shadow-violet-900/20"
            >
              <div className="w-12 h-12 md:w-14 md:h-14 bg-violet-900/50 rounded-full flex items-center justify-center text-violet-400 mb-4 md:mb-6 border border-violet-700 transition-transform duration-300 hover:scale-110">
                {feature.icon}
              </div>
              <h3 className="text-lg md:text-xl font-semibold text-white mb-2 md:mb-3">
                {feature.title}
              </h3>
              <p className="text-sm md:text-base text-slate-300 leading-relaxed">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

export default memo(HowItWorks)

