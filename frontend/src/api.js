const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

export async function fetchHealth() {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error('Failed to fetch system health');
  return res.json();
}

export async function fetchMetadata() {
  const res = await fetch(`${API_BASE}/graph/metadata`);
  if (!res.ok) throw new Error('Failed to fetch metadata');
  return res.json();
}

export async function searchTalent({ skill, company, minExperience }) {
  const params = new URLSearchParams();
  if (skill) params.append('skill', skill);
  if (company) params.append('company', company);
  if (minExperience) params.append('min_experience', minExperience);

  const res = await fetch(`${API_BASE}/talent/search?${params.toString()}`);
  if (!res.ok) throw new Error('Failed to search talent');
  return res.json();
}

export async function fetchWarmIntroductions(referrer, targetSkill, maxHops = 2) {
  const params = new URLSearchParams({
    referrer,
    target_skill: targetSkill,
    max_hops: maxHops,
  });
  const res = await fetch(`${API_BASE}/talent/warm-introductions?${params.toString()}`);
  if (!res.ok) throw new Error('Failed to fetch warm introductions');
  return res.json();
}

export async function fetchProjectMatchmaker(projectName) {
  const params = new URLSearchParams({ project_name: projectName });
  const res = await fetch(`${API_BASE}/talent/project-matchmaker?${params.toString()}`);
  if (!res.ok) throw new Error('Failed to fetch project matches');
  return res.json();
}

export async function fetchGraphSnapshot(limit = 120) {
  const res = await fetch(`${API_BASE}/graph/snapshot?limit=${limit}`);
  if (!res.ok) throw new Error('Failed to load graph visualizer');
  return res.json();
}