"use client";

import React from "react";
import { cn } from "@/lib/utils";
import { useAnimatedCounter } from "@/hooks/use-animations";
import { type LucideIcon } from "lucide-react";

/* ───────────────────── Stat Card ───────────────────── */
interface StatCardProps {
  title: string;
  value: number;
  suffix?: string;
  prefix?: string;
  change?: string;
  changeType?: "positive" | "negative" | "neutral";
  icon: LucideIcon;
  accentColor?: string;
}

export function StatCard({
  title,
  value,
  suffix = "",
  prefix = "",
  change,
  changeType = "neutral",
  icon: Icon,
  accentColor = "indigo",
}: StatCardProps) {
  const animated = useAnimatedCounter(value, 1800);

  const colorMap: Record<string, string> = {
    indigo: "text-indigo-400 bg-indigo-500/10 border-indigo-500/20",
    emerald: "text-emerald-400 bg-emerald-500/10 border-emerald-500/20",
    pink: "text-pink-400 bg-pink-500/10 border-pink-500/20",
    cyan: "text-cyan-400 bg-cyan-500/10 border-cyan-500/20",
    amber: "text-amber-400 bg-amber-500/10 border-amber-500/20",
    violet: "text-violet-400 bg-violet-500/10 border-violet-500/20",
  };

  const changeColor =
    changeType === "positive"
      ? "text-emerald-400"
      : changeType === "negative"
      ? "text-red-400"
      : "text-neutral-500";

  return (
    <div className="group relative overflow-hidden rounded-2xl border border-white/[0.06] bg-white/[0.02] p-6 transition-all duration-300 hover:border-white/[0.12] hover:bg-white/[0.04] hover:shadow-2xl hover:shadow-black/20">
      {/* Glow accent */}
      <div
        className={cn(
          "absolute -right-6 -top-6 h-24 w-24 rounded-full blur-3xl opacity-0 transition-opacity duration-500 group-hover:opacity-30",
          accentColor === "indigo" && "bg-indigo-500",
          accentColor === "emerald" && "bg-emerald-500",
          accentColor === "pink" && "bg-pink-500",
          accentColor === "cyan" && "bg-cyan-500",
          accentColor === "amber" && "bg-amber-500",
          accentColor === "violet" && "bg-violet-500"
        )}
      />

      <div className="flex items-start justify-between mb-4">
        <span className="text-[11px] font-semibold uppercase tracking-widest text-neutral-500">
          {title}
        </span>
        <div
          className={cn(
            "flex h-9 w-9 items-center justify-center rounded-xl border",
            colorMap[accentColor]
          )}
        >
          <Icon className="h-4 w-4" />
        </div>
      </div>

      <div className="mb-1.5">
        <span className="text-3xl font-bold tracking-tight text-white tabular-nums">
          {prefix}
          {animated.toLocaleString()}
          {suffix}
        </span>
      </div>

      {change && (
        <span className={cn("text-[11px] font-medium", changeColor)}>
          {change}
        </span>
      )}
    </div>
  );
}

/* ───────────────────── Glass Panel ───────────────────── */
interface GlassPanelProps {
  children: React.ReactNode;
  className?: string;
  hover?: boolean;
}

export function GlassPanel({ children, className, hover = true }: GlassPanelProps) {
  return (
    <div
      className={cn(
        "rounded-2xl border border-white/[0.06] bg-white/[0.02] backdrop-blur-sm",
        hover && "transition-all duration-300 hover:border-white/[0.1] hover:bg-white/[0.035]",
        className
      )}
    >
      {children}
    </div>
  );
}

/* ───────────────────── Section Header ───────────────────── */
interface SectionHeaderProps {
  title: string;
  subtitle?: string;
  action?: React.ReactNode;
}

export function SectionHeader({ title, subtitle, action }: SectionHeaderProps) {
  return (
    <div className="flex items-end justify-between mb-6">
      <div>
        <h3 className="text-sm font-bold text-white">{title}</h3>
        {subtitle && (
          <p className="text-[11px] text-neutral-500 mt-0.5">{subtitle}</p>
        )}
      </div>
      {action}
    </div>
  );
}

/* ───────────────────── Status Badge ───────────────────── */
interface StatusBadgeProps {
  status: "active" | "paused" | "error" | "resolved" | "blocked" | "warning" | "acknowledged" | "pending" | "applied" | "failed" | "suppressed" | "approved" | "rejected" | "expired";
  label?: string;
}

