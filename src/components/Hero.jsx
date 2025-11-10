function Hero({ onScrollToForm }) {
  return (
    // Premium cinematic header with subtler gradient and increased vertical padding (py-16 = 4rem)
    <header className="bg-gradient-to-br from-slate-900/95 via-slate-900 to-violet-950/30 py-16 md:py-24 px-4 md:px-6 border-b border-slate-700/50 relative overflow-hidden">
      {/* Subtle ambient glow effect for premium feel */}
      <div className="absolute inset-0 bg-gradient-to-t from-violet-900/5 to-transparent pointer-events-none"></div>
      
      <div className="container mx-auto max-w-5xl text-center relative z-10">
        {/* Logo - Increased hierarchy with larger spacing */}
        <div className="flex items-center justify-center gap-4 mb-10 animate-fade-in">
          <span className="text-6xl md:text-7xl drop-shadow-2xl">🧠</span>
          <h1 className="text-6xl md:text-7xl lg:text-8xl font-extrabold text-white tracking-tight">
            Mirror
          </h1>
        </div>
        
        {/* Tagline - Reduced size to create hierarchy contrast with title */}
        <p className="text-base md:text-lg text-slate-300/90 mb-14 max-w-2xl mx-auto leading-relaxed font-light">
          An AI-powered self-awareness mirror that learns from your emotional patterns, not just your words.
        </p>
        
        {/* CTA Button - Added glowing border effect for premium feel */}
        <button
          onClick={onScrollToForm}
          className="group relative bg-gradient-to-r from-violet-600 to-violet-700 hover:from-violet-500 hover:to-violet-600 text-white font-semibold px-10 py-4 rounded-xl transition-all duration-300 shadow-2xl shadow-violet-900/40 hover:shadow-violet-500/50 hover:scale-105"
        >
          {/* Glowing border effect - subtle but premium */}
          <span className="absolute inset-0 rounded-xl bg-gradient-to-r from-violet-400 to-violet-500 opacity-0 group-hover:opacity-20 blur-sm transition-opacity duration-300"></span>
          <span className="absolute inset-0 rounded-xl ring-2 ring-violet-400/30 group-hover:ring-violet-300/50 transition-all duration-300"></span>
          <span className="relative">Get Started with Self Reflection</span>
        </button>
      </div>
    </header>
  )
}

export default Hero

