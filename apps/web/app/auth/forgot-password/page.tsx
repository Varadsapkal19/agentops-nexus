"use client";

import Link from "next/link";
import { Cpu, Mail, ArrowLeft } from "lucide-react";
import { useState } from "react";

export default function ForgotPasswordPage() {
  const [submitted, setSubmitted] = useState(false);

  return (
    <div className="flex min-h-screen items-center justify-center bg-[#030303] px-6 py-12">
      <div className="w-full max-w-md glass-panel p-8 rounded-2xl border border-white/10 shadow-2xl">
        <div className="text-center mb-8">
          <div className="h-12 w-12 rounded-xl bg-gradient-to-tr from-indigo-500 to-purple-500 flex items-center justify-center shadow-lg shadow-indigo-500/20 mx-auto mb-4">
            <Cpu className="h-6 w-6 text-white" />
          </div>
          <h2 className="text-2xl font-bold tracking-tight">Reset password</h2>
          <p className="text-sm text-neutral-400 mt-2">
            {submitted ? "Check your email for a reset link" : "Enter your email to receive a password reset link"}
          </p>
        </div>

        {!submitted ? (
          <form className="space-y-6" onSubmit={(e) => { e.preventDefault(); setSubmitted(true); }}>
            <div>
              <label className="block text-sm font-medium text-neutral-300 mb-2">Email Address</label>
              <div className="relative">
                <input type="email" placeholder="name@company.com" required className="w-full pl-10 pr-4 py-3 bg-neutral-900/50 border border-white/10 rounded-xl focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none transition text-sm" />
                <Mail className="absolute left-3 top-3.5 h-4 w-4 text-neutral-500" />
              </div>
            </div>

            <button type="submit" className="w-full py-3.5 px-4 rounded-xl bg-gradient-to-r from-indigo-500 to-purple-600 font-bold hover:from-indigo-600 hover:to-purple-700 transition shadow-lg shadow-indigo-500/20">
              Send Reset Link
            </button>
          </form>
        ) : (
          <div className="text-center py-4">
            <p className="text-sm text-neutral-400 mb-6">
              We have sent a password reset link to your email address. Please follow the instructions to secure your account.
            </p>
            <button onClick={() => setSubmitted(false)} className="text-xs text-indigo-400 hover:underline">
              Didn't receive email? Try again
            </button>
          </div>
        )}

        <div className="mt-8 pt-6 border-t border-white/5 flex items-center justify-center">
          <Link href="/auth/login" className="inline-flex items-center gap-2 text-xs text-neutral-400 hover:text-white transition font-medium">
            <ArrowLeft className="h-3 w-3" /> Back to Login
          </Link>
        </div>
      </div>
    </div>
  );
}
