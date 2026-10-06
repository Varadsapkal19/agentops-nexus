"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { Shield, Sparkles, Activity, Cpu, ArrowRight, Zap, CheckCircle2, Lock, BarChart3, Database } from "lucide-react";

export default function Home() {
  return (
    <div className="min-h-screen bg-neutral-950 text-white selection:bg-indigo-500 selection:text-white">
      {/* Background glow effects */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -left-40 h-96 w-96 rounded-full bg-indigo-600/15 blur-[120px]" />
        <div className="absolute top-1/3 -right-40 h-96 w-96 rounded-full bg-pink-600/15 blur-[120px]" />
        <div className="absolute -bottom-40 left-1/3 h-96 w-96 rounded-full bg-cyan-600/15 blur-[120px]" />
      </div>

      {/* Navigation */}
      <nav className="sticky top-0 z-50 border-b border-white/[0.06] bg-neutral-950/80 backdrop-blur-md">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-tr from-indigo-500 via-purple-500 to-pink-500 shadow-lg shadow-indigo-500/20">
              <Shield className="h-5 w-5 text-white" />
            </div>
            <span className="text-lg font-extrabold tracking-tight text-white">AgentOps Nexus</span>
          </div>
          <div className="flex items-center gap-4">
            <Link
              href="/auth/login"
              className="text-xs font-semibold text-neutral-400 transition hover:text-white"
            >
              Sign In
            </Link>
            <Link
              href="/dashboard"
              className="flex items-center gap-2 rounded-xl bg-indigo-600 px-4 py-2 text-xs font-bold text-white shadow-lg shadow-indigo-600/30 transition hover:bg-indigo-500"
            >
              Launch Dashboard <ArrowRight className="h-3.5 w-3.5" />
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative mx-auto max-w-7xl px-6 pt-20 pb-16 text-center">
        <div className="mx-auto inline-flex items-center gap-2 rounded-full border border-indigo-500/30 bg-indigo-500/10 px-4 py-1.5 text-xs font-semibold text-indigo-400 mb-8">
          <Sparkles className="h-3.5 w-3.5 animate-pulse" /> AI COO for Enterprise Agent Ecosystems
        </div>

        <h1 className="mx-auto max-w-4xl text-5xl font-black tracking-tight text-white sm:text-6xl md:text-7xl">
          One Agent to Govern <br />
          <span className="bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
            Every Other Agent
          </span>
        </h1>

        <p className="mx-auto mt-6 max-w-2xl text-base text-neutral-400 sm:text-lg">
          Real-time observability, automated evaluation, cost governance, and Enkrypt AI safety guardrails for production multi-agent LLM systems.
        </p>

        <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
          <Link
            href="/dashboard"
            className="flex items-center gap-2 rounded-xl bg-indigo-600 px-6 py-3.5 text-sm font-bold text-white shadow-xl shadow-indigo-600/30 transition hover:bg-indigo-500"
          >
            Go to Nexus Control Center <ArrowRight className="h-4 w-4" />
          </Link>
          <Link
            href="/auth/signup"
            className="rounded-xl border border-white/[0.08] bg-white/[0.03] px-6 py-3.5 text-sm font-bold text-white backdrop-blur-sm transition hover:border-white/[0.15] hover:bg-white/[0.06]"
          >
            Start Enterprise Trial
          </Link>
        </div>
      </section>

      {/* Feature Cards Grid */}
      <section className="mx-auto max-w-7xl px-6 py-16">
        <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
          <div className="rounded-2xl border border-white/[0.06] bg-white/[0.02] p-8 backdrop-blur-sm transition hover:border-white/[0.12]">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-indigo-500/10 text-indigo-400 mb-6">
              <Activity className="h-6 w-6" />
            </div>
            <h3 className="text-lg font-bold text-white">Agent Tracing & Latency</h3>
            <p className="mt-2 text-xs text-neutral-400 leading-relaxed">
              Trace multi-agent execution DAGs, measure step-by-step latency, and analyze call graphs in real-time.
            </p>
          </div>

          <div className="rounded-2xl border border-white/[0.06] bg-white/[0.02] p-8 backdrop-blur-sm transition hover:border-white/[0.12]">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-pink-500/10 text-pink-400 mb-6">
              <Shield className="h-6 w-6" />
            </div>
            <h3 className="text-lg font-bold text-white">Enkrypt AI Safety Shield</h3>
            <p className="mt-2 text-xs text-neutral-400 leading-relaxed">
              Detect hallucinations, jailbreaks, PII exposure, and toxicity before responses leave your pipeline.
            </p>
          </div>

          <div className="rounded-2xl border border-white/[0.06] bg-white/[0.02] p-8 backdrop-blur-sm transition hover:border-white/[0.12]">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-emerald-500/10 text-emerald-400 mb-6">
              <BarChart3 className="h-6 w-6" />
            </div>
            <h3 className="text-lg font-bold text-white">Cost & Token Governance</h3>
            <p className="mt-2 text-xs text-neutral-400 leading-relaxed">
              Monitor spend per agent, set budget caps, and receive automated recommendations for model switching.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}
