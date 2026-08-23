import React, { useState, useEffect } from 'react';
import { fetchProjectMatchmaker } from '../api';
import { Cpu, Users, CheckCircle2, UserCheck, Flame, Percent } from 'lucide-react';

export default function ProjectMatchmakerTab({ metadata }) {
  const [selectedProject, setSelectedProject] = useState('');
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (metadata.projects?.length && !selectedProject) {
      setSelectedProject(metadata.projects[0]);
    }
  }, [metadata]);

  const handleMatch = async (e) => {
    if (e) e.preventDefault();
    if (!selectedProject) return;

    setLoading(true);
    setError(null);
    try {
      const res = await fetchProjectMatchmaker(selectedProject);
      setData(res);
    } catch (err) {
      setError(err.message || 'Error running project matchmaker query');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="p-6 rounded-2xl bg-gradient-to-r from-emerald-950/40 via-slate-900 to-slate-900 border border-emerald-500/20">
        <div className="flex items-center space-x-3 mb-2">
          <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
            Graph Compatibility & Affinity Matchmaker
          </span>
          <span className="text-xs text-slate-400">Complex Cross-Pattern Traversal</span>
        </div>
        <h2 className="text-2xl font-bold text-white">Project Staffing & Team Matchmaker</h2>
        <p className="text-sm text-slate-300 mt-1 max-w-2xl">
          Instantly ranks engineers by stack overlap with the project requirements while simultaneously computing which existing project contributors they already have past working relationships with.
        </p>

        {/* Project Selector Form */}
        <form onSubmit={handleMatch} className="mt-6 flex flex-col md:flex-row gap-4 max-w-xl">
          <div className="flex-1">
            <select
              value={selectedProject}
              onChange={(e) => setSelectedProject(e.target.value)}
              className="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2.5 text-sm text-white focus:ring-2 focus:ring-emerald-500 outline-none"
            >
              {metadata.projects?.map((p) => (
                <option key={p} value={p}>{p}</option>
              ))}
            </select>
          </div>
          <button
            type="submit"
            disabled={loading}
            className="bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-white font-medium py-2.5 px-6 rounded-xl transition flex items-center justify-center space-x-2 shadow-lg shadow-emerald-600/30"
          >
            {loading ? (
              <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            ) : (
              <>
                <Cpu className="w-4 h-4" />
                <span>Evaluate Candidates</span>
              </>
            )}
          </button>
        </form>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-sm">
          {error}
        </div>
      )}

      {data && (
        <div className="space-y-4">
          <div className="flex items-center justify-between text-sm text-slate-400 px-1">
            <span>Candidates scored for <strong className="text-white">{data.project}</strong></span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {data.top_candidates.map((c, idx) => (
              <div key={idx} className="p-5 bg-slate-800/50 hover:bg-slate-800/80 transition rounded-2xl border border-slate-700/60 flex flex-col justify-between space-y-4">
                <div>
                  <div className="flex items-start justify-between">
                    <div>
                      <h3 className="text-lg font-bold text-white">{c.name}</h3>
                      <p className="text-sm text-slate-400">{c.title} • {c.location}</p>
                    </div>
                    
                    {/* Match Score Badge */}
                    <div className="flex flex-col items-end">
                      <div className="flex items-center space-x-1 px-2.5 py-1 rounded-lg bg-emerald-500/10 text-emerald-300 border border-emerald-500/30 font-mono font-bold text-sm">
                        <Percent className="w-3.5 h-3.5" />
                        <span>{c.match_percentage}%</span>
                      </div>
                      <span className="text-[10px] text-slate-500 mt-1">
                        {c.matchCount} / {c.totalSkillsRequired} skills
                      </span>
                    </div>
                  </div>

                  {/* Matched Skills */}
                  <div className="mt-4">
                    <span className="text-xs text-slate-400 font-medium block mb-1.5">Stack Overlap:</span>
                    <div className="flex flex-wrap gap-1.5">
                      {c.matchedSkills.map((sk, skIdx) => (
                        <span key={skIdx} className="text-xs px-2 py-0.5 rounded-md bg-slate-700/80 text-slate-200 border border-slate-600">
                          {sk.skill} <span className="text-slate-400 text-[10px]">({sk.level})</span>
                        </span>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Team Familiarity / Co-worker affinity */}
                <div className="pt-3 border-t border-slate-700/50">
                  <div className="flex items-center space-x-2 text-xs">
                    <Users className="w-3.5 h-3.5 text-indigo-400" />
                    <span className="text-slate-400 font-medium">Team Familiarity:</span>
                  </div>
                  {c.team_connections && c.team_connections.length > 0 ? (
                    <p className="text-xs text-indigo-300 mt-1">
                      Already worked with: <strong className="text-white">{c.team_connections.join(', ')}</strong>
                    </p>
                  ) : (
                    <p className="text-xs text-slate-500 mt-1">No prior direct project teammates (New connection)</p>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}