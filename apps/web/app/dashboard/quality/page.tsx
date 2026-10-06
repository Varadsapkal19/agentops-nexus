"use client";

import { motion, Variants } from "framer-motion";
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip } from "recharts";
import { Award, CheckCircle2, AlertTriangle, Sparkles, Activity } from "lucide-react";
import { StatCard, GlassPanel, SectionHeader, ProgressRing } from "@/components/ui/nexus-components";

const stagger: Variants = { hidden: { opacity: 0 }, show: { opacity: 1, transition: { staggerChildren: 0.06 } } };
const fade: Variants = { hidden: { opacity: 0, y: 16 }, show: { opacity: 1, y: 0, transition: { duration: 0.4 } } };

const radarData = [
  { dimension: "Relevance", score: 96 },
  { dimension: "Groundedness", score: 94 },
  { dimension: "Coherence", score: 98 },
  { dimension: "Completeness", score: 92 },
  { dimension: "Accuracy", score: 95 },
  { dimension: "Safety", score: 99 },
];

const agentQualityScores = [
  { name: "Supervisor Agent", relevance: 98, groundedness: 97, accuracy: 99, overall: 98.0 },
  { name: "Shield Content Validator", relevance: 99, groundedness: 99, accuracy: 100, overall: 99.3 },
  { name: "Customer Success Bot", relevance: 94, groundedness: 91, accuracy: 93, overall: 92.6 },
  { name: "Billing Evaluator", relevance: 97, groundedness: 96, accuracy: 98, overall: 97.0 },
  { name: "Lead Router Agent", relevance: 92, groundedness: 89, accuracy: 91, overall: 90.6 },
];

export default function QualityEvaluation() {
  return (
    <motion.div variants={stagger} initial="hidden" animate="show" className="space-y-8">
      <motion.div variants={fade} className="flex items-end justify-between">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight text-white">Quality & Evaluation Engine</h1>
          <p className="mt-1 text-sm text-neutral-500">Multi-dimensional quality scoring, hallucination tracking, and answer relevancy</p>
        </div>
        <div className="flex items-center gap-2 rounded-full border border-cyan-500/20 bg-cyan-500/10 px-3 py-1.5 text-xs font-semibold text-cyan-400">
          <Award className="h-4 w-4" /> Quality Agent Active
        </div>
      </motion.div>

      <motion.div variants={fade} className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard title="Overall Score" value={94} suffix=".2%" change="+1.4% improvement" changeType="positive" icon={Award} accentColor="cyan" />
        <StatCard title="Relevancy" value={96} suffix="%" change="Target: >90%" changeType="positive" icon={CheckCircle2} accentColor="emerald" />
        <StatCard title="Groundedness" value={94} suffix="%" change="RAG confidence" changeType="positive" icon={Activity} accentColor="indigo" />
        <StatCard title="Hallucination Rate" value={1} suffix=".8%" change="−0.6% reduction" changeType="positive" icon={AlertTriangle} accentColor="amber" />
      </motion.div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <motion.div variants={fade} className="lg:col-span-2">
          <GlassPanel className="p-6">
            <SectionHeader title="Multi-Dimension Quality Radar" subtitle="Scored across 6 core criteria" />
            <ResponsiveContainer width="100%" height={280}>
              <RadarChart cx="50%" cy="50%" outerRadius="80%" data={radarData}>
                <PolarGrid stroke="rgba(255,255,255,0.08)" />
                <PolarAngleAxis dataKey="dimension" tick={{ fill: "#a1a1aa", fontSize: 11 }} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} tick={{ fill: "#71717a", fontSize: 9 }} />
                <Radar name="Quality Score" dataKey="score" stroke="#06b6d4" fill="#06b6d4" fillOpacity={0.3} />
              </RadarChart>
            </ResponsiveContainer>
          </GlassPanel>
        </motion.div>

        <motion.div variants={fade}>
          <GlassPanel className="p-6">
            <SectionHeader title="Evaluation Benchmarks" />
            <div className="space-y-6 mt-4">
              <ProgressRing value={96} color="#06b6d4" label="Relevancy Threshold" />
              <div className="space-y-3 text-xs">
                <div className="flex justify-between border-b border-white/5 pb-2">
                  <span className="text-neutral-500">Evaluator Model</span>
                  <span className="font-semibold text-white">GPT-4o Evaluation Agent</span>
                </div>
                <div className="flex justify-between border-b border-white/5 pb-2">
                  <span className="text-neutral-500">Sample Rate</span>
                  <span className="font-semibold text-emerald-400">100% of Runs</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-neutral-500">Target SLA</span>
                  <span className="font-semibold text-indigo-400">&gt; 92.0%</span>
                </div>
              </div>
            </div>
          </GlassPanel>
        </motion.div>
      </div>

      <motion.div variants={fade}>
        <GlassPanel className="p-6">
          <SectionHeader title="Agent Quality Breakdown" subtitle="Detailed dimension scores per agent" />
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-white/5 text-[10px] font-semibold uppercase tracking-wider text-neutral-600">
                  <th className="pb-3 pr-4">Agent</th>
                  <th className="pb-3 pr-4 text-right">Relevance</th>
                  <th className="pb-3 pr-4 text-right">Groundedness</th>
                  <th className="pb-3 pr-4 text-right">Accuracy</th>
                  <th className="pb-3 pr-4 text-right">Overall Quality</th>
                  <th className="pb-3">Health Bar</th>
                </tr>
              </thead>
              <tbody>
                {agentQualityScores.map((a) => (
                  <tr key={a.name} className="border-b border-white/[0.03] transition hover:bg-white/[0.015]">
                    <td className="py-3.5 pr-4 font-medium text-white">{a.name}</td>
                    <td className="py-3.5 pr-4 text-right tabular-nums text-neutral-300">{a.relevance}%</td>
                    <td className="py-3.5 pr-4 text-right tabular-nums text-neutral-300">{a.groundedness}%</td>
                    <td className="py-3.5 pr-4 text-right tabular-nums text-neutral-300">{a.accuracy}%</td>
                    <td className="py-3.5 pr-4 text-right font-bold text-cyan-400 tabular-nums">{a.overall}%</td>
                    <td className="py-3.5">
                      <div className="h-1.5 w-full rounded-full bg-white/5">
                        <div className="h-full rounded-full bg-cyan-400 transition-all duration-700" style={{ width: `${a.overall}%` }} />
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
