"use client";

import React from 'react';

export default function Footer() {
  const currentYear = new Date().getFullYear();
  
  return (
    <footer className="gradient-green text-white mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-5 md:py-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 sm:gap-5 md:gap-6">
          <div className="md:col-span-1">
            <h3 className="text-lg sm:text-xl md:text-2xl font-bold mb-2 sm:mb-3" style={{ color: '#ffffff', fontFamily: 'var(--font-poppins)' }}>Evolution of Todo</h3>
            <p className="text-green-100 text-xs sm:text-sm">
              Your personal task management solution. Stay organized and productive.
            </p>
          </div>
          
          <div className="grid grid-cols-2 gap-3 sm:gap-4 md:gap-6 md:col-span-2">
            <div>
              <h4 className="font-semibold mb-2 sm:mb-3 text-xs sm:text-sm md:text-base">Quick Links</h4>
              <ul className="space-y-1 sm:space-y-1.5 text-xs sm:text-sm">
                <li>
                  <a href="/" className="text-green-100 hover:text-white transition-colors">
                    Home
                  </a>
                </li>
                <li>
                  <a href="/dashboard" className="text-green-100 hover:text-white transition-colors">
                    Dashboard
                  </a>
                </li>
                <li>
                  <a href="/login" className="text-green-100 hover:text-white transition-colors">
                    Login
                  </a>
                </li>
                <li>
                  <a href="/register" className="text-green-100 hover:text-white transition-colors">
                    Register
                  </a>
                </li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold mb-2 sm:mb-3 text-xs sm:text-sm md:text-base">Features</h4>
              <ul className="space-y-1 sm:space-y-1.5 text-xs sm:text-sm text-green-100">
                <li>✓ Secure Authentication</li>
                <li>✓ Task Management</li>
                <li>✓ Real-time Updates</li>
                <li>✓ Clean Interface</li>
              </ul>
            </div>
          </div>
        </div>
        
        <div className="border-t border-green-700 mt-3 sm:mt-4 md:mt-5 pt-3 sm:pt-4 md:pt-5 text-center text-xs sm:text-sm text-green-100 px-4">
          <p className="mb-1">© {currentYear} Evolution of Todo. All rights reserved.</p>
          <p className="break-words">Developed by: Merchantsons For GIAIC Hackathon 2 - Roll # 00037391</p>
        </div>
      </div>
    </footer>
  );
}

