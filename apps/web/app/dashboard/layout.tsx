"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import {
  Cpu, LayoutDashboard, ShieldCheck, Activity, BarChart3, Database,
  Workflow, FileCode, GraduationCap, AlertTriangle, Lightbulb, Zap, Settings,
  User, Bell, Search, LogOut, ShieldAlert
} from "lucide-react";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const router = useRouter();
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [checkingAuth, setCheckingAuth] = useState(true);

  useEffect(() => {
    // Auth Guard Check
    const token = localStorage.getItem("nexus_auth_token");
    if (!token) {
      router.push("/auth/login");
    } else {
      setIsAuthenticated(true);
    }
    setCheckingAuth(false);
  }, [router]);

  const handleLogout = () => {
    localStorage.removeItem("nexus_auth_token");
    localStorage.removeItem("nexus_user_email");
    document.cookie = "nexus_auth_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    router.push("/auth/login");
  };

  if (checkingAuth) {
    return (
      <div className="flex h-screen items-center justify-center bg-[#030303] text-white">
        <div className="flex flex-col items-center gap-3">
          <div className="h-8 w-8 animate-spin rounded-full border-2 border-indigo-500 border-t-transparent" />
          <p className="text-xs font-semibold text-neutral-400">Verifying Admin Session...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) return null;

  const menuItems = [
    { name: "Overview", icon: LayoutDashboard, path: "/dashboard" },
    { name: "Agent Monitor", icon: Cpu, path: "/dashboard/agents" },
    { name: "Cost Governance", icon: BarChart3, path: "/dashboard/costs" },
    { name: "Quality Assessment", icon: Activity, path: "/dashboard/quality" },
    { name: "Safety & Shield", icon: ShieldCheck, path: "/dashboard/safety" },
    { name: "Memory & Qdrant", icon: Database, path: "/dashboard/memory" },
    { name: "Workflow Builder", icon: Workflow, path: "/dashboard/workflows" },
    { name: "Prompt Library", icon: FileCode, path: "/dashboard/prompts" },
    { name: "Knowledge Base", icon: GraduationCap, path: "/dashboard/knowledge" },
    { name: "Alerts & Incidents", icon: AlertTriangle, path: "/dashboard/alerts" },
    { name: "Optimization Center", icon: Zap, path: "/dashboard/optimizations" },
    { name: "Recommendations", icon: Lightbulb, path: "/dashboard/recommendations" },
    { name: "System Settings", icon: Settings, path: "/dashboard/settings" },
  ];

  return (
    <div className="flex h-screen bg-[#030303] overflow-hidden text-neutral-200">
      {/* Sidebar */}
      <aside className="w-64 glass-panel border-r border-white/5 flex flex-col z-20">
        {/* Brand */}
        <div className="p-6 border-b border-white/5 flex items-center gap-2.5">
          <div className="h-8 w-8 rounded-lg bg-gradient-to-tr from-indigo-500 to-purple-500 flex items-center justify-center">
            <Cpu className="h-4.5 w-4.5 text-white" />
          </div>
          <span className="font-bold text-lg tracking-tight text-white">
            AgentOps <span className="text-indigo-400">Nexus</span>
          </span>
        </div>

        {/* Navigation Menu */}
        <nav className="flex-1 px-4 py-6 overflow-y-auto space-y-1">
          {menuItems.map((item) => {
            const isActive = pathname === item.path;
            return (
              <Link
                key={item.name}
                href={item.path}
                className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition ${
                  isActive
                    ? "bg-white/10 text-white border border-white/10"
                    : "text-neutral-400 hover:bg-white/5 hover:text-white"
                }`}
              >
                <item.icon className={`h-4.5 w-4.5 ${isActive ? "text-indigo-400" : "text-neutral-400"}`} />
                {item.name}
              </Link>
            );
          })}
        </nav>

        {/* User profile footer */}
        <div className="p-4 border-t border-white/5 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="h-9 w-9 rounded-full bg-indigo-500/20 border border-indigo-500/30 flex items-center justify-center font-bold text-xs text-indigo-400">
              AD
            </div>
            <div>
              <p className="text-xs font-semibold text-white">Admin User</p>
              <p className="text-[10px] text-neutral-500">admin@agentopsnexus.com</p>
            </div>
          </div>
          <button
            onClick={handleLogout}
            title="Sign Out"
            className="p-2 rounded-lg hover:bg-red-500/10 text-neutral-500 hover:text-red-400 transition"
          >
            <LogOut className="h-4 w-4" />
          </button>
        </div>
      </aside>

      {/* Main Container */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="h-16 glass-panel border-b border-white/5 px-8 flex items-center justify-between z-10">
          <div className="flex items-center gap-4 w-96 relative">
            <Search className="absolute left-3 top-2.5 h-4 w-4 text-neutral-500" />
            <input
              type="text"
              placeholder="Search agents, workflows, prompts..."
              className="w-full bg-neutral-900/50 border border-white/5 rounded-lg pl-10 pr-4 py-2 text-xs outline-none focus:border-white/10 transition"
            />
          </div>

          <div className="flex items-center gap-4">
            <button className="relative p-2 rounded-lg hover:bg-white/5 text-neutral-400 hover:text-white transition">
              <Bell className="h-4.5 w-4.5" />
              <span className="absolute top-1.5 right-1.5 h-1.5 w-1.5 rounded-full bg-indigo-500"></span>
            </button>
            <div className="h-8 w-px bg-white/5"></div>
            <div className="text-xs text-right">
              <p className="text-white font-semibold">Nexus Org</p>
              <p className="text-[10px] text-emerald-400">Admin Mode Active</p>
            </div>
          </div>
        </header>

        {/* Content area */}
        <main className="flex-1 overflow-y-auto p-8 bg-[#030303]">
          {children}
        </main>
      </div>
    </div>
  );
}
