"use client";

import { useState } from "react";
import { motion, Variants } from "framer-motion";
import { Settings, Key, Shield, Bell, Save, CheckCircle2 } from "lucide-react";
import { GlassPanel, SectionHeader } from "@/components/ui/nexus-components";

const stagger: Variants = { hidden: { opacity: 0 }, show: { opacity: 1, transition: { staggerChildren: 0.06 } } };
const fade: Variants = { hidden: { opacity: 0, y: 16 }, show: { opacity: 1, y: 0, transition: { duration: 0.4 } } };

export default function PlatformSettings() {
  const [saved, setSaved] = useState(false);
  const [openaiKey, setOpenaiKey] = useState("sk-proj-••••••••••••••••••••");
  const [anthropicKey, setAnthropicKey] = useState("sk-ant-••••••••••••••••••••");
  const [enkryptKey, setEnkryptKey] = useState("enk_live_••••••••••••••••••••");

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => setSaved(false), 2500);
  };

  return (
    <motion.div variants={stagger} initial="hidden" animate="show" className="space-y-8">
      <motion.div variants={fade} className="flex items-end justify-between">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight text-white">System & Governance Settings</h1>
          <p className="mt-1 text-sm text-neutral-500">Configure API keys, webhooks, security policies, and integrations</p>
        </div>
      </motion.div>

      <form onSubmit={handleSave} className="space-y-6">
        {/* API Credentials */}
        <motion.div variants={fade}>
          <GlassPanel className="p-6">
            <SectionHeader title="API Credentials & Provider Keys" subtitle="Managed securely with environment encryption" />
            <div className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-neutral-300 mb-1">OpenAI API Key</label>
                <input
                  type="password"
                  value={openaiKey}
                  onChange={(e) => setOpenaiKey(e.target.value)}
                  className="w-full rounded-xl border border-white/10 bg-neutral-900/60 px-4 py-3 text-xs font-mono text-white outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-neutral-300 mb-1">Anthropic Claude API Key</label>
                <input
                  type="password"
                  value={anthropicKey}
                  onChange={(e) => setAnthropicKey(e.target.value)}
                  className="w-full rounded-xl border border-white/10 bg-neutral-900/60 px-4 py-3 text-xs font-mono text-white outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-neutral-300 mb-1">Enkrypt AI Moderation Key</label>
                <input
                  type="password"
                  value={enkryptKey}
                  onChange={(e) => setEnkryptKey(e.target.value)}
                  className="w-full rounded-xl border border-white/10 bg-neutral-900/60 px-4 py-3 text-xs font-mono text-white outline-none focus:border-indigo-500"
                />
              </div>
            </div>
          </GlassPanel>
        </motion.div>

        {/* Action Button */}
        <motion.div variants={fade} className="flex items-center gap-4">
          <button
            type="submit"
            className="flex items-center gap-2 rounded-xl bg-indigo-600 px-6 py-3 text-xs font-bold text-white shadow-lg shadow-indigo-600/30 transition hover:bg-indigo-500"
          >
            <Save className="h-4 w-4" /> Save Settings
          </button>

          {saved && (
            <span className="flex items-center gap-1.5 text-xs font-bold text-emerald-400">
              <CheckCircle2 className="h-4 w-4" /> Settings Saved Successfully!
            </span>
          )}
        </motion.div>
      </form>
    </motion.div>
  );
}
