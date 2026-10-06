"use client";

import { useState } from "react";
import { motion, Variants } from "framer-motion";
import { AlertTriangle, CheckCircle, Bell, Filter, ShieldAlert } from "lucide-react";
import { StatCard, GlassPanel, SectionHeader, StatusBadge, SeverityBadge } from "@/components/ui/nexus-components";

const stagger: Variants = { hidden: { opacity: 0 }, show: { opacity: 1, transition: { staggerChildren: 0.06 } } };
const fade: Variants = { hidden: { opacity: 0, y: 16 }, show: { opacity: 1, y: 0, transition: { duration: 0.4 } } };

interface AlertItem {
  id: string;
  title: string;
  message: string;
  severity: "critical" | "high" | "medium" | "low" | "info";
  status: "active" | "acknowledged" | "resolved" | "suppressed";
  agent: string;
  time: string;
}

const initialAlerts: AlertItem[] = [
  { id: "ALT-801", title: "Hallucination Risk Detected", message: "Customer Success Bot attempted to state unapproved 40% enterprise discount", severity: "high", status: "active", agent: "Customer Success Bot", time: "14m ago" },
  { id: "ALT-802", title: "Monthly Budget Threshold Reached", message: "Billing Evaluator utilized 92% of designated monthly budget cap ($2,300 spent)", severity: "medium", status: "acknowledged", agent: "Billing Evaluator", time: "2h ago" },
  { id: "ALT-803", title: "Upstream Model Latency Spike", message: "Claude 3.5 API latency exceeded 4.5s for 5 consecutive runs", severity: "low", status: "resolved", agent: "Lead Router Agent", time: "1d ago" },
];

export default function AlertsIncidents() {
  const [alerts, setAlerts] = useState<AlertItem[]>(initialAlerts);

  const acknowledgeAlert = (id: string) => {
    setAlerts(alerts.map((a) => (a.id === id ? { ...a, status: "acknowledged" } : a)));
  };

  return (
    <motion.div variants={stagger} initial="hidden" animate="show" className="space-y-8">
      <motion.div variants={fade} className="flex items-end justify-between">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight text-white">Alerts & Incident Management</h1>
          <p className="mt-1 text-sm text-neutral-500">Real-time incident dispatch, severity triage, and automated resolution logs</p>
        </div>
        <div className="flex items-center gap-2 rounded-full border border-red-500/20 bg-red-500/10 px-3 py-1.5 text-xs font-semibold text-red-400">
          <AlertTriangle className="h-4 w-4" /> 1 Active Incident
        </div>
      </motion.div>

      <motion.div variants={fade} className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard title="Active Alerts" value={1} change="Requires triage" changeType="negative" icon={AlertTriangle} accentColor="pink" />
        <StatCard title="Acknowledged" value={1} change="Under investigation" changeType="neutral" icon={Bell} accentColor="amber" />
        <StatCard title="Resolved Today" value={4} change="100% auto-mitigated" changeType="positive" icon={CheckCircle} accentColor="emerald" />
        <StatCard title="Mean Time To Resolve" value={4} suffix="m" change="Fast SLA response" changeType="positive" icon={ShieldAlert} accentColor="indigo" />
      </motion.div>

      <motion.div variants={fade}>
        <GlassPanel className="p-6">
          <SectionHeader title="System Incident Dispatch Log" subtitle="Real-time alert queue with action controls" />
          <div className="space-y-4">
            {alerts.map((alert) => (
              <div key={alert.id} className="flex flex-wrap items-center justify-between gap-4 rounded-xl border border-white/[0.04] bg-white/[0.01] p-5 transition hover:border-white/[0.08]">
                <div className="flex items-start gap-4">
                  <div className={`mt-0.5 flex h-9 w-9 items-center justify-center rounded-xl ${
                    alert.severity === "high" ? "bg-red-500/10 text-red-400" : "bg-amber-500/10 text-amber-400"
                  }`}>
                    <AlertTriangle className="h-5 w-5" />
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-[10px] text-neutral-600">{alert.id}</span>
                      <SeverityBadge severity={alert.severity} />
                    </div>
                    <h4 className="mt-1 text-sm font-bold text-white">{alert.title}</h4>
                    <p className="mt-0.5 text-xs text-neutral-400">{alert.message}</p>
                    <p className="mt-2 text-[10px] text-neutral-600">Agent: <span className="text-neutral-300 font-semibold">{alert.agent}</span> · {alert.time}</p>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  {alert.status === "active" && (
                    <button
                      onClick={() => acknowledgeAlert(alert.id)}
                      className="rounded-lg bg-indigo-600 px-4 py-2 text-xs font-bold text-white transition hover:bg-indigo-500"
                    >
                      Acknowledge
                    </button>
                  )}
                  <StatusBadge status={alert.status} />
                </div>
              </div>
            ))}
          </div>
        </GlassPanel>
      </motion.div>
    </motion.div>
  );
}
