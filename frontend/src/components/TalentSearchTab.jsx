import React, { useState, useEffect } from 'react';
import { searchTalent } from '../api';
import { Search, MapPin, Briefcase, Mail, Filter } from 'lucide-react';

export default function TalentSearchTab({ metadata }) {
  const [skill, setSkill] = useState('');
  const [company, setCompany] = useState('');
  const [minExp, setMinExp] = useState(0);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const runSearch = async () => {
    setLoading(true);
    try {
      const res = await searchTalent({
        skill: skill || undefined,
        company: company || undefined,
        minExperience: minExp || undefined,
      });
      setResults(res.results || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    runSearch();
  }, [skill, company, minExp]);

  return (
    <div className="space-y-6">
      {/* Filters Bar */}
      <div className="p-5 rounded-2xl bg-slate-900 border border-slate-800 flex flex-wrap gap-4 items-center justify-between">
        <div className="flex flex-wrap items-center gap-3 flex-1">
          <div className="flex items-center space-x-2 text-xs font-semibold text-slate-400 uppercase tracking-wider">
            <Filter className="w-4 h-4" />
            <span>Filters:</span>
          </div>

          <select
            value={skill}
            onChange={(e) => setSkill(e.target.value)}
            className="bg-slate-800 border border-slate-700 rounded-xl px-3 py-1.5 text-xs text-white outline-none focus:border-indigo-500"
          >
            <option value="">All Skills</option>
            {metadata.skills?.map((s) => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>

          <select
            value={company}
            onChange={(e) => setCompany(e.target.value)}
            className="bg-slate-800 border border-slate-700 rounded-xl px-3 py-1.5 text-xs text-white outline-none focus:border-indigo-500"
          >
            <option value="">All Companies</option>
            {metadata.companies?.map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>

          <select
            value={minExp}
            onChange={(e) => setMinExp(Number(e.target.value))}
            className="bg-slate-800 border border-slate-700 rounded-xl px-3 py-1.5 text-xs text-white outline-none focus:border-indigo-500"
          >
            <option value={0}>Any Experience</option>
            <option value={5}>5+ Years</option>
            <option value={8}>8+ Years</option>
            <option value={10}>10+ Years</option>
          </select>
        </div>

        <span className="text-xs text-slate-400">
          Showing <strong className="text-white">{results.length}</strong> candidates
        </span>
      </div>

      {/* Results grid */}
      {loading ? (
        <div className="flex justify-center py-16">
          <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {results.map((person, idx) => (
            <div key={idx} className="p-5 bg-slate-800/40 hover:bg-slate-800/80 transition rounded-2xl border border-slate-700/60 flex flex-col justify-between">
              <div>
                <h3 className="text-base font-bold text-white">{person.name}</h3>
                <p className="text-xs text-indigo-400 font-medium mt-0.5">{person.title}</p>

                <div className="mt-3 space-y-1.5 text-xs text-slate-400">
                  <div className="flex items-center space-x-2">
                    <MapPin className="w-3.5 h-3.5 text-slate-500" />
                    <span>{person.location}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Briefcase className="w-3.5 h-3.5 text-slate-500" />
                    <span>{person.years_experience} years professional experience</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Mail className="w-3.5 h-3.5 text-slate-500" />
                    <span>{person.email}</span>
                  </div>
                </div>

                {/* Skills tags */}
                <div className="mt-4">
                  <span className="text-[11px] text-slate-500 font-medium block mb-1">Skills:</span>
                  <div className="flex flex-wrap gap-1">
                    {person.skills?.slice(0, 5).map((s, sIdx) => (
                      <span key={sIdx} className="text-[11px] px-2 py-0.5 rounded bg-slate-700/60 text-slate-300 border border-slate-600/50">
                        {s.name}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              {/* Past Companies */}
              <div className="mt-4 pt-3 border-t border-slate-700/50 text-[11px] text-slate-400">
                <span>Alumni of: </span>
                <span className="text-slate-200">
                  {person.companies?.map((c) => c.name).filter(Boolean).join(', ') || 'Independent'}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}