export function StatusBadge({ status, label }: StatusBadgeProps) {
  const config: Record<string, { bg: string; text: string; dot: string; defaultLabel: string }> = {
    active: { bg: "bg-emerald-500/10", text: "text-emerald-400", dot: "bg-emerald-400", defaultLabel: "Active" },
    paused: { bg: "bg-amber-500/10", text: "text-amber-400", dot: "bg-amber-400", defaultLabel: "Paused" },
    error: { bg: "bg-red-500/10", text: "text-red-400", dot: "bg-red-400", defaultLabel: "Error" },
    resolved: { bg: "bg-emerald-500/10", text: "text-emerald-400", dot: "bg-emerald-400", defaultLabel: "Resolved" },
    blocked: { bg: "bg-pink-500/10", text: "text-pink-400", dot: "bg-pink-400", defaultLabel: "Blocked" },
    warning: { bg: "bg-amber-500/10", text: "text-amber-400", dot: "bg-amber-400", defaultLabel: "Warning" },
    acknowledged: { bg: "bg-amber-500/10", text: "text-amber-400", dot: "bg-amber-400", defaultLabel: "Acknowledged" },
    pending: { bg: "bg-amber-500/10", text: "text-amber-400", dot: "bg-amber-400", defaultLabel: "Pending" },
    applied: { bg: "bg-emerald-500/10", text: "text-emerald-400", dot: "bg-emerald-400", defaultLabel: "Applied" },
    failed: { bg: "bg-red-500/10", text: "text-red-400", dot: "bg-red-400", defaultLabel: "Failed" },
    suppressed: { bg: "bg-neutral-500/10", text: "text-neutral-400", dot: "bg-neutral-400", defaultLabel: "Suppressed" },
    approved: { bg: "bg-emerald-500/10", text: "text-emerald-400", dot: "bg-emerald-400", defaultLabel: "Approved" },
    rejected: { bg: "bg-red-500/10", text: "text-red-400", dot: "bg-red-400", defaultLabel: "Rejected" },
    expired: { bg: "bg-neutral-500/10", text: "text-neutral-400", dot: "bg-neutral-400", defaultLabel: "Expired" },
  };

  const c = config[status] || config.active;

  return (
    <span className={cn("inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-[10px] font-semibold", c.bg, c.text)}>
      <span className={cn("h-1.5 w-1.5 rounded-full animate-pulse", c.dot)} />
      {label || c.defaultLabel}
    </span>
  );
}

/* ───────────────────── Severity Badge ───────────────────── */
interface SeverityBadgeProps {
  severity: "critical" | "high" | "medium" | "low" | "info";
}

export function SeverityBadge({ severity }: SeverityBadgeProps) {
  const config: Record<string, { bg: string; text: string; label: string }> = {
    critical: { bg: "bg-red-500/15", text: "text-red-400", label: "Critical" },
    high: { bg: "bg-orange-500/15", text: "text-orange-400", label: "High" },
    medium: { bg: "bg-amber-500/15", text: "text-amber-400", label: "Medium" },
    low: { bg: "bg-blue-500/15", text: "text-blue-400", label: "Low" },
    info: { bg: "bg-neutral-500/15", text: "text-neutral-400", label: "Info" },
  };

  const c = config[severity] || config.info;

  return (
    <span className={cn("rounded-md px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider", c.bg, c.text)}>
      {c.label}
    </span>
  );
}

/* ───────────────────── Progress Ring ───────────────────── */
interface ProgressRingProps {
  value: number;
  size?: number;
  strokeWidth?: number;
  color?: string;
  label?: string;
}

export function ProgressRing({ value, size = 80, strokeWidth = 6, color = "#6366f1", label }: ProgressRingProps) {
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (value / 100) * circumference;

  return (
    <div className="flex flex-col items-center gap-2">
      <div className="relative" style={{ width: size, height: size }}>
        <svg width={size} height={size} className="-rotate-90">
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke="rgba(255,255,255,0.05)"
            strokeWidth={strokeWidth}
            fill="none"
          />
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke={color}
            strokeWidth={strokeWidth}
            fill="none"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            strokeLinecap="round"
            className="transition-all duration-1000 ease-out"
          />
        </svg>
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-sm font-bold text-white">{value}%</span>
        </div>
      </div>
      {label && <span className="text-[10px] font-medium text-neutral-500">{label}</span>}
    </div>
  );
}
