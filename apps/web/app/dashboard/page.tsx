"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { motion, Variants } from "framer-motion";
import {
  AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, PieChart, Pie, Cell,
} from "recharts";
import {
  Shield, Sparkles, Activity, Cpu, ArrowUpRight, BarChart3,
  Database, TrendingUp, TrendingDown, Zap, Clock, AlertTriangle,
} from "lucide-react";
import {
  StatCard, GlassPanel, SectionHeader, StatusBadge, SeverityBadge, ProgressRing,
} from "@/components/ui/nexus-components";

/* ─── Mock Data ─── */
const tokenData = [
  { day: "Mon", tokens: 124000, cost: 31.2 },
  { day: "Tue", tokens: 98000, cost: 24.5 },
  { day: "Wed", tokens: 156000, cost: 39.0 },
  { day: "Thu", tokens: 142000, cost: 35.5 },
  { day: "Fri", tokens: 189000, cost: 47.2 },
  { day: "Sat", tokens: 67000, cost: 16.7 },
  { day: "Sun", tokens: 45000, cost: 11.2 },
];

const modelDistribution = [
  { name: "GPT-4o", value: 42, color: "#6366f1" },
  { name: "Claude 3.5", value: 28, color: "#8b5cf6" },
  { name: "GPT-4o Mini", value: 18, color: "#06b6d4" },
  { name: "Gemini 1.5", value: 12, color: "#10b981" },
];

const qualityTrend = [
  { hour: "00:00", score: 92.1 },
  { hour: "04:00", score: 94.5 },
  { hour: "08:00", score: 93.8 },
  { hour: "12:00", score: 95.2 },
  { hour: "16:00", score: 94.9 },
  { hour: "20:00", score: 96.1 },
  { hour: "Now", score: 94.2 },
];

const recentRuns = [
  { id: "run-4821", agent: "Supervisor", model: "gpt-4o", tokens: 2840, latency: "1.2s", quality: 98, status: "active" as const, time: "12s ago" },
  { id: "run-4820", agent: "Safety Shield", model: "gpt-4o", tokens: 1205, latency: "0.8s", quality: 100, status: "active" as const, time: "34s ago" },
  { id: "run-4819", agent: "Cost Analyzer", model: "gpt-4o-mini", tokens: 890, latency: "0.4s", quality: 95, status: "active" as const, time: "1m ago" },
  { id: "run-4818", agent: "Lead Router", model: "claude-3.5", tokens: 3200, latency: "1.8s", quality: 72, status: "blocked" as const, time: "3m ago" },
  { id: "run-4817", agent: "Quality Agent", model: "gpt-4o-mini", tokens: 420, latency: "0.3s", quality: 97, status: "active" as const, time: "5m ago" },
];

const incidents = [
  { id: "INC-104", agent: "Customer Success Bot", issue: "Hallucination detected in product pricing response", time: "14 min ago", status: "blocked" as const, severity: "high" as const },
  { id: "INC-103", agent: "Billing Evaluator", issue: "Monthly budget threshold exceeded (92% utilized)", time: "2h ago", status: "resolved" as const, severity: "medium" as const },
  { id: "INC-102", agent: "Lead Router Agent", issue: "Upstream API timeout after 30s — 3 retries failed", time: "1d ago", status: "resolved" as const, severity: "high" as const },
];

/* ─── Custom Tooltip ─── */
function ChartTooltip({ active, payload, label }: any) {
  if (!active || !payload?.length) return null;
  return (
    <div className="rounded-lg border border-white/10 bg-neutral-900/95 px-3 py-2 shadow-xl backdrop-blur-sm">
      <p className="text-[10px] font-semibold text-neutral-400 mb-1">{label}</p>
      {payload.map((p: any, i: number) => (
        <p key={i} className="text-xs font-bold" style={{ color: p.color }}>
          {p.name}: {typeof p.value === "number" && p.name.toLowerCase().includes("cost") ? `$${p.value.toFixed(2)}` : p.value.toLocaleString()}
        </p>
      ))}
    </div>
  );
}



/* ─── Stagger Animation ─── */
const container: Variants = {
  hidden: { opacity: 0 },
  show: { opacity: 1, transition: { staggerChildren: 0.08 } },
};
const item: Variants = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { duration: 0.5 } },
};

/* ─── Live Clock ─── */
function LiveClock() {
  const [time, setTime] = useState("");
  useEffect(() => {
    const tick = () => setTime(new Date().toLocaleTimeString("en-US", { hour12: false }));
    tick();
    const id = setInterval(tick, 1000);
    return () => clearInterval(id);
  }, []);
  return <span className="font-mono text-xs tabular-nums text-neutral-500">{time}</span>;
}

