"use client";

import { motion, Variants } from "framer-motion";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, AreaChart, Area, Cell,
} from "recharts";
import { DollarSign, TrendingDown, AlertCircle, Zap, ArrowDown } from "lucide-react";
import { StatCard, GlassPanel, SectionHeader, ProgressRing } from "@/components/ui/nexus-components";

const dailyCosts = [
  { day: "Mon", gpt4o: 42, claude: 28, mini: 8, gemini: 5 },
  { day: "Tue", gpt4o: 38, claude: 22, mini: 12, gemini: 4 },
  { day: "Wed", gpt4o: 55, claude: 31, mini: 9, gemini: 7 },
  { day: "Thu", gpt4o: 48, claude: 26, mini: 11, gemini: 6 },
  { day: "Fri", gpt4o: 62, claude: 35, mini: 14, gemini: 8 },
  { day: "Sat", gpt4o: 22, claude: 12, mini: 5, gemini: 2 },
  { day: "Sun", gpt4o: 15, claude: 8, mini: 3, gemini: 1 },
];

const forecast = [
  { week: "W1", actual: 620, forecast: 600 },
  { week: "W2", actual: 580, forecast: 610 },
  { week: "W3", actual: 710, forecast: 640 },
  { week: "W4", actual: null, forecast: 660 },
];

const topAgentCosts = [
  { name: "Customer Success Bot", model: "gpt-4o", cost: 482.30, tokens: 1920000, pct: 26.2 },
  { name: "Lead Router Agent", model: "claude-3.5", cost: 341.50, tokens: 1140000, pct: 18.5 },
  { name: "Supervisor Agent", model: "gpt-4o", cost: 298.20, tokens: 1190000, pct: 16.2 },
  { name: "Safety Shield", model: "gpt-4o", cost: 245.80, tokens: 983000, pct: 13.3 },
  { name: "Billing Evaluator", model: "gpt-4o-mini", cost: 87.40, tokens: 583000, pct: 4.7 },
];

function ChartTooltip({ active, payload, label }: any) {
  if (!active || !payload?.length) return null;
  return (
    <div className="rounded-lg border border-white/10 bg-neutral-900/95 px-3 py-2 shadow-xl backdrop-blur-sm">
      <p className="text-[10px] font-semibold text-neutral-400 mb-1">{label}</p>
      {payload.map((p: any, i: number) => (
        <p key={i} className="text-xs font-bold" style={{ color: p.color }}>
          {p.name}: ${typeof p.value === "number" ? p.value.toFixed(2) : p.value}
        </p>
      ))}
    </div>
  );
}



const stagger: Variants = { hidden: { opacity: 0 }, show: { opacity: 1, transition: { staggerChildren: 0.06 } } };
const fade: Variants = { hidden: { opacity: 0, y: 16 }, show: { opacity: 1, y: 0, transition: { duration: 0.4 } } };

