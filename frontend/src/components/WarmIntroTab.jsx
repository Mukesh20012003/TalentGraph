import React, { useState, useEffect } from 'react';
import { fetchWarmIntroductions } from '../api';
import { GitMerge, ArrowRight, UserCheck, ShieldCheck, Sparkles, MapPin, Briefcase } from 'lucide-react';

export default function WarmIntroTab({ metadata }) {
  const [referrer, setReferrer] = useState('');
  const [targetSkill, setTargetSkill] = useState('');
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (metadata.persons?.length && !referrer) {
      setReferrer(metadata.persons[0]);
    }
    if (metadata.skills?.length && !targetSkill) {
      setTargetSkill('Rust');
    }
  }, [metadata]);

  const handleSearch = async (e) => {
    if (e) e.preventDefault();
    if (!referrer || !targetSkill) return;

    setLoading(true);
    setError(null);
    try {
      const res = await fetchWarmIntroductions(referrer, targetSkill);
      setData(res);
    } catch (err) {
      setError(err.message || 'Error executing multi-hop traversal query.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Hero & Query Explanation */}
      <div className="p-6 rounded-2xl bg-gradient-to-r from-indigo-900/40 via-slate-900 to-slate-900 border border-indigo-500/20">
        <div className="flex items-center space-x-3 mb-2">
          <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-500/10 text-indigo-400 border border-indigo-500/30">
            Multi-Hop Cypher Traversal
          </span>
          <span className="text-xs text-slate-400">(:Person)-[:KNOWS*1..2]-(:Person)-[:HAS_SKILL]-&gt;(:Skill)</span>
        </div>
        <h2 className="text-2xl font-bold text-white">Warm Introduction Finder</h2>
        <p className="text-sm text-slate-300 mt-1 max-w-2xl">
          Discover candidate engineers who possess your desired technical skill and are 1 to 2 degrees of separation away from you in the professional network.
        </p>

        {/* Input form */}
        <form onSubmit={handleSearch} className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1.5">Who is asking? (Referrer)</label>
            <select
              value={referrer}
              onChange={(e) => setReferrer(e.target.value)}
              className="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2.5 text-sm text-white focus:ring-2 focus:ring-indigo-500 outline-none"
            >
              {metadata.persons?.map((p) => (
                <option key={p} value={p}>{p}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1.5">Target Skill Needed</label>
            <select
              value={targetSkill}
              onChange={(e) => setTargetSkill(e.target.value)}
              className="w-full bg-slate-800 border border-slate-700 rounded-xl px-3 py-2.5 text-sm text-white focus:ring-2 focus:ring-indigo-500 outline-none"
            >
              {metadata.skills?.map((s) => (
                <option key={s} value={s}>{s}</option>
              ))}
            </select>
          </div>

          <div className="flex items-end">
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white font-medium py-2.5 px-4 rounded-xl transition flex items-center justify-center space-x-2 shadow-lg shadow-indigo-600/30"
            >
              {loading ? (
                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              ) : (
                <>
                  <Sparkles className="w-4 h-4" />
                  <span>Traverse Graph</span>
                </>
              )}
            </button>
          </div>
        </form>
      </div>

      {/* Traversal Results */}
      {error && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-sm">
          {error}
        </div>
      )}

      {data && (
        <div className="space-y-4">
          <div className="flex items-center justify-between text-sm text-slate-400 px-1">
            <span>Found <strong className="text-white">{data.total_matches}</strong> candidates with <span className="text-indigo-400 font-mono">{data.target_skill}</span> within 2 hops of <strong className="text-white">{data.referrer}</strong></span>
          </div>

          {data.candidates.length === 0 ? (
            <div className="text-center py-12 bg-slate-800/30 rounded-2xl border border-slate-800">
              <p className="text-slate-400">No candidates found within 2 network hops. Try another skill or referrer.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {data.candidates.map((c, idx) => (
                <div key={idx} className="p-5 bg-slate-800/50 hover:bg-slate-800/80 transition rounded-2xl border border-slate-700/60 flex flex-col justify-between space-y-4">
                  <div>
                    <div className="flex items-start justify-between">
                      <div>
                        <h3 className="text-lg font-bold text-white flex items-center space-x-2">
                          <span>{c.candidate_name}</span>
                          <span className="text-xs px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                            {c.degrees_of_separation} {c.degrees_of_separation === 1 ? 'Hop (Direct)' : 'Hops (2nd Degree)'}
                          </span>
                        </h3>
                        <p className="text-sm text-indigo-300 font-medium mt-0.5">{c.title}</p>
                      </div>
                      <span className="text-xs px-2.5 py-1 rounded-md bg-emerald-500/10 text-emerald-300 border border-emerald-500/20 font-mono font-medium">
                        {c.skill_level} in {c.matched_skill}
                      </span>
                    </div>

                    <div className="mt-3 flex items-center space-x-4 text-xs text-slate-400">
                      <div className="flex items-center space-x-1">
                        <MapPin className="w-3.5 h-3.5" />
                        <span>{c.location}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Briefcase className="w-3.5 h-3.5" />
                        <span>{c.years_experience} yrs exp</span>
                      </div>
                    </div>
                  </div>

                  {/* Visual Connection Path Breadcrumbs */}
                  <div className="pt-3 border-t border-slate-700/50">
                    <span className="text-xs text-slate-400 block mb-1.5 font-medium">Introduction Path:</span>
                    <div className="flex items-center flex-wrap gap-1.5 text-xs">
                      {c.connection_path.map((node, stepIdx) => (
                        <React.Fragment key={stepIdx}>
                          <span className={`px-2 py-1 rounded-md font-mono ${
                            stepIdx === 0
                              ? 'bg-slate-700 text-slate-300'
                              : stepIdx === c.connection_path.length - 1
                              ? 'bg-indigo-600/30 text-indigo-200 border border-indigo-500/40 font-semibold'
                              : 'bg-slate-800 text-slate-300 border border-slate-700'
                          }`}>
                            {node}
                          </span>
                          {stepIdx < c.connection_path.length - 1 && (
                            <ArrowRight className="w-3 h-3 text-slate-500" />
                          )}
                        </React.Fragment>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}