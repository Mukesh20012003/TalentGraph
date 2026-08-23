import React from 'react';
import { Database, Network, Search, Cpu, Users, GitMerge, Activity } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, health }) {
  const isHealthy = health?.status === 'healthy';

  const navItems = [
    { id: 'network', label: 'Warm Introductions', icon: GitMerge },
    { id: 'matchmaker', label: 'Project Matchmaker', icon: Cpu },
    { id: 'search', label: 'Talent Directory', icon: Search },
    { id: 'visualizer', label: 'Graph Explorer', icon: Network },
  ];

  return (
    <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Logo */}
          <div className="flex items-center space-x-3 cursor-pointer" onClick={() => setActiveTab('network')}>
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-violet-500 flex items-center justify-center shadow-lg shadow-indigo-500/20">
              <Network className="w-6 h-6 text-white" />
            </div>
            <div>
              <span className="text-lg font-bold bg-gradient-to-r from-white via-slate-200 to-indigo-300 bg-clip-text text-transparent">
                TalentGraph
              </span>
              <span className="text-xs block text-slate-400 font-mono">Powered by CognoDB</span>
            </div>
          </div>

          {/* Navigation Tabs */}
          <nav className="hidden md:flex space-x-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const active = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`flex items-center space-x-2 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                    active
                      ? 'bg-indigo-600/10 text-indigo-400 border border-indigo-500/30'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </nav>

          {/* Live DB Status indicator */}
          <div className="flex items-center space-x-3">
            <div className="flex items-center space-x-2 px-3 py-1.5 rounded-full bg-slate-800/80 border border-slate-700/60 text-xs">
              <span className={`w-2 h-2 rounded-full ${isHealthy ? 'bg-emerald-400 animate-pulse' : 'bg-rose-500'}`} />
              <span className="text-slate-300 font-medium">
                {isHealthy ? 'CognoDB Connected' : 'DB Offline'}
              </span>
            </div>
          </div>

        </div>
      </div>
    </header>
  );
}