import { useState, useEffect, lazy, Suspense } from 'react'
import { useNavigate } from 'react-router-dom'
import HowItWorks from '../components/HowItWorks'
import SignupForm from '../components/SignupForm'
import Footer from '../components/Footer'

function LandingPage() {
  const navigate = useNavigate()
  const [showSuccess, setShowSuccess] = useState(false)
  const [isVisible, setIsVisible] = useState({})

  const handleSignupSuccess = (response) => {
    setShowSuccess(true)

    // Store user ID in session storage for future features
    if (response.data?.user_id) {
      sessionStorage.setItem('mirror_user_id', response.data.user_id)
    }
  }

  // Intersection Observer for fade-in animations on scroll
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setIsVisible((prev) => ({ ...prev, [entry.target.id]: true }))
          }
        })
      },
      { threshold: 0.1 }
    )

    document.querySelectorAll('[data-animate]').forEach((el) => {
      observer.observe(el)
    })

    return () => observer.disconnect()
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950">
      {/* Sticky Navigation Bar */}
      <nav className="sticky top-0 z-50 bg-slate-900/95 backdrop-blur-sm border-b border-slate-700/50">
        <div className="container mx-auto px-4 md:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <button 
              onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
              className="flex items-center gap-2 hover:opacity-80 transition-opacity"
            >
              <span className="text-3xl">🧠</span>
              <span className="text-xl font-bold text-white">Mirror</span>
            </button>
            
            {/* Nav Links */}
            <div className="flex items-center gap-4">
              <button
                onClick={() => document.getElementById('how-it-works')?.scrollIntoView({ behavior: 'smooth' })}
                className="text-slate-300 hover:text-violet-400 transition-colors font-medium text-sm"
              >
                How It Works
              </button>
              <button
                onClick={() => navigate('/signin')}
                className="text-slate-300 hover:text-violet-400 transition-colors font-medium text-sm"
              >
                Sign In
              </button>
              <button
                onClick={() => document.getElementById('signup-form')?.scrollIntoView({ behavior: 'smooth' })}
                className="bg-violet-600 hover:bg-violet-500 text-white px-4 py-2 rounded-lg transition-colors font-medium text-sm"
              >
                Get Started
              </button>
            </div>
          </div>
        </div>
      </nav>
      
      {/* Two-Column Hero Section - Premium Layout */}
      <header className="bg-gradient-to-br from-slate-900/95 via-slate-900 to-violet-950/30 py-16 md:py-24 px-4 md:px-6 lg:px-8 relative overflow-hidden">
        {/* Ambient background glow */}
        <div className="absolute inset-0 bg-gradient-to-t from-violet-900/5 to-transparent pointer-events-none"></div>
        
        <div className="container mx-auto max-w-7xl relative z-10">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-16 items-center">
            
            {/* LEFT COLUMN: Headline, Subtitle, CTA */}
            <div className="text-center lg:text-left space-y-8 animate-fade-in">
              {/* Logo + Brand */}
              <div className="flex items-center justify-center lg:justify-start gap-4">
                <span className="text-6xl md:text-7xl drop-shadow-2xl">🧠</span>
                <h1 className="text-6xl md:text-7xl lg:text-8xl font-extrabold text-white tracking-tight">
                  Mirror
                </h1>
              </div>

              {/* Subtitle with clear hierarchy */}
              <p className="text-lg md:text-xl text-slate-300/90 leading-relaxed font-light max-w-xl mx-auto lg:mx-0">
                An AI-powered self-awareness mirror that learns from your emotional patterns, not just your words.
              </p>

              {/* Enhanced CTA with glowing effect */}
              <button
                onClick={() => {
                  document.getElementById('signup-form')?.scrollIntoView({ behavior: 'smooth' })
                }}
                className="group relative bg-gradient-to-r from-violet-600 to-violet-700 hover:from-violet-500 hover:to-violet-600 text-white font-semibold px-10 py-4 rounded-xl transition-all duration-300 shadow-2xl shadow-violet-900/40 hover:shadow-violet-500/50 hover:scale-105"
              >
                {/* Glowing border effect */}
                <span className="absolute inset-0 rounded-xl bg-gradient-to-r from-violet-400 to-violet-500 opacity-0 group-hover:opacity-20 blur-sm transition-opacity duration-300"></span>
                <span className="absolute inset-0 rounded-xl ring-2 ring-violet-400/30 group-hover:ring-violet-300/50 transition-all duration-300"></span>
                <span className="relative">Get Started with Self Reflection</span>
              </button>
            </div>

            {/* RIGHT COLUMN: Optimized Screenshot Mockup */}
            <div className="relative animate-fade-in-delay hidden lg:block">
              {/* Simplified mockup container for better performance */}
              <div className="relative rounded-2xl overflow-hidden shadow-xl shadow-violet-900/20 border border-slate-700/50 bg-slate-800">
                {/* Streamlined placeholder - much faster rendering */}
                <div className="aspect-[4/3] rounded-xl bg-gradient-to-br from-slate-700 to-slate-800 flex items-center justify-center relative">
                  <div className="text-center p-8 space-y-3">
                    <div className="w-16 h-16 mx-auto bg-violet-600/30 rounded-full flex items-center justify-center border border-violet-500/40">
                      <span className="text-3xl">📊</span>
                    </div>
                    <p className="text-slate-300 font-semibold text-sm">Your Dashboard Awaits</p>
                    <p className="text-xs text-slate-400">Track emotions • Detect patterns • Grow</p>
                  </div>
                  {/* Single optimized gradient overlay */}
                  <div className="absolute inset-0 bg-gradient-to-t from-violet-900/10 to-transparent pointer-events-none"></div>
                </div>
              </div>
            </div>

          </div>
        </div>
      </header>

      {/* Optimized sections - load instantly, animate on scroll for better perceived performance */}
      <div id="how-it-works" data-animate className={`transition-all duration-700 ${isVisible['how-it-works'] ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
        <HowItWorks />
      </div>
      
      <div id="signup-section" data-animate className={`transition-all duration-700 ${isVisible['signup-section'] ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
        <SignupForm onSuccess={handleSignupSuccess} showSuccess={showSuccess} />
      </div>
      
      <Footer />
    </div>
  )
}

export default LandingPage