/* ─── Page ─── */
export default function DashboardOverview() {
  return (
    <motion.div variants={container} initial="hidden" animate="show" className="space-y-8">
      {/* ── Header ── */}
      <motion.div variants={item} className="flex items-end justify-between">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight text-white">
            Nexus Control Center
          </h1>
          <p className="mt-1 text-sm text-neutral-500">
            Real-time overview of your enterprise AI agent ecosystem
          </p>
        </div>
        <div className="flex items-center gap-4">
          <LiveClock />
          <div className="inline-flex items-center gap-2 rounded-full border border-indigo-500/25 bg-indigo-500/5 px-3 py-1.5 text-[11px] font-semibold text-indigo-400">
            <Sparkles className="h-3 w-3 animate-pulse" />
            Supervisor Online
          </div>
        </div>
      </motion.div>

      {/* ── Stat Cards ── */}
      <motion.div variants={item} className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard title="Active Agents" value={13} suffix=" / 15" change="+2 this week" changeType="positive" icon={Cpu} accentColor="indigo" />
        <StatCard title="Today's Cost" value={187} prefix="$" suffix=".50" change="−12% vs yesterday" changeType="positive" icon={TrendingDown} accentColor="emerald" />
        <StatCard title="Safety Blocks" value={3} change="0 active violations" changeType="neutral" icon={Shield} accentColor="pink" />
        <StatCard title="Avg Quality" value={94} suffix=".2%" change="+1.4% improvement" changeType="positive" icon={Activity} accentColor="cyan" />
      </motion.div>

      {/* ── Charts Row ── */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* Token & Cost Area Chart */}
        <motion.div variants={item}>
          <GlassPanel className="p-6 lg:col-span-2">
            <SectionHeader
              title="Token Usage & Costs"
              subtitle="Last 7 days"
              action={
                <div className="flex gap-3 text-[10px] font-semibold">
                  <span className="flex items-center gap-1.5 text-indigo-400">
                    <span className="h-2 w-2 rounded-full bg-indigo-500" /> Tokens
                  </span>
                  <span className="flex items-center gap-1.5 text-emerald-400">
                    <span className="h-2 w-2 rounded-full bg-emerald-500" /> Cost
                  </span>
                </div>
              }
            />
            <ResponsiveContainer width="100%" height={240}>
              <AreaChart data={tokenData} margin={{ top: 5, right: 5, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="tokenGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#6366f1" stopOpacity={0.3} />
                    <stop offset="100%" stopColor="#6366f1" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="costGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#10b981" stopOpacity={0.3} />
                    <stop offset="100%" stopColor="#10b981" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
                <XAxis dataKey="day" tick={{ fontSize: 10, fill: "#71717a" }} axisLine={false} tickLine={false} />
                <YAxis yAxisId="tokens" tick={{ fontSize: 10, fill: "#71717a" }} axisLine={false} tickLine={false} tickFormatter={(v) => `${(v / 1000).toFixed(0)}k`} />
                <YAxis yAxisId="cost" orientation="right" tick={{ fontSize: 10, fill: "#71717a" }} axisLine={false} tickLine={false} tickFormatter={(v) => `$${v}`} />
                <Tooltip content={<ChartTooltip />} />
                <Area yAxisId="tokens" type="monotone" dataKey="tokens" stroke="#6366f1" strokeWidth={2} fill="url(#tokenGrad)" name="Tokens" />
                <Area yAxisId="cost" type="monotone" dataKey="cost" stroke="#10b981" strokeWidth={2} fill="url(#costGrad)" name="Cost" />
              </AreaChart>
            </ResponsiveContainer>
          </GlassPanel>
        </motion.div>

        {/* Model Distribution */}
        <motion.div variants={item}>
          <GlassPanel className="p-6">
            <SectionHeader title="Model Distribution" subtitle="By request volume" />
            <div className="flex items-center justify-center">
              <ResponsiveContainer width="100%" height={180}>
                <PieChart>
                  <Pie
                    data={modelDistribution}
                    cx="50%"
                    cy="50%"
                    innerRadius={50}
                    outerRadius={75}
                    dataKey="value"
                    stroke="none"
                  >
                    {modelDistribution.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip content={<ChartTooltip />} />
                </PieChart>
              </ResponsiveContainer>
            </div>
            <div className="mt-2 grid grid-cols-2 gap-2">
              {modelDistribution.map((m) => (
                <div key={m.name} className="flex items-center gap-2 text-[10px]">
                  <span className="h-2 w-2 rounded-full" style={{ backgroundColor: m.color }} />
                  <span className="text-neutral-400">{m.name}</span>
                  <span className="ml-auto font-bold text-white">{m.value}%</span>
                </div>
              ))}
            </div>
          </GlassPanel>
        </motion.div>
      </div>

      {/* ── Quality Trend + Health Rings ── */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* Quality Line Chart */}
        <motion.div variants={item} className="lg:col-span-2">
          <GlassPanel className="p-6">
            <SectionHeader title="Quality Score Trend" subtitle="24-hour rolling average" />
            <ResponsiveContainer width="100%" height={200}>
              <AreaChart data={qualityTrend} margin={{ top: 5, right: 5, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="qualGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#06b6d4" stopOpacity={0.25} />
                    <stop offset="100%" stopColor="#06b6d4" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
                <XAxis dataKey="hour" tick={{ fontSize: 10, fill: "#71717a" }} axisLine={false} tickLine={false} />
                <YAxis domain={[88, 100]} tick={{ fontSize: 10, fill: "#71717a" }} axisLine={false} tickLine={false} tickFormatter={(v) => `${v}%`} />
                <Tooltip content={<ChartTooltip />} />
                <Area type="monotone" dataKey="score" stroke="#06b6d4" strokeWidth={2.5} fill="url(#qualGrad)" name="Quality Score" />
              </AreaChart>
            </ResponsiveContainer>
          </GlassPanel>
        </motion.div>

        {/* Health Rings */}
        <motion.div variants={item}>
          <GlassPanel className="p-6">
            <SectionHeader title="System Health" />
            <div className="grid grid-cols-2 gap-6 mt-2">
              <ProgressRing value={98} color="#10b981" label="Uptime" />
              <ProgressRing value={37} color="#6366f1" label="Budget Used" />
              <ProgressRing value={94} color="#06b6d4" label="Quality" />
              <ProgressRing value={100} color="#8b5cf6" label="Safety" />
            </div>
          </GlassPanel>
        </motion.div>
      </div>

      {/* ── Recent Agent Runs ── */}
      <motion.div variants={item}>
        <GlassPanel className="p-6">
          <SectionHeader
            title="Live Agent Execution Feed"
            subtitle="Last 5 runs across all agents"
            action={
              <div className="flex items-center gap-1.5 text-[10px] font-semibold text-emerald-400">
                <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse" />
                Streaming
              </div>
            }
          />
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-white/5 text-[10px] font-semibold uppercase tracking-wider text-neutral-600">
                  <th className="pb-3 pr-4">Run ID</th>
                  <th className="pb-3 pr-4">Agent</th>
                  <th className="pb-3 pr-4">Model</th>
                  <th className="pb-3 pr-4 text-right">Tokens</th>
                  <th className="pb-3 pr-4 text-right">Latency</th>
                  <th className="pb-3 pr-4 text-right">Quality</th>
                  <th className="pb-3 pr-4">Status</th>
                  <th className="pb-3 text-right">When</th>
                </tr>
              </thead>
              <tbody>
                {recentRuns.map((run) => (
                  <tr key={run.id} className="border-b border-white/[0.03] transition hover:bg-white/[0.015]">
                    <td className="py-3.5 pr-4 font-mono text-neutral-500">{run.id}</td>
                    <td className="py-3.5 pr-4 font-medium text-white">{run.agent}</td>
                    <td className="py-3.5 pr-4 text-neutral-400">{run.model}</td>
                    <td className="py-3.5 pr-4 text-right tabular-nums text-neutral-300">{run.tokens.toLocaleString()}</td>
                    <td className="py-3.5 pr-4 text-right tabular-nums text-neutral-400">{run.latency}</td>
                    <td className="py-3.5 pr-4 text-right">
                      <span className={run.quality >= 90 ? "text-emerald-400 font-semibold" : "text-amber-400 font-semibold"}>
                        {run.quality}%
                      </span>
                    </td>
                    <td className="py-3.5 pr-4"><StatusBadge status={run.status} /></td>
                    <td className="py-3.5 text-right text-neutral-600">{run.time}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </GlassPanel>
      </motion.div>

      {/* ── Incidents ── */}
      <motion.div variants={item}>
        <GlassPanel className="p-6">
          <SectionHeader
            title="Active Incidents & Governance Log"
            action={
              <Link href="/dashboard/alerts" className="flex items-center gap-1 text-[11px] font-semibold text-indigo-400 transition hover:text-indigo-300">
                View All <ArrowUpRight className="h-3 w-3" />
              </Link>
            }
          />
          <div className="space-y-3">
            {incidents.map((inc) => (
              <div key={inc.id} className="flex items-center justify-between rounded-xl border border-white/[0.04] bg-white/[0.01] p-4 transition hover:border-white/[0.08] hover:bg-white/[0.025]">
                <div className="flex items-start gap-3">
                  <div className={`mt-0.5 flex h-8 w-8 items-center justify-center rounded-lg ${inc.status === "blocked" ? "bg-pink-500/10 text-pink-400" : "bg-neutral-800 text-neutral-500"}`}>
                    <AlertTriangle className="h-4 w-4" />
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="text-[10px] font-mono text-neutral-600">{inc.id}</span>
                      <SeverityBadge severity={inc.severity} />
                    </div>
                    <p className="mt-1 text-sm font-medium text-white">{inc.issue}</p>
                    <p className="mt-0.5 text-[10px] text-neutral-600">
                      Agent: <span className="text-neutral-400">{inc.agent}</span> · {inc.time}
                    </p>
                  </div>
                </div>
                <StatusBadge status={inc.status} />
              </div>
            ))}
          </div>
        </GlassPanel>
      </motion.div>
    </motion.div>
  );
}
