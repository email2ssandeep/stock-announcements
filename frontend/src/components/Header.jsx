export default function Header() {
  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-6 h-14 flex items-center justify-between gap-4">
        {/* Logo */}
        <div className="flex items-center gap-2 shrink-0">
          <div className="w-7 h-7 rounded-full bg-teal flex items-center justify-center">
            <span className="text-white font-bold text-xs">SA</span>
          </div>
          <span className="font-bold text-gray-800 text-base hidden sm:block">
            StockAlerts
          </span>
        </div>

        {/* Nav */}
        <nav className="hidden md:flex items-center gap-5 text-sm text-gray-600">
          <a href="#" className="hover:text-teal font-medium text-gray-800 border-b-2 border-teal pb-0.5">Announcements</a>
          <a href="#" className="hover:text-teal">Infosys</a>
          <a href="#" className="hover:text-teal">HCL</a>
          <a href="#" className="hover:text-teal">Reliance</a>
          <a href="#" className="hover:text-teal">TCS</a>
        </nav>

        {/* Right */}
        <div className="flex items-center gap-3 shrink-0">
          <div className="relative hidden sm:block">
            <input
              type="text"
              placeholder="Search announcements…"
              className="text-sm border border-gray-200 rounded-full px-4 py-1.5 pr-8 w-48 focus:outline-none focus:border-teal"
            />
            <svg className="absolute right-3 top-2 w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-4.35-4.35M17 11A6 6 0 1 1 5 11a6 6 0 0 1 12 0z" />
            </svg>
          </div>
          <div className="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center text-gray-500 text-xs font-medium cursor-pointer">
            M
          </div>
        </div>
      </div>
    </header>
  );
}
