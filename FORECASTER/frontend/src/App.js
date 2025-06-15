import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'react-hot-toast';
import { motion } from 'framer-motion';

// Layout Components
import Navbar from './components/layout/Navbar';
import Sidebar from './components/layout/Sidebar';

// Page Components
import Dashboard from './pages/Dashboard';
import Forecasting from './pages/Forecasting';
import Analytics from './pages/Analytics';
import WhatIf from './pages/WhatIf';
import Alerts from './pages/Alerts';
import Settings from './pages/Settings';
import Login from './pages/Login';

// Hooks and Utils
import { useAuthStore } from './store/authStore';
import { useThemeStore } from './store/themeStore';

// Styles
import './App.css';

// Create a client for React Query
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

function App() {
  const { isAuthenticated, user } = useAuthStore();
  const { theme } = useThemeStore();

  return (
    <QueryClientProvider client={queryClient}>
      <div className={`App ${theme === 'dark' ? 'dark' : ''}`}>
        <Router>
          <Toaster
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: theme === 'dark' ? '#374151' : '#fff',
                color: theme === 'dark' ? '#f3f4f6' : '#111827',
              },
            }}
          />
          
          {!isAuthenticated ? (
            <Login />
          ) : (
            <div className="flex h-screen bg-gray-50 dark:bg-gray-900">
              {/* Sidebar */}
              <Sidebar />
              
              {/* Main Content */}
              <div className="flex-1 flex flex-col overflow-hidden">
                {/* Navbar */}
                <Navbar />
                
                {/* Main Content Area */}
                <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-50 dark:bg-gray-900">
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.3 }}
                    className="container mx-auto px-6 py-8"
                  >
                    <Routes>
                      <Route path="/" element={<Dashboard />} />
                      <Route path="/dashboard" element={<Dashboard />} />
                      <Route path="/forecasting" element={<Forecasting />} />
                      <Route path="/analytics" element={<Analytics />} />
                      <Route path="/what-if" element={<WhatIf />} />
                      <Route path="/alerts" element={<Alerts />} />
                      <Route path="/settings" element={<Settings />} />
                    </Routes>
                  </motion.div>
                </main>
              </div>
            </div>
          )}
        </Router>
      </div>
    </QueryClientProvider>
  );
}

export default App; 