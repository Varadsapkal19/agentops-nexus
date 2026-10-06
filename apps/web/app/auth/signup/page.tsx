"use client";

import Link from "next/link";
import { Cpu, Mail, Lock, User } from "lucide-react";

export default function SignupPage() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-[#030303] px-6 py-12">
      <div className="w-full max-w-md glass-panel p-8 rounded-2xl border border-white/10 shadow-2xl">
        <div className="text-center mb-8">
          <div className="h-12 w-12 rounded-xl bg-gradient-to-tr from-indigo-500 to-purple-500 flex items-center justify-center shadow-lg shadow-indigo-500/20 mx-auto mb-4">
            <Cpu className="h-6 w-6 text-white" />
          </div>
          <h2 className="text-2xl font-bold tracking-tight">Create your account</h2>
          <p className="text-sm text-neutral-400 mt-2">Deploy your agent governance supervisor today</p>
        </div>

        <form className="space-y-5" onSubmit={(e) => { e.preventDefault(); window.location.href = '/dashboard'; }}>
          <div>
            <label className="block text-sm font-medium text-neutral-300 mb-2">Full Name</label>
            <div className="relative">
              <input type="text" placeholder="John Doe" required className="w-full pl-10 pr-4 py-3 bg-neutral-900/50 border border-white/10 rounded-xl focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none transition text-sm" />
              <User className="absolute left-3 top-3.5 h-4 w-4 text-neutral-500" />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-neutral-300 mb-2">Work Email</label>
            <div className="relative">
              <input type="email" placeholder="name@company.com" required className="w-full pl-10 pr-4 py-3 bg-neutral-900/50 border border-white/10 rounded-xl focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none transition text-sm" />
              <Mail className="absolute left-3 top-3.5 h-4 w-4 text-neutral-500" />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-neutral-300 mb-2">Password</label>
            <div className="relative">
              <input type="password" placeholder="Min. 8 characters" required className="w-full pl-10 pr-4 py-3 bg-neutral-900/50 border border-white/10 rounded-xl focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none transition text-sm" />
              <Lock className="absolute left-3 top-3.5 h-4 w-4 text-neutral-500" />
            </div>
          </div>

          <div className="flex items-center">
            <input type="checkbox" id="terms" required className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500 bg-neutral-900" />
            <label htmlFor="terms" className="ml-2 block text-xs text-neutral-400">
              I agree to the <Link href="#" className="text-indigo-400 hover:underline">Terms of Service</Link> and <Link href="#" className="text-indigo-400 hover:underline">Privacy Policy</Link>.
            </label>
          </div>

          <button type="submit" className="w-full py-3.5 px-4 rounded-xl bg-gradient-to-r from-indigo-500 to-purple-600 font-bold hover:from-indigo-600 hover:to-purple-700 transition shadow-lg shadow-indigo-500/20">
            Create Account
          </button>
        </form>

        <div className="mt-6 text-center text-xs text-neutral-500">
          Already have an account? <Link href="/auth/login" className="text-indigo-400 hover:text-indigo-300 transition font-semibold">Sign in</Link>
        </div>
      </div>
    </div>
  );
}
