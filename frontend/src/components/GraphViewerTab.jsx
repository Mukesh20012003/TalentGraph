import React, { useState, useEffect, useRef } from 'react';
import ForceGraph2D from 'react-force-graph-2d';
import { fetchGraphSnapshot } from '../api';
import { RefreshCw, ZoomIn, ZoomOut, Maximize2, Info } from 'lucide-react';

const NODE_COLORS = {
  Person: '#6366f1',   // Indigo
  Skill: '#10b981',    // Emerald
  Company: '#f59e0b',  // Amber
  Project: '#ef4444',  // Rose
};

export default function GraphViewerTab() {
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });
  const [loading, setLoading] = useState(true);
  const [selectedNode, setSelectedNode] = useState(null);
  const fgRef = useRef();

  const loadData = async () => {
    setLoading(true);
    try {
      const data = await fetchGraphSnapshot(140);
      setGraphData(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  return (
    <div className="relative w-full h-[700px] rounded-2xl overflow-hidden border border-slate-800 bg-slate-950 flex">
      
      {/* Legend & Controls Overlay */}
      <div className="absolute top-4 left-4 z-10 p-3 rounded-xl bg-slate-900/90 backdrop-blur border border-slate-800 text-xs space-y-2 shadow-xl">
        <span className="font-semibold text-slate-300 block">Graph Schema Legend</span>
        <div className="flex flex-col space-y-1">
          {Object.entries(NODE_COLORS).map(([type, color]) => (
            <div key={type} className="flex items-center space-x-2">
              <span className="w-3 h-3 rounded-full" style={{ backgroundColor: color }} />
              <span className="text-slate-300">{type}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="absolute top-4 right-4 z-10 flex space-x-2">
        <button
          onClick={loadData}
          className="p-2 rounded-xl bg-slate-900/90 hover:bg-slate-800 border border-slate-800 text-slate-300 transition"
          title="Reload Graph"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
        </button>
      </div>

      {/* Force-directed Graph Canvas */}
      <div className="flex-1 w-full h-full">
        <ForceGraph2D
          ref={fgRef}
          graphData={graphData}
          nodeLabel={(node) => `${node.group}: ${node.name}`}
          nodeColor={(node) => NODE_COLORS[node.group] || '#94a3b8'}
          nodeRelSize={6}
          linkColor={() => '#334155'}
          linkDirectionalParticles={2}
          linkDirectionalParticleSpeed={0.005}
          linkDirectionalParticleWidth={1.5}
          linkDirectionalParticleColor={() => '#818cf8'}
          onNodeClick={(node) => setSelectedNode(node)}
          backgroundColor="#090d16"
        />
      </div>

      {/* Selected Node Drawer */}
      {selectedNode && (
        <div className="absolute bottom-4 right-4 w-80 p-4 rounded-2xl bg-slate-900/95 backdrop-blur-md border border-slate-700/80 shadow-2xl z-20 text-xs">
          <div className="flex items-center justify-between pb-2 border-b border-slate-800">
            <span
              className="px-2 py-0.5 rounded text-[10px] font-bold uppercase"
              style={{ backgroundColor: `${NODE_COLORS[selectedNode.group]}20`, color: NODE_COLORS[selectedNode.group] }}
            >
              {selectedNode.group}
            </span>
            <button
              onClick={() => setSelectedNode(null)}
              className="text-slate-500 hover:text-white"
            >
              ✕
            </button>
          </div>

          <h4 className="text-base font-bold text-white mt-2">{selectedNode.name}</h4>
          
          <div className="mt-3 space-y-1.5 max-h-48 overflow-y-auto">
            {Object.entries(selectedNode.properties || {}).map(([k, v]) => (
              <div key={k} className="flex justify-between border-b border-slate-800/40 py-1">
                <span className="text-slate-400 capitalize">{k.replace('_', ' ')}:</span>
                <span className="text-slate-200 font-mono font-medium truncate max-w-[140px]">{String(v)}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}