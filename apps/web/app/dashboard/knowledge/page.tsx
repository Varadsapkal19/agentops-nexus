"use client";

import { useState } from "react";
import { motion, Variants } from "framer-motion";
import { GraduationCap, Upload, FileText, CheckCircle2, Layers, Database } from "lucide-react";
import { StatCard, GlassPanel, SectionHeader, StatusBadge } from "@/components/ui/nexus-components";

const stagger: Variants = { hidden: { opacity: 0 }, show: { opacity: 1, transition: { staggerChildren: 0.06 } } };
const fade: Variants = { hidden: { opacity: 0, y: 16 }, show: { opacity: 1, y: 0, transition: { duration: 0.4 } } };

const documents = [
  { id: "doc-101", title: "Enterprise SLA & Governance Guidelines 2026.pdf", chunks: 142, model: "text-embedding-3-large", status: "ready" as const, uploaded: "2d ago", size: "4.2 MB" },
  { id: "doc-102", title: "Agentops_Nexus_System_Architecture.md", chunks: 89, model: "text-embedding-3-large", status: "ready" as const, uploaded: "1d ago", size: "1.8 MB" },
  { id: "doc-103", title: "Enkrypt_AI_Moderation_Policy_Spec.pdf", chunks: 210, model: "text-embedding-3-large", status: "ready" as const, uploaded: "5h ago", size: "6.5 MB" },
  { id: "doc-104", title: "Customer_Billing_Terms_v4.docx", chunks: 45, model: "text-embedding-3-large", status: "ready" as const, uploaded: "12h ago", size: "890 KB" },
];

export default function KnowledgeBase() {
  return (
    <motion.div variants={stagger} initial="hidden" animate="show" className="space-y-8">
      <motion.div variants={fade} className="flex items-end justify-between">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight text-white">Knowledge Base & RAG Index</h1>
          <p className="mt-1 text-sm text-neutral-500">Document chunking, vector embedding sync, and RAG context store</p>
        </div>
        <button className="flex items-center gap-2 rounded-xl bg-indigo-600 px-4 py-2.5 text-xs font-bold text-white shadow-lg shadow-indigo-600/30 transition hover:bg-indigo-500">
          <Upload className="h-4 w-4" /> Upload Document
        </button>
      </motion.div>

      <motion.div variants={fade} className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard title="Indexed Documents" value={48} change="+6 this week" changeType="positive" icon={FileText} accentColor="indigo" />
        <StatCard title="Total Chunks" value={124000} change="100% embedded" changeType="positive" icon={Layers} accentColor="purple" />
        <StatCard title="Embedding Model" value={3072} prefix="" suffix=" dims" change="text-embedding-3" changeType="neutral" icon={Database} accentColor="cyan" />
        <StatCard title="RAG Retrieval Latency" value={6} suffix="ms" change="p95 speed" changeType="positive" icon={CheckCircle2} accentColor="emerald" />
      </motion.div>

      <motion.div variants={fade}>
        <GlassPanel className="p-6">
          <SectionHeader title="Managed Knowledge Documents" subtitle="RAG context documents indexed in Qdrant" />
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-white/5 text-[10px] font-semibold uppercase tracking-wider text-neutral-600">
                  <th className="pb-3 pr-4">Document Title</th>
                  <th className="pb-3 pr-4">Embedding Model</th>
                  <th className="pb-3 pr-4 text-right">Chunks</th>
                  <th className="pb-3 pr-4 text-right">File Size</th>
                  <th className="pb-3 pr-4 text-right">Uploaded</th>
                  <th className="pb-3 text-right">Status</th>
                </tr>
              </thead>
              <tbody>
                {documents.map((doc) => (
                  <tr key={doc.id} className="border-b border-white/[0.03] transition hover:bg-white/[0.015]">
                    <td className="py-3.5 pr-4 flex items-center gap-2.5 font-medium text-white">
                      <FileText className="h-4 w-4 text-indigo-400" />
                      {doc.title}
                    </td>
                    <td className="py-3.5 pr-4 text-neutral-400 font-mono text-[11px]">{doc.model}</td>
                    <td className="py-3.5 pr-4 text-right tabular-nums font-bold text-white">{doc.chunks}</td>
                    <td className="py-3.5 pr-4 text-right tabular-nums text-neutral-400">{doc.size}</td>
                    <td className="py-3.5 pr-4 text-right text-neutral-500">{doc.uploaded}</td>
                    <td className="py-3.5 text-right"><StatusBadge status="active" label="Indexed" /></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </GlassPanel>
      </motion.div>
    </motion.div>
  );
}
