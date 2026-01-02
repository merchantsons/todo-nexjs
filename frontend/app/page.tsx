import Link from 'next/link';
import Button from '@/components/ui/Button';
import Footer from '@/components/layout/Footer';

export default function LandingPage() {
  return (
    <div className="min-h-[100dvh] h-[100dvh] sm:h-screen flex flex-col bg-gradient-to-b from-green-50 to-white overflow-hidden">
      <header className="flex-shrink-0 max-w-7xl mx-auto px-3 sm:px-4 md:px-6 lg:px-8 py-2 sm:py-3 md:py-4 lg:py-6 w-full">
        <div className="flex flex-col sm:flex-row justify-between items-center gap-2 sm:gap-3 md:gap-0">
          <Link href="/" className="flex items-center gap-1.5 sm:gap-2 md:gap-3 justify-center sm:justify-start">
            <span className="text-xl sm:text-2xl md:text-3xl lg:text-4xl xl:text-5xl">📚</span>
            <h1 className="text-lg sm:text-xl md:text-2xl lg:text-3xl xl:text-4xl 2xl:text-5xl font-bold cursor-pointer" style={{ color: '#0d2818', fontFamily: 'var(--font-lavishly-yours), cursive' }}>Evolution of Todo</h1>
          </Link>
          <div className="flex gap-1.5 sm:gap-2 md:gap-4 w-full sm:w-auto justify-center sm:justify-end">
            <Link href="/login" className="flex-1 sm:flex-initial">
              <Button variant="secondary" className="w-full sm:w-auto text-xs sm:text-sm md:text-base px-3 sm:px-4 md:px-6 py-1.5 sm:py-2 md:py-3">Login</Button>
            </Link>
            <Link href="/register" className="flex-1 sm:flex-initial">
              <Button variant="primary" className="w-full sm:w-auto text-xs sm:text-sm md:text-base px-3 sm:px-4 md:px-6 py-1.5 sm:py-2 md:py-3">Register</Button>
            </Link>
          </div>
        </div>
      </header>
      
      <main className="flex-1 overflow-y-auto max-w-7xl mx-auto px-3 sm:px-4 md:px-6 lg:px-8 py-1 sm:py-2 md:py-4 lg:py-6 w-full flex flex-col min-h-0">
        <div className="text-center mb-1 sm:mb-3 md:mb-4 lg:mb-6 flex-shrink-0">
          <h2 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl xl:text-6xl 2xl:text-7xl mb-1 sm:mb-2 md:mb-3 lg:mb-4 px-2 font-bold flex flex-col sm:flex-row items-center justify-center gap-1 sm:gap-2 md:gap-3 lg:gap-4" style={{ color: '#0d2818', fontFamily: 'var(--font-poppins)' }}>
            <span className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl xl:text-6xl 2xl:text-7xl">📚</span>
            <span>Evolution of Todo</span>
          </h2>
          <p className="text-xs sm:text-sm md:text-base lg:text-lg xl:text-xl text-gray-700 mb-1.5 sm:mb-3 md:mb-4 lg:mb-6 px-2 sm:px-4">
            Your personal task management solution
          </p>
          <Link href="/register">
            <Button variant="primary" className="text-xs sm:text-sm md:text-base lg:text-lg px-4 sm:px-5 md:px-6 lg:px-8 py-2 sm:py-2.5 md:py-3 lg:py-4">
              Get Started →
            </Button>
          </Link>
          <p className="mt-1.5 sm:mt-2 md:mt-3 lg:mt-4 text-[10px] sm:text-xs md:text-sm lg:text-base text-gray-600 px-2 sm:px-4">
            Already have an account?{" "}
            <Link href="/login" className="text-green-700 hover:text-green-800 font-medium transition-colors">
              Log in
            </Link>
          </p>
        </div>
        
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2 sm:gap-3 md:gap-4 lg:gap-6 xl:gap-8 mt-1 sm:mt-3 md:mt-4 lg:mt-6 flex-shrink-0 pb-2 sm:pb-4">
          <div className="bg-white rounded-lg p-2.5 sm:p-3 md:p-4 lg:p-6 shadow-lg border border-green-100 hover:shadow-xl transition-shadow">
            <div className="text-xl sm:text-2xl md:text-3xl lg:text-4xl mb-1.5 sm:mb-2 md:mb-3 lg:mb-4">✓</div>
            <h3 className="text-sm sm:text-base md:text-lg lg:text-xl font-semibold mb-1 sm:mb-1.5 md:mb-2 text-gray-900">Secure</h3>
            <p className="text-[10px] sm:text-xs md:text-sm lg:text-base text-gray-600">Your data protected with JWT authentication</p>
          </div>
          
          <div className="bg-white rounded-lg p-2.5 sm:p-3 md:p-4 lg:p-6 shadow-lg border border-green-100 hover:shadow-xl transition-shadow">
            <div className="text-xl sm:text-2xl md:text-3xl lg:text-4xl mb-1.5 sm:mb-2 md:mb-3 lg:mb-4">✨</div>
            <h3 className="text-sm sm:text-base md:text-lg lg:text-xl font-semibold mb-1 sm:mb-1.5 md:mb-2 text-gray-900">Simple</h3>
            <p className="text-[10px] sm:text-xs md:text-sm lg:text-base text-gray-600">Clean UI easy to use</p>
          </div>
          
          <div className="bg-white rounded-lg p-2.5 sm:p-3 md:p-4 lg:p-6 shadow-lg border border-green-100 hover:shadow-xl transition-shadow">
            <div className="text-xl sm:text-2xl md:text-3xl lg:text-4xl mb-1.5 sm:mb-2 md:mb-3 lg:mb-4">🔒</div>
            <h3 className="text-sm sm:text-base md:text-lg lg:text-xl font-semibold mb-1 sm:mb-1.5 md:mb-2 text-gray-900">Private</h3>
            <p className="text-[10px] sm:text-xs md:text-sm lg:text-base text-gray-600">Your tasks only yours</p>
          </div>
        </div>
      </main>
      
      <div className="flex-shrink-0">
        <Footer />
      </div>
    </div>
  );
}
