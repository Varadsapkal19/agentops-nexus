"use client";

import { Zap, Sparkles, TrendingUp } from "lucide-react";

export default function OptimizationsCenter() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-extrabold text-white tracking-tight">Optimization Center</h1>
        <p className="text-sm text-neutral-400 mt-1">Overview of automated configurations, prompt testing, and models routing</p>
      </div>

      <div className="glass-card p-8 rounded-2xl border border-white/5 text-center text-xs text-neutral-500 py-16">
        <Zap className="h-10 w-10 text-neutral-700 mx-auto mb-4" />
        <h3 className="font-bold text-white text-sm mb-2">Automated route testing is active</h3>
        <p className="max-w-md mx-auto mb-6">AgentOps Nexus is dynamically benchmarking prompt versions and routing requests to the cheapest model that satisfies constraints.</p>
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-emerald-500/25 bg-emerald-500/5 text-emerald-400 font-semibold">
          <TrendingUp className="h-3.5 w-3.5" /> Total System Cost Reduced by 24.5%
        </div>
      </div>
    </div>
  );
}
