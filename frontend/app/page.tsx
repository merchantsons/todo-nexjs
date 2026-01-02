import Link from 'next/link';
import Button from '@/components/ui/Button';
import Footer from '@/components/layout/Footer';

export default function LandingPage() {
  return (
    <div className="h-screen flex flex-col bg-gradient-to-b from-green-50 to-white overflow-hidden">
      <header className="flex-shrink-0 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3 sm:py-4 md:py-6 w-full">
        <div className="flex flex-col sm:flex-row justify-between items-center gap-3 sm:gap-0">
          <Link href="/" className="flex items-center gap-2 sm:gap-3 justify-center sm:justify-start">
            <span className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl">📚</span>
            <h1 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold cursor-pointer" style={{ color: '#0d2818', fontFamily: 'var(--font-lavishly-yours), cursive' }}>Evolution of Todo</h1>
          </Link>
          <div className="flex gap-2 sm:gap-4 w-full sm:w-auto justify-center sm:justify-end">
            <Link href="/login" className="flex-1 sm:flex-initial">
              <Button variant="secondary" className="w-full sm:w-auto text-sm sm:text-base px-4 sm:px-6 py-2 sm:py-3">Login</Button>
            </Link>
            <Link href="/register" className="flex-1 sm:flex-initial">
              <Button variant="primary" className="w-full sm:w-auto text-sm sm:text-base px-4 sm:px-6 py-2 sm:py-3">Register</Button>
            </Link>
          </div>
        </div>
      </header>
      
      <main className="flex-1 overflow-y-auto max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-6 md:py-8 w-full">
        <div className="text-center mb-4 sm:mb-6 md:mb-8">
          <h2 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl xl:text-7xl mb-2 sm:mb-3 md:mb-4 px-2 font-bold flex items-center justify-center gap-2 sm:gap-3 md:gap-4" style={{ color: '#0d2818', fontFamily: 'var(--font-poppins)' }}>
            <span className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl xl:text-7xl">📚</span>
            <span>Evolution of Todo</span>
          </h2>
          <p className="text-sm sm:text-base md:text-lg lg:text-xl text-gray-700 mb-4 sm:mb-6 md:mb-8 px-4">
            Your personal task management solution
          </p>
          <Link href="/register">
            <Button variant="primary" className="text-sm sm:text-base md:text-lg px-5 sm:px-6 md:px-8 py-2.5 sm:py-3 md:py-4">
              Get Started →
            </Button>
          </Link>
          <p className="mt-3 sm:mt-4 text-xs sm:text-sm md:text-base text-gray-600 px-4">
            Already have an account?{" "}
            <Link href="/login" className="text-green-700 hover:text-green-800 font-medium transition-colors">
              Log in
            </Link>
          </p>
        </div>
        
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-4 md:gap-6 lg:gap-8 mt-4 sm:mt-6 md:mt-8">
          <div className="bg-white rounded-lg p-3 sm:p-4 md:p-6 shadow-lg border border-green-100 hover:shadow-xl transition-shadow">
            <div className="text-2xl sm:text-3xl md:text-4xl mb-2 sm:mb-3 md:mb-4">✓</div>
            <h3 className="text-base sm:text-lg md:text-xl font-semibold mb-1 sm:mb-2 text-gray-900">Secure</h3>
            <p className="text-xs sm:text-sm md:text-base text-gray-600">Your data protected with JWT authentication</p>
          </div>
          
          <div className="bg-white rounded-lg p-3 sm:p-4 md:p-6 shadow-lg border border-green-100 hover:shadow-xl transition-shadow">
            <div className="text-2xl sm:text-3xl md:text-4xl mb-2 sm:mb-3 md:mb-4">✨</div>
            <h3 className="text-base sm:text-lg md:text-xl font-semibold mb-1 sm:mb-2 text-gray-900">Simple</h3>
            <p className="text-xs sm:text-sm md:text-base text-gray-600">Clean UI easy to use</p>
          </div>
          
          <div className="bg-white rounded-lg p-3 sm:p-4 md:p-6 shadow-lg border border-green-100 hover:shadow-xl transition-shadow">
            <div className="text-2xl sm:text-3xl md:text-4xl mb-2 sm:mb-3 md:mb-4">🔒</div>
            <h3 className="text-base sm:text-lg md:text-xl font-semibold mb-1 sm:mb-2 text-gray-900">Private</h3>
            <p className="text-xs sm:text-sm md:text-base text-gray-600">Your tasks only yours</p>
          </div>
        </div>
      </main>
      
      <div className="flex-shrink-0">
        <Footer />
      </div>
    </div>
  );
}
