"use client";

import { useState } from "react";
import { motion, Variants } from "framer-motion";
import { Lightbulb, ArrowUpRight, DollarSign, Zap, CheckCircle2, Award } from "lucide-react";
import { StatCard, GlassPanel, SectionHeader, StatusBadge } from "@/components/ui/nexus-components";

const stagger: Variants = { hidden: { opacity: 0 }, show: { opacity: 1, transition: { staggerChildren: 0.06 } } };
const fade: Variants = { hidden: { opacity: 0, y: 16 }, show: { opacity: 1, y: 0, transition: { duration: 0.4 } } };

interface RecItem {
  id: string;
  title: string;
  impact: string;
  impactDetail: string;
  confidence: number;
  status: "pending" | "approved" | "rejected" | "applied" | "failed" | "expired";
  reason: string;
}

const initialRecs: RecItem[] = [
  { id: "REC-301", title: "Switch Billing Evaluator to GPT-4o Mini", impact: "Cost Savings", impactDetail: "Save $140/mo (38% reduction)", confidence: 96, status: "pending", reason: "Billing classification tasks maintain 99.1% accuracy on Mini with 4x lower token cost." },
  { id: "REC-302", title: "Enable Prompt Variable Caching on Customer Support Bot", impact: "Latency Reduction", impactDetail: "Reduce response latency by 600ms", confidence: 92, status: "applied", reason: "Repetitive system prompt tokens can be cached across multi-turn conversations." },
  { id: "REC-303", title: "Add Enkrypt PII Redactor Guardrail to Lead Router", impact: "Safety Hardening", impactDetail: "Prevent sensitive data logging", confidence: 99, status: "pending", reason: "Telemetry logs detected raw phone numbers in debug payloads." },
];

export default function RecommendationsEngine() {
  const [recs, setRecs] = useState<RecItem[]>(initialRecs);

  const applyRecommendation = (id: string) => {
    setRecs(recs.map((r) => (r.id === id ? { ...r, status: "applied" } : r)));
  };

  return (
    <motion.div variants={stagger} initial="hidden" animate="show" className="space-y-8">
      <motion.div variants={fade} className="flex items-end justify-between">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight text-white">AI COO Recommendation Engine</h1>
          <p className="mt-1 text-sm text-neutral-500">Autonomous governance suggestions for cost, quality, and safety optimization</p>
        </div>
        <div className="flex items-center gap-2 rounded-full border border-amber-500/20 bg-amber-500/10 px-3 py-1.5 text-xs font-semibold text-amber-400">
          <Lightbulb className="h-4 w-4" /> AI COO Advisor Active
        </div>
      </motion.div>

      <motion.div variants={fade} className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard title="Est. Monthly Savings" value={340} prefix="$" change="Via model routing" changeType="positive" icon={DollarSign} accentColor="emerald" />
        <StatCard title="Pending Insights" value={2} change="Actionable choices" changeType="neutral" icon={Lightbulb} accentColor="amber" />
        <StatCard title="Applied Recommendations" value={18} change="100% successful" changeType="positive" icon={CheckCircle2} accentColor="indigo" />
        <StatCard title="Avg Confidence Score" value={96} suffix="%" change="High confidence" changeType="positive" icon={Award} accentColor="cyan" />
      </motion.div>

      <motion.div variants={fade}>
        <GlassPanel className="p-6">
          <SectionHeader title="Autonomous Optimization Suggestions" subtitle="Review and apply recommended configuration changes" />
          <div className="space-y-4">
            {recs.map((r) => (
              <div key={r.id} className="rounded-xl border border-white/[0.04] bg-white/[0.01] p-5 transition hover:border-white/[0.08]">
                <div className="flex items-start justify-between">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-[10px] text-neutral-600">{r.id}</span>
                      <span className="rounded bg-emerald-500/10 px-2 py-0.5 text-[10px] font-bold text-emerald-400">
                        {r.impact}: {r.impactDetail}
                      </span>
                    </div>
                    <h4 className="mt-1 text-sm font-bold text-white">{r.title}</h4>
                    <p className="mt-2 text-xs text-neutral-400 leading-relaxed">{r.reason}</p>
                  </div>
                  <StatusBadge status={r.status} />
                </div>

                <div className="mt-4 flex items-center justify-between border-t border-white/[0.04] pt-4">
                  <span className="text-[10px] font-semibold text-neutral-500">
                    Confidence Score: <span className="font-bold text-indigo-400">{r.confidence}%</span>
                  </span>
                  {r.status === "pending" && (
                    <button
                      onClick={() => applyRecommendation(r.id)}
                      className="rounded-lg bg-indigo-600 px-4 py-2 text-xs font-bold text-white transition hover:bg-indigo-500"
                    >
                      Auto-Apply Change
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        </GlassPanel>
      </motion.div>
    </motion.div>
  );
}
