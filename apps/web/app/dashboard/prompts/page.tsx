"use client";

import { useState } from "react";
import { motion, Variants } from "framer-motion";
import { FileCode, Plus, History, Play, CheckCircle2, Copy, Sparkles } from "lucide-react";
import { GlassPanel, SectionHeader, StatusBadge } from "@/components/ui/nexus-components";

const stagger: Variants = { hidden: { opacity: 0 }, show: { opacity: 1, transition: { staggerChildren: 0.06 } } };
const fade: Variants = { hidden: { opacity: 0, y: 16 }, show: { opacity: 1, y: 0, transition: { duration: 0.4 } } };

const promptTemplates = [
  { id: "prt-01", name: "System Supervisor Instruction", category: "System", version: 3, qualityScore: 98, lastUpdated: "2d ago", variables: ["agent_role", "context_summary"] },
  { id: "prt-02", name: "Customer Support Resolution Prompt", category: "User", version: 5, qualityScore: 94, lastUpdated: "1d ago", variables: ["ticket_id", "user_query", "kb_context"] },
  { id: "prt-03", name: "Safety Shield Content Validator", category: "Safety", version: 2, qualityScore: 99, lastUpdated: "4h ago", variables: ["output_response", "sensitivity"] },
  { id: "prt-04", name: "Billing Discrepancy Evaluation", category: "System", version: 1, qualityScore: 92, lastUpdated: "5d ago", variables: ["account_id", "invoice_data"] },
];

export default function PromptLibrary() {
  const [selectedPrompt, setSelectedPrompt] = useState(promptTemplates[0]);

  return (
    <motion.div variants={stagger} initial="hidden" animate="show" className="space-y-8">
      <motion.div variants={fade} className="flex items-end justify-between">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight text-white">Prompt Engineering Library</h1>
          <p className="mt-1 text-sm text-neutral-500">Version control, variable injection, and prompt performance benchmarking</p>
        </div>
        <button className="flex items-center gap-2 rounded-xl bg-indigo-600 px-4 py-2.5 text-xs font-bold text-white shadow-lg shadow-indigo-600/30 transition hover:bg-indigo-500">
          <Plus className="h-4 w-4" /> Create New Prompt
        </button>
      </motion.div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* Template List */}
        <motion.div variants={fade} className="space-y-3">
          <GlassPanel className="p-4">
            <SectionHeader title="Prompt Catalog" subtitle={`${promptTemplates.length} managed templates`} />
            <div className="space-y-2">
              {promptTemplates.map((p) => (
                <div
                  key={p.id}
                  onClick={() => setSelectedPrompt(p)}
                  className={`cursor-pointer rounded-xl border p-3.5 transition ${
                    selectedPrompt.id === p.id
                      ? "border-indigo-500/40 bg-indigo-500/10 text-white"
                      : "border-white/[0.04] bg-white/[0.01] text-neutral-400 hover:border-white/[0.08] hover:text-white"
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-mono text-neutral-500">{p.id}</span>
                    <span className="rounded bg-indigo-500/10 px-2 py-0.5 text-[9px] font-bold text-indigo-400">
                      v{p.version}
                    </span>
                  </div>
                  <h4 className="mt-1 text-xs font-bold text-white">{p.name}</h4>
                  <div className="mt-2 flex items-center justify-between text-[10px]">
                    <span className="text-neutral-500">Score: <span className="font-bold text-emerald-400">{p.qualityScore}%</span></span>
                    <span className="text-neutral-500">{p.lastUpdated}</span>
                  </div>
                </div>
              ))}
            </div>
          </GlassPanel>
        </motion.div>

        {/* Prompt Editor & Inspection View */}
        <motion.div variants={fade} className="lg:col-span-2">
          <GlassPanel className="p-6">
            <div className="flex items-center justify-between border-b border-white/5 pb-4 mb-6">
              <div>
                <span className="text-[10px] font-mono text-neutral-500">{selectedPrompt.id} · Version {selectedPrompt.version}</span>
                <h3 className="text-base font-bold text-white">{selectedPrompt.name}</h3>
              </div>
              <div className="flex items-center gap-2">
                <button className="flex items-center gap-1.5 rounded-lg border border-white/10 px-3 py-1.5 text-xs font-semibold text-neutral-300 transition hover:bg-white/5">
                  <History className="h-3.5 w-3.5" /> Diff History
                </button>
                <button className="flex items-center gap-1.5 rounded-lg bg-indigo-600 px-3 py-1.5 text-xs font-semibold text-white transition hover:bg-indigo-500">
                  <Play className="h-3.5 w-3.5" /> Test Prompt
                </button>
              </div>
            </div>

            {/* Content Editor */}
            <div className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-neutral-400 mb-2">System Instruction Body</label>
                <textarea
                  rows={8}
                  readOnly
                  className="w-full rounded-xl border border-white/10 bg-neutral-950 p-4 text-xs font-mono text-neutral-200 outline-none leading-relaxed"
                  value={`You are an enterprise AI governance agent. Your primary role is to monitor and optimize multi-agent execution graphs.

Rules:
1. Enforce strict compliance boundaries.
2. If token count exceeds threshold, optimize prompt variables: {{context_summary}}.
3. Evaluate output quality score for role: {{agent_role}}.`}
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-neutral-400 mb-2">Declared Template Variables</label>
                <div className="flex flex-wrap gap-2">
                  {selectedPrompt.variables.map((v) => (
                    <span key={v} className="rounded-lg border border-indigo-500/30 bg-indigo-500/10 px-3 py-1 font-mono text-xs font-bold text-indigo-400">
                      {`{{${v}}}`}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </GlassPanel>
        </motion.div>
      </div>
    </motion.div>
  );
}
