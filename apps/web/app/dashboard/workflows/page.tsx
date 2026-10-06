"use client";

import { motion, Variants } from "framer-motion";
import { Workflow, Play, Plus, GitBranch, ArrowRight, CheckCircle2, Clock, Zap } from "lucide-react";
import { GlassPanel, SectionHeader, StatusBadge } from "@/components/ui/nexus-components";

const stagger: Variants = { hidden: { opacity: 0 }, show: { opacity: 1, transition: { staggerChildren: 0.06 } } };
const fade: Variants = { hidden: { opacity: 0, y: 16 }, show: { opacity: 1, y: 0, transition: { duration: 0.4 } } };

const workflows = [
  { id: "wf-101", name: "Customer Onboarding Chain", steps: 5, trigger: "Webhook Event", status: "active" as const, runs: 1240, avgTime: "2.4s", cost: "$0.04/run" },
  { id: "wf-102", name: "Multi-Model Safety & Audit Routing", steps: 4, trigger: "API Request", status: "active" as const, runs: 4820, avgTime: "1.1s", cost: "$0.02/run" },
  { id: "wf-103", name: "Billing Discrepancy Auto-Resolver", steps: 6, trigger: "Schedule (Hourly)", status: "active" as const, runs: 340, avgTime: "4.8s", cost: "$0.12/run" },
  { id: "wf-104", name: "Nightly Knowledge Base Embedding Sync", steps: 3, trigger: "Cron (00:00 UTC)", status: "paused" as const, runs: 30, avgTime: "45.0s", cost: "$0.85/run" },
];

export default function WorkflowOrchestration() {
  return (
    <motion.div variants={stagger} initial="hidden" animate="show" className="space-y-8">
      <motion.div variants={fade} className="flex items-end justify-between">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight text-white">Multi-Agent Workflows</h1>
          <p className="mt-1 text-sm text-neutral-500">Visual DAG workflow builder, step-level orchestration, and execution routing</p>
        </div>
        <button className="flex items-center gap-2 rounded-xl bg-indigo-600 px-4 py-2.5 text-xs font-bold text-white shadow-lg shadow-indigo-600/30 transition hover:bg-indigo-500">
          <Plus className="h-4 w-4" /> Create Workflow
        </button>
      </motion.div>

      {/* Visual Workflow Canvas Snapshot */}
      <motion.div variants={fade}>
        <GlassPanel className="p-6">
          <SectionHeader title="Active Canvas Snapshot" subtitle="Customer Onboarding Chain (wf-101)" />
          <div className="relative rounded-xl border border-white/[0.06] bg-neutral-950/80 p-8">
            <div className="flex flex-wrap items-center justify-between gap-4">
              {/* Step 1 */}
              <div className="flex items-center gap-3 rounded-xl border border-indigo-500/30 bg-indigo-500/10 p-4">
                <Zap className="h-5 w-5 text-indigo-400" />
                <div>
                  <p className="text-[10px] font-semibold text-indigo-400">Trigger</p>
                  <p className="text-xs font-bold text-white">User Signed Up</p>
                </div>
              </div>
              <ArrowRight className="h-4 w-4 text-neutral-600" />

              {/* Step 2 */}
              <div className="flex items-center gap-3 rounded-xl border border-pink-500/30 bg-pink-500/10 p-4">
                <CheckCircle2 className="h-5 w-5 text-pink-400" />
                <div>
                  <p className="text-[10px] font-semibold text-pink-400">Guardrail</p>
                  <p className="text-xs font-bold text-white">Shield Validation</p>
                </div>
              </div>
              <ArrowRight className="h-4 w-4 text-neutral-600" />

              {/* Step 3 */}
              <div className="flex items-center gap-3 rounded-xl border border-cyan-500/30 bg-cyan-500/10 p-4">
                <GitBranch className="h-5 w-5 text-cyan-400" />
                <div>
                  <p className="text-[10px] font-semibold text-cyan-400">LLM Router</p>
                  <p className="text-xs font-bold text-white">GPT-4o Router</p>
                </div>
              </div>
              <ArrowRight className="h-4 w-4 text-neutral-600" />

              {/* Step 4 */}
              <div className="flex items-center gap-3 rounded-xl border border-emerald-500/30 bg-emerald-500/10 p-4">
                <CheckCircle2 className="h-5 w-5 text-emerald-400" />
                <div>
                  <p className="text-[10px] font-semibold text-emerald-400">Output Action</p>
                  <p className="text-xs font-bold text-white">Send Welcome Digest</p>
                </div>
              </div>
            </div>
          </div>
        </GlassPanel>
      </motion.div>

      {/* Workflows List */}
      <motion.div variants={fade}>
        <GlassPanel className="p-6">
          <SectionHeader title="Configured Workflows" subtitle="Manage and trigger multi-agent DAGs" />
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
            {workflows.map((wf) => (
              <div key={wf.id} className="rounded-xl border border-white/[0.04] bg-white/[0.01] p-5 transition hover:border-white/[0.08]">
                <div className="flex items-start justify-between">
                  <div>
                    <span className="text-[10px] font-mono text-neutral-600">{wf.id}</span>
                    <h4 className="text-sm font-bold text-white mt-0.5">{wf.name}</h4>
                    <p className="text-[11px] text-neutral-500 mt-1">Trigger: {wf.trigger}</p>
                  </div>
                  <StatusBadge status={wf.status} />
                </div>
                <div className="mt-4 grid grid-cols-3 gap-2 border-t border-white/[0.04] pt-3 text-[10px]">
                  <div>
                    <span className="text-neutral-600">Steps</span>
                    <p className="font-bold text-white">{wf.steps} Nodes</p>
                  </div>
                  <div>
                    <span className="text-neutral-600">Total Runs</span>
                    <p className="font-bold text-white">{wf.runs.toLocaleString()}</p>
                  </div>
                  <div>
                    <span className="text-neutral-600">Avg Latency</span>
                    <p className="font-bold text-emerald-400">{wf.avgTime}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </GlassPanel>
      </motion.div>
    </motion.div>
  );
}
