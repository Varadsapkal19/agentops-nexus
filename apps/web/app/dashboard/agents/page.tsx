"use client";

import { useState } from "react";
import { motion, Variants } from "framer-motion";
import {
  Cpu, Play, Pause, Edit, Sliders, ExternalLink,
  Sparkles, Clock, Gauge, ArrowUpRight,
} from "lucide-react";
import { GlassPanel, StatusBadge, ProgressRing } from "@/components/ui/nexus-components";

interface Agent {
  id: string;
  name: string;
  type: string;
  status: "active" | "paused" | "error";
  model: string;
  successRate: number;
  avgLatency: string;
  totalRuns: number;
  tokensCost: string;
  lastRun: string;
  uptime: string;
}

const agentsData: Agent[] = [
  { id: "sup-001", name: "Supervisor Agent", type: "orchestrator", status: "active", model: "gpt-4o", successRate: 100, avgLatency: "1.2s", totalRuns: 4821, tokensCost: "$298.20", lastRun: "12s ago", uptime: "99.99%" },
  { id: "saf-002", name: "Shield Content Validator", type: "safety", status: "active", model: "gpt-4o", successRate: 100, avgLatency: "0.8s", totalRuns: 3204, tokensCost: "$245.80", lastRun: "34s ago", uptime: "99.99%" },
  { id: "cst-003", name: "Customer Success Bot", type: "support", status: "active", model: "gpt-4o", successRate: 98.2, avgLatency: "1.8s", totalRuns: 8920, tokensCost: "$482.30", lastRun: "2m ago", uptime: "99.95%" },
  { id: "led-004", name: "Lead Router Agent", type: "routing", status: "paused", model: "claude-3.5-sonnet", successRate: 95.4, avgLatency: "2.1s", totalRuns: 5610, tokensCost: "$341.50", lastRun: "15m ago", uptime: "98.20%" },
  { id: "bil-005", name: "Billing Evaluator", type: "cost_governance", status: "active", model: "gpt-4o-mini", successRate: 99.1, avgLatency: "0.4s", totalRuns: 2450, tokensCost: "$87.40", lastRun: "5m ago", uptime: "99.98%" },
  { id: "qua-006", name: "Quality Agent", type: "quality", status: "active", model: "gpt-4o-mini", successRate: 97.8, avgLatency: "0.3s", totalRuns: 1890, tokensCost: "$42.10", lastRun: "1m ago", uptime: "99.97%" },
];

const stagger: Variants = { hidden: { opacity: 0 }, show: { opacity: 1, transition: { staggerChildren: 0.07 } } };
const fade: Variants = { hidden: { opacity: 0, y: 16 }, show: { opacity: 1, y: 0, transition: { duration: 0.4 } } };

export default function AgentMonitor() {
  const [agents, setAgents] = useState(agentsData);

  const toggleAgent = (id: string) => {
    setAgents(agents.map((a) =>
      a.id === id ? { ...a, status: a.status === "active" ? "paused" : "active" } as Agent : a
    ));
  };

  const activeCount = agents.filter((a) => a.status === "active").length;

  return (
    <motion.div variants={stagger} initial="hidden" animate="show" className="space-y-8">
      <motion.div variants={fade} className="flex items-end justify-between">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight text-white">Agent Monitoring Console</h1>
          <p className="mt-1 text-sm text-neutral-500">Configure, monitor, and control running agents in real-time</p>
        </div>
        <div className="flex items-center gap-3">
          <div className="text-right text-xs">
            <p className="font-bold text-white">{activeCount} of {agents.length} active</p>
            <p className="text-neutral-600">Total runs: {agents.reduce((s, a) => s + a.totalRuns, 0).toLocaleString()}</p>
          </div>
        </div>
      </motion.div>

      <motion.div variants={fade} className="grid grid-cols-1 gap-5 md:grid-cols-2 xl:grid-cols-3">
        {agents.map((agent) => (
          <GlassPanel key={agent.id} className="p-0 overflow-hidden">
            {/* Header */}
            <div className="flex items-center justify-between border-b border-white/[0.04] px-5 py-4">
              <div className="flex items-center gap-3">
                <div className={`flex h-10 w-10 items-center justify-center rounded-xl border ${
                  agent.status === "active"
                    ? "border-indigo-500/20 bg-indigo-500/10 text-indigo-400"
                    : "border-neutral-700 bg-neutral-800 text-neutral-500"
                }`}>
                  <Cpu className="h-5 w-5" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-white">{agent.name}</h3>
                  <p className="text-[10px] font-mono text-neutral-600">{agent.id} · {agent.type}</p>
                </div>
              </div>
              <StatusBadge status={agent.status} />
            </div>

            {/* Metrics Grid */}
            <div className="grid grid-cols-3 divide-x divide-white/[0.04] border-b border-white/[0.04]">
              <div className="px-4 py-3 text-center">
                <p className="text-[9px] font-semibold uppercase tracking-wider text-neutral-600">Model</p>
                <p className="mt-1 text-[11px] font-bold text-white truncate">{agent.model}</p>
              </div>
              <div className="px-4 py-3 text-center">
                <p className="text-[9px] font-semibold uppercase tracking-wider text-neutral-600">Success</p>
                <p className={`mt-1 text-[11px] font-bold ${agent.successRate >= 98 ? "text-emerald-400" : agent.successRate >= 95 ? "text-amber-400" : "text-red-400"}`}>
                  {agent.successRate}%
                </p>
              </div>
              <div className="px-4 py-3 text-center">
                <p className="text-[9px] font-semibold uppercase tracking-wider text-neutral-600">Latency</p>
                <p className="mt-1 text-[11px] font-bold text-white">{agent.avgLatency}</p>
              </div>
            </div>

            {/* Details */}
            <div className="space-y-2 px-5 py-4 text-[11px]">
              <div className="flex justify-between">
                <span className="text-neutral-600">Total Runs</span>
                <span className="font-semibold text-neutral-300 tabular-nums">{agent.totalRuns.toLocaleString()}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-neutral-600">Accumulated Cost</span>
                <span className="font-semibold text-neutral-300">{agent.tokensCost}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-neutral-600">Uptime</span>
                <span className="font-semibold text-emerald-400">{agent.uptime}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-neutral-600">Last Run</span>
                <span className="text-neutral-500">{agent.lastRun}</span>
              </div>
            </div>

            {/* Actions */}
            <div className="flex items-center justify-between border-t border-white/[0.04] px-5 py-3">
              <div className="flex gap-2">
                <button className="flex items-center gap-1.5 rounded-lg border border-white/[0.06] px-3 py-1.5 text-[10px] font-semibold text-neutral-400 transition hover:border-white/[0.12] hover:bg-white/[0.03] hover:text-white">
                  <Edit className="h-3 w-3" /> Prompt
                </button>
                <button className="flex items-center gap-1.5 rounded-lg border border-white/[0.06] px-3 py-1.5 text-[10px] font-semibold text-neutral-400 transition hover:border-white/[0.12] hover:bg-white/[0.03] hover:text-white">
                  <Sliders className="h-3 w-3" /> Config
                </button>
              </div>
              <button
                onClick={() => toggleAgent(agent.id)}
                className={`flex h-8 w-8 items-center justify-center rounded-lg transition ${
                  agent.status === "active"
                    ? "bg-amber-500/10 text-amber-400 hover:bg-amber-500/20"
                    : "bg-emerald-500/10 text-emerald-400 hover:bg-emerald-500/20"
                }`}
              >
                {agent.status === "active" ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
              </button>
            </div>
          </GlassPanel>
        ))}
      </motion.div>
    </motion.div>
  );
}
