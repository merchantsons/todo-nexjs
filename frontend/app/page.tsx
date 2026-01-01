import Link from 'next/link';
import Button from '@/components/ui/Button';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      <header className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">Evolution of Todo</h1>
          <div className="flex gap-4">
            <Link href="/login">
              <Button variant="secondary">Login</Button>
            </Link>
            <Link href="/register">
              <Button variant="primary">Register</Button>
            </Link>
          </div>
        </div>
      </header>
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-16">
          <h2 className="text-5xl font-bold text-gray-900 mb-4">
            Evolution of Todo
          </h2>
          <p className="text-xl text-gray-600 mb-8">
            Your personal task management solution
          </p>
          <Link href="/register">
            <Button variant="primary" className="text-lg px-8 py-4">
              Get Started →
            </Button>
          </Link>
          <p className="mt-4 text-gray-600">
            Already have an account?{" "}
            <Link href="/login" className="text-blue-600 hover:underline">
              Log in
            </Link>
          </p>
        </div>
        
        <div className="grid md:grid-cols-3 gap-8 mt-16">
          <div className="bg-white rounded-lg p-6 shadow">
            <div className="text-4xl mb-4">✓</div>
            <h3 className="text-xl font-semibold mb-2">Secure</h3>
            <p className="text-gray-600">Your data protected with JWT authentication</p>
          </div>
          
          <div className="bg-white rounded-lg p-6 shadow">
            <div className="text-4xl mb-4">✨</div>
            <h3 className="text-xl font-semibold mb-2">Simple</h3>
            <p className="text-gray-600">Clean UI easy to use</p>
          </div>
          
          <div className="bg-white rounded-lg p-6 shadow">
            <div className="text-4xl mb-4">🔒</div>
            <h3 className="text-xl font-semibold mb-2">Private</h3>
            <p className="text-gray-600">Your tasks only yours</p>
          </div>
        </div>
      </main>
    </div>
  );
}
