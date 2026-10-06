"use client";

import { Cpu, Users, Activity, HardDrive } from "lucide-react";

export default function AdminPanel() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-extrabold text-white tracking-tight">Admin & System Health</h1>
        <p className="text-sm text-neutral-400 mt-1">Manage global system workloads, microservice states, and users</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="glass-card p-6 rounded-2xl border border-white/5">
          <div className="flex justify-between items-center mb-4">
            <span className="text-xs text-neutral-400">Total Users</span>
            <Users className="h-5 w-5 text-indigo-400" />
          </div>
          <h2 className="text-2xl font-bold text-white">4 users</h2>
        </div>

        <div className="glass-card p-6 rounded-2xl border border-white/5">
          <div className="flex justify-between items-center mb-4">
            <span className="text-xs text-neutral-400">Redis Memory</span>
            <HardDrive className="h-5 w-5 text-indigo-400" />
          </div>
          <h2 className="text-2xl font-bold text-white">124 MB</h2>
        </div>

        <div className="glass-card p-6 rounded-2xl border border-white/5">
          <div className="flex justify-between items-center mb-4">
            <span className="text-xs text-neutral-400">PostgreSQL Pool</span>
            <Activity className="h-5 w-5 text-emerald-400" />
          </div>
          <h2 className="text-2xl font-bold text-white">10 / 20 open</h2>
        </div>

        <div className="glass-card p-6 rounded-2xl border border-white/5">
          <div className="flex justify-between items-center mb-4">
            <span className="text-xs text-neutral-400">CPU Load</span>
            <Cpu className="h-5 w-5 text-emerald-400" />
          </div>
          <h2 className="text-2xl font-bold text-white">1.8% average</h2>
        </div>
      </div>
    </div>
  );
}