export default function CostGovernance() {
  return (
    <motion.div variants={stagger} initial="hidden" animate="show" className="space-y-8">
      <motion.div variants={fade}>
        <h1 className="text-3xl font-extrabold tracking-tight text-white">AI Cost Governance</h1>
        <p className="mt-1 text-sm text-neutral-500">Budget monitoring, spend forecasting, and model optimization recommendations</p>
      </motion.div>

      <motion.div variants={fade} className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard title="Monthly Spend" value={1842} prefix="$" suffix=".30" change="Within budget" changeType="positive" icon={DollarSign} accentColor="indigo" />
        <StatCard title="Budget Cap" value={2500} prefix="$" change="Resets Nov 1st" changeType="neutral" icon={AlertCircle} accentColor="amber" />
        <StatCard title="Savings This Month" value={340} prefix="+$" suffix=".50" change="Via model routing" changeType="positive" icon={TrendingDown} accentColor="emerald" />
        <StatCard title="Cost per Run" value={0} prefix="$" suffix="0.14" change="−8% vs last month" changeType="positive" icon={Zap} accentColor="violet" />
      </motion.div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <motion.div variants={fade} className="lg:col-span-2">
          <GlassPanel className="p-6">
            <SectionHeader
              title="Daily Spend by Model"
              subtitle="Stacked breakdown — last 7 days"
              action={
                <div className="flex gap-3 text-[10px] font-semibold">
                  <span className="flex items-center gap-1.5 text-indigo-400"><span className="h-2 w-2 rounded-full bg-indigo-500" /> GPT-4o</span>
                  <span className="flex items-center gap-1.5 text-violet-400"><span className="h-2 w-2 rounded-full bg-violet-500" /> Claude</span>
                  <span className="flex items-center gap-1.5 text-cyan-400"><span className="h-2 w-2 rounded-full bg-cyan-500" /> Mini</span>
                  <span className="flex items-center gap-1.5 text-emerald-400"><span className="h-2 w-2 rounded-full bg-emerald-500" /> Gemini</span>
                </div>
              }
            />
            <ResponsiveContainer width="100%" height={260}>
              <BarChart data={dailyCosts} margin={{ top: 5, right: 5, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
                <XAxis dataKey="day" tick={{ fontSize: 10, fill: "#71717a" }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fontSize: 10, fill: "#71717a" }} axisLine={false} tickLine={false} tickFormatter={(v) => `$${v}`} />
                <Tooltip content={<ChartTooltip />} />
                <Bar dataKey="gpt4o" stackId="a" fill="#6366f1" radius={[0, 0, 0, 0]} name="GPT-4o" />
                <Bar dataKey="claude" stackId="a" fill="#8b5cf6" name="Claude" />
                <Bar dataKey="mini" stackId="a" fill="#06b6d4" name="Mini" />
                <Bar dataKey="gemini" stackId="a" fill="#10b981" radius={[4, 4, 0, 0]} name="Gemini" />
              </BarChart>
            </ResponsiveContainer>
          </GlassPanel>
        </motion.div>

        <motion.div variants={fade}>
          <GlassPanel className="p-6">
            <SectionHeader title="Budget Utilization" />
            <div className="flex flex-col items-center gap-6 mt-2">
              <ProgressRing value={73} size={120} strokeWidth={8} color="#6366f1" label="73% of $2,500" />
              <div className="w-full space-y-3 text-xs">
                <div className="flex justify-between border-b border-white/5 pb-2">
                  <span className="text-neutral-500">Remaining</span>
                  <span className="font-bold text-emerald-400">$657.70</span>
                </div>
                <div className="flex justify-between border-b border-white/5 pb-2">
                  <span className="text-neutral-500">Daily Avg</span>
                  <span className="font-bold text-white">$61.41</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-neutral-500">Projected EOM</span>
                  <span className="font-bold text-amber-400">$2,340</span>
                </div>
              </div>
            </div>
          </GlassPanel>
        </motion.div>
      </div>

      <motion.div variants={fade}>
        <GlassPanel className="p-6">
          <SectionHeader title="Top Agent Costs" subtitle="Highest spending agents this billing cycle" />
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-white/5 text-[10px] font-semibold uppercase tracking-wider text-neutral-600">
                  <th className="pb-3 pr-4">Agent</th>
                  <th className="pb-3 pr-4">Model</th>
                  <th className="pb-3 pr-4 text-right">Total Cost</th>
                  <th className="pb-3 pr-4 text-right">Tokens</th>
                  <th className="pb-3 pr-4 text-right">% of Budget</th>
                  <th className="pb-3">Spend Bar</th>
                </tr>
              </thead>
              <tbody>
                {topAgentCosts.map((a) => (
                  <tr key={a.name} className="border-b border-white/[0.03] transition hover:bg-white/[0.015]">
                    <td className="py-3.5 pr-4 font-medium text-white">{a.name}</td>
                    <td className="py-3.5 pr-4 text-neutral-400">{a.model}</td>
                    <td className="py-3.5 pr-4 text-right font-bold tabular-nums text-white">${a.cost.toFixed(2)}</td>
                    <td className="py-3.5 pr-4 text-right tabular-nums text-neutral-400">{(a.tokens / 1000).toFixed(0)}k</td>
                    <td className="py-3.5 pr-4 text-right tabular-nums text-neutral-300">{a.pct}%</td>
                    <td className="py-3.5">
                      <div className="h-1.5 w-full rounded-full bg-white/5">
                        <div className="h-full rounded-full bg-indigo-500 transition-all duration-700" style={{ width: `${Math.min(a.pct * 3, 100)}%` }} />
                      </div>
                    </td>
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
