"use client";

import { useState } from "react";
import { motion, Variants } from "framer-motion";
import { Database, Search, Cpu, HardDrive, Layers, RefreshCw, Key, Shield } from "lucide-react";
import { StatCard, GlassPanel, SectionHeader, StatusBadge } from "@/components/ui/nexus-components";

const stagger: Variants = { hidden: { opacity: 0 }, show: { opacity: 1, transition: { staggerChildren: 0.06 } } };
const fade: Variants = { hidden: { opacity: 0, y: 16 }, show: { opacity: 1, y: 0, transition: { duration: 0.4 } } };

const collections = [
  { name: "agent_memories", vectors: 48210, dimensions: 3072, metric: "Cosine", size: "142 MB" },
  { name: "hallucinations", vectors: 1240, dimensions: 3072, metric: "Cosine", size: "12 MB" },
  { name: "prompt_templates", vectors: 580, dimensions: 1536, metric: "Euclidean", size: "4 MB" },
  { name: "knowledge_documents", vectors: 124000, dimensions: 3072, metric: "Cosine", size: "410 MB" },
  { name: "safety_incidents", vectors: 3400, dimensions: 1536, metric: "Dot Product", size: "28 MB" },
  { name: "agent_evaluations", vectors: 18900, dimensions: 3072, metric: "Cosine", size: "64 MB" },
];

export default function MemoryQdrant() {
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [searching, setSearching] = useState(false);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;
    setSearching(true);
    setTimeout(() => {
      setSearchResults([
        { id: "point-8491", collection: "agent_memories", score: 0.942, payload: { agent: "Customer Success Bot", text: "Customer requested pricing discount details for enterprise plan" } },
        { id: "point-8490", collection: "knowledge_documents", score: 0.891, payload: { source: "SLA_Policy_2026.pdf", chunk: "99.9% uptime guaranteed for high availability tier" } },
        { id: "point-8489", collection: "hallucinations", score: 0.812, payload: { agent: "Lead Router Agent", flag: "Fabricated refund SLA term (>90 days)" } },
      ]);
      setSearching(false);
    }, 500);
  };

  return (
    <motion.div variants={stagger} initial="hidden" animate="show" className="space-y-8">
      <motion.div variants={fade} className="flex items-end justify-between">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight text-white">Vector Memory & Qdrant Engine</h1>
          <p className="mt-1 text-sm text-neutral-500">Inspect vector embeddings, payload search, and Qdrant collection memory</p>
        </div>
        <div className="flex items-center gap-2 rounded-full border border-purple-500/20 bg-purple-500/10 px-3 py-1.5 text-xs font-semibold text-purple-400">
          <Database className="h-4 w-4" /> Qdrant Cluster Connected (v1.11)
        </div>
      </motion.div>

      <motion.div variants={fade} className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard title="Total Vector Points" value={196330} change="+12.4k vectors today" changeType="positive" icon={Database} accentColor="purple" />
        <StatCard title="Active Collections" value={9} change="100% indexed" changeType="positive" icon={Layers} accentColor="indigo" />
        <StatCard title="Vector Storage" value={660} suffix=" MB" change="Optimized memory" changeType="neutral" icon={HardDrive} accentColor="cyan" />
        <StatCard title="Search Latency" value={4} suffix="ms" change="p99 HNSW search" changeType="positive" icon={RefreshCw} accentColor="emerald" />
      </motion.div>

      {/* Vector Search Playground */}
      <motion.div variants={fade}>
        <GlassPanel className="p-6">
          <SectionHeader title="Semantic Vector Search Playground" subtitle="Query Qdrant collections using text embeddings" />
          <form onSubmit={handleSearch} className="flex gap-3">
            <div className="relative flex-1">
              <Search className="absolute left-3.5 top-3.5 h-4 w-4 text-neutral-500" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Enter query string to generate embedding & search cosine similarity..."
                className="w-full rounded-xl border border-white/10 bg-neutral-900/60 pl-10 pr-4 py-3 text-xs text-white outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
              />
            </div>
            <button
              type="submit"
              disabled={searching}
              className="rounded-xl bg-indigo-600 px-6 py-3 text-xs font-bold text-white shadow-lg shadow-indigo-600/30 transition hover:bg-indigo-500 disabled:opacity-50"
            >
              {searching ? "Searching..." : "Vector Search"}
            </button>
          </form>

          {searchResults.length > 0 && (
            <div className="mt-6 space-y-3">
              <p className="text-[10px] font-semibold uppercase tracking-wider text-neutral-500">Top Semantic Matches</p>
              {searchResults.map((res) => (
                <div key={res.id} className="rounded-xl border border-white/[0.04] bg-white/[0.01] p-4 text-xs transition hover:border-white/[0.08]">
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-mono text-[10px] text-neutral-500">{res.id} · <span className="text-purple-400">{res.collection}</span></span>
                    <span className="rounded-full bg-emerald-500/10 px-2.5 py-0.5 text-[10px] font-bold text-emerald-400">
                      Score: {(res.score * 100).toFixed(1)}%
                    </span>
                  </div>
                  <pre className="overflow-x-auto rounded-lg bg-neutral-950 p-3 text-[11px] font-mono text-neutral-300">
                    {JSON.stringify(res.payload, null, 2)}
                  </pre>
                </div>
              ))}
            </div>
          )}
        </GlassPanel>
      </motion.div>

      {/* Collections Grid */}
      <motion.div variants={fade}>
        <GlassPanel className="p-6">
          <SectionHeader title="Qdrant Collection Status" subtitle="Live index statistics per collection" />
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-white/5 text-[10px] font-semibold uppercase tracking-wider text-neutral-600">
                  <th className="pb-3 pr-4">Collection Name</th>
                  <th className="pb-3 pr-4 text-right">Vector Points</th>
                  <th className="pb-3 pr-4 text-right">Dimensions</th>
                  <th className="pb-3 pr-4">Distance Metric</th>
                  <th className="pb-3 pr-4 text-right">Disk Size</th>
                  <th className="pb-3 text-right">Status</th>
                </tr>
              </thead>
              <tbody>
                {collections.map((c) => (
                  <tr key={c.name} className="border-b border-white/[0.03] transition hover:bg-white/[0.015]">
                    <td className="py-3.5 pr-4 font-mono font-bold text-white">{c.name}</td>
                    <td className="py-3.5 pr-4 text-right tabular-nums text-neutral-300">{c.vectors.toLocaleString()}</td>
                    <td className="py-3.5 pr-4 text-right tabular-nums text-neutral-400">{c.dimensions}</td>
                    <td className="py-3.5 pr-4 text-purple-400 font-semibold">{c.metric}</td>
                    <td className="py-3.5 pr-4 text-right tabular-nums text-neutral-400">{c.size}</td>
                    <td className="py-3.5 text-right"><StatusBadge status="active" label="Indexed" /></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </GlassPanel>
      </motion.div>
    </motion.div>
  );
}
