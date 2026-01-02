"use client";

import React from 'react';

export default function Footer() {
  const currentYear = new Date().getFullYear();
  
  return (
    <footer className="gradient-green text-white mt-auto">
      <div className="max-w-7xl mx-auto px-2 sm:px-4 md:px-6 lg:px-8 py-2 sm:py-3 md:py-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-2 sm:gap-3 md:gap-4">
          <div className="md:col-span-1">
            <h3 className="text-xs sm:text-sm md:text-lg lg:text-xl font-bold mb-1 sm:mb-2" style={{ color: '#ffffff', fontFamily: 'var(--font-poppins)' }}>Evolution of Todo</h3>
            <p className="text-green-100 text-[9px] sm:text-xs md:text-sm">
              Your personal task management solution. Stay organized and productive.
            </p>
          </div>
          
          <div className="grid grid-cols-2 gap-2 sm:gap-3 md:gap-4 md:col-span-2">
            <div>
              <h4 className="font-semibold mb-1 sm:mb-2 text-[9px] sm:text-xs md:text-sm">Quick Links</h4>
              <ul className="space-y-0.5 sm:space-y-1 text-[9px] sm:text-xs md:text-sm">
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
              <h4 className="font-semibold mb-1 sm:mb-2 text-[9px] sm:text-xs md:text-sm">Features</h4>
              <ul className="space-y-0.5 sm:space-y-1 text-[9px] sm:text-xs md:text-sm text-green-100">
                <li>✓ Secure Authentication</li>
                <li>✓ Task Management</li>
                <li>✓ Real-time Updates</li>
                <li>✓ Clean Interface</li>
              </ul>
            </div>
          </div>
        </div>
        
        <div className="border-t border-green-700 mt-2 sm:mt-2.5 md:mt-3 pt-2 sm:pt-2.5 md:pt-3 text-center text-[9px] sm:text-xs md:text-sm text-green-100 px-2 sm:px-4">
          <p className="mb-0.5 sm:mb-1">© {currentYear} Evolution of Todo. All rights reserved.</p>
          <p className="break-words">Developed by: Merchantsons For GIAIC Hackathon 2 - Roll # 00037391</p>
        </div>
      </div>
    </footer>
  );
}

