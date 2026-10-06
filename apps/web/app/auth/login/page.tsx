"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { Cpu, Mail, Lock, Eye, EyeOff, AlertCircle, Sparkles } from "lucide-react";
import { useState } from "react";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("admin@agentopsnexus.com");
  const [password, setPassword] = useState("Admin@123");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    setTimeout(() => {
      // Valid credentials check
      if (email.trim().toLowerCase() === "admin@agentopsnexus.com" && password === "Admin@123") {
        localStorage.setItem("nexus_auth_token", "admin_session_token_nexus_2026");
        localStorage.setItem("nexus_user_email", email);
        document.cookie = "nexus_auth_token=admin_session_token_nexus_2026; path=/;";
        router.push("/dashboard");
      } else {
        setError("Invalid email or password. Use the admin credentials shown below.");
        setLoading(false);
      }
    }, 600);
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-[#030303] px-6 py-12 text-white">
      <div className="w-full max-w-md rounded-2xl border border-white/10 bg-neutral-950/80 p-8 shadow-2xl backdrop-blur-xl relative">
        {/* Top Logo Badge */}
        <div className="absolute -top-10 left-1/2 -translate-x-1/2 flex h-20 w-20 items-center justify-center rounded-2xl bg-gradient-to-tr from-indigo-500 via-purple-500 to-pink-500 shadow-xl shadow-indigo-500/30">
          <Cpu className="h-10 w-10 text-white" />
        </div>

        <div className="text-center mt-8 mb-6">
          <h2 className="text-2xl font-extrabold tracking-tight">AgentOps Nexus</h2>
          <p className="text-xs text-neutral-400 mt-1">Sign in with Enterprise Admin credentials</p>
        </div>

        {/* Demo Admin Banner */}
        <div className="mb-6 rounded-xl border border-indigo-500/30 bg-indigo-500/10 p-3.5 text-xs text-indigo-300">
          <div className="flex items-center gap-1.5 font-bold mb-1">
            <Sparkles className="h-3.5 w-3.5 text-indigo-400" /> Default Admin Credentials
          </div>
          <p className="text-[11px] text-neutral-300">Email: <span className="font-mono text-white font-semibold">admin@agentopsnexus.com</span></p>
          <p className="text-[11px] text-neutral-300">Password: <span className="font-mono text-white font-semibold">Admin@123</span></p>
        </div>

        {error && (
          <div className="mb-6 flex items-center gap-2 rounded-xl border border-red-500/30 bg-red-500/10 p-3 text-xs text-red-400">
            <AlertCircle className="h-4 w-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <form className="space-y-5" onSubmit={handleLogin}>
          <div>
            <label className="block text-xs font-semibold text-neutral-300 mb-2">Admin Email</label>
            <div className="relative">
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="w-full pl-10 pr-4 py-3 bg-neutral-900/60 border border-white/10 rounded-xl focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none transition text-xs font-mono"
              />
              <Mail className="absolute left-3 top-3.5 h-4 w-4 text-neutral-500" />
            </div>
          </div>

          <div>
            <div className="flex justify-between items-center mb-2">
              <label className="block text-xs font-semibold text-neutral-300">Password</label>
            </div>
            <div className="relative">
              <input
                type={showPassword ? "text" : "password"}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full pl-10 pr-10 py-3 bg-neutral-900/60 border border-white/10 rounded-xl focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none transition text-xs font-mono"
              />
              <Lock className="absolute left-3 top-3.5 h-4 w-4 text-neutral-500" />
              <button type="button" onClick={() => setShowPassword(!showPassword)} className="absolute right-3 top-3.5 text-neutral-500 hover:text-white">
                {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
              </button>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3.5 px-4 rounded-xl bg-gradient-to-r from-indigo-500 to-purple-600 font-bold hover:from-indigo-600 hover:to-purple-700 transition shadow-lg shadow-indigo-500/25 text-xs text-white disabled:opacity-50"
          >
            {loading ? "Authenticating Admin..." : "Sign In to Control Center"}
          </button>
        </form>
      </div>
    </div>
  );
}
