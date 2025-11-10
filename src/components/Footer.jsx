import { memo } from 'react'

function Footer() {
  return (
    // Enhanced responsive footer with better mobile spacing
    <footer className="bg-slate-950 text-white py-10 md:py-12 px-4 md:px-6 border-t border-slate-800">
      <div className="container mx-auto max-w-6xl">
        {/* Responsive link layout - stacks on mobile, horizontal on desktop */}
        <div className="flex flex-col sm:flex-row justify-center items-center gap-4 sm:gap-6 mb-6">
          <a href="#" className="text-slate-400 hover:text-violet-400 transition-colors duration-200 text-sm hover:underline">
            Privacy Policy
          </a>
          {/* Hide separator dots on mobile for cleaner look */}
          <span className="hidden sm:inline text-slate-700">•</span>
          <a href="#" className="text-slate-400 hover:text-violet-400 transition-colors duration-200 text-sm hover:underline">
            Terms of Service
          </a>
          <span className="hidden sm:inline text-slate-700">•</span>
          <a href="mailto:mirror2025@gmail.com" className="text-slate-400 hover:text-violet-400 transition-colors duration-200 text-sm hover:underline">
            Contact Us
          </a>
        </div>
        
        {/* Copyright text with better mobile sizing */}
        <p className="text-center text-slate-500 text-xs sm:text-sm leading-relaxed px-4">
          © 2025 Mirror — Built for self-reflection
        </p>
      </div>
    </footer>
  )
}

export default memo(Footer)

