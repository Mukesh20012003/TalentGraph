import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import WarmIntroTab from './components/WarmIntroTab';
import ProjectMatchmakerTab from './components/ProjectMatchmakerTab';
import TalentSearchTab from './components/TalentSearchTab';
import GraphViewerTab from './components/GraphViewerTab';
import { fetchHealth, fetchMetadata } from './api';
import { Database, AlertTriangle } from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('network');
  const [health, setHealth] = useState(null);
  const [metadata, setMetadata] = useState({ persons: [], skills: [], companies: [], projects: [] });
  const [error, setError] = useState(null);

  useEffect(() => {
    async function init() {
      try {
        const [healthRes, metaRes] = await Promise.all([
          fetchHealth(),
          fetchMetadata()
        ]);
        setHealth(healthRes);
        setMetadata(metaRes);
      } catch (err) {
        console.error('System init error:', err);
        setError('Cannot connect to CognoDB backend. Ensure FastAPI server is running.');
      }
    }
    init();
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} health={health} />

      {/* Backend / DB Offline Banner */}
      {error && (
        <div className="bg-rose-500/10 border-b border-rose-500/30 px-4 py-2.5 text-center text-xs text-rose-300 flex items-center justify-center space-x-2">
          <AlertTriangle className="w-4 h-4" />
          <span>{error}</span>
        </div>
      )}

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'network' && <WarmIntroTab metadata={metadata} />}
        {activeTab === 'matchmaker' && <ProjectMatchmakerTab metadata={metadata} />}
        {activeTab === 'search' && <TalentSearchTab metadata={metadata} />}
        {activeTab === 'visualizer' && <GraphViewerTab />}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-900 py-6 text-center text-xs text-slate-500">
        Built for Wexa AI Take-Home Assignment • CognoDB Graph Engine & openCypher
      </footer>
    </div>
  );
}