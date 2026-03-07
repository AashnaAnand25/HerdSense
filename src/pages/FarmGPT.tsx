import { useState, useRef, useEffect } from "react";
import AppLayout from "@/components/AppLayout";
import { FARM_DOCUMENTS, SUGGESTED_QUESTIONS } from "@/data/syntheticData";
import { motion, AnimatePresence } from "framer-motion";
import { Send, Upload, FileText, ChevronRight, X, Settings, AlertCircle, Sparkles } from "lucide-react";

interface Message {
  role: "user" | "assistant";
  content: string;
  citations?: string[];
}

const SYSTEM_PROMPT = `You are FarmGPT, an agricultural document assistant for HerdSense. You help farmers understand their farm records, vet histories, and operational data. ONLY answer questions based on the provided farm documents below. If the answer is not in the documents, say so explicitly and suggest what document might contain it. Always cite which document and approximate section your answer comes from. Keep answers concise and actionable for a busy farmer. Never hallucinate statistics or animal data.`;

function buildDocContext(docs: Record<string, string>) {
  return Object.entries(docs)
    .map(([name, content]) => `\n\n=== ${name} ===\n${content}`)
    .join("\n");
}

function ChatMessage({ msg }: { msg: Message }) {
  const isUser = msg.role === "user";
  return (
    <motion.div
      className={`flex ${isUser ? "justify-end" : "justify-start"} mb-4`}
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
    >
      {!isUser && (
        <div className="w-7 h-7 rounded-full bg-lime-dark border border-primary/30 flex items-center justify-center mr-2 flex-shrink-0 mt-1">
          <Sparkles size={12} className="text-primary" />
        </div>
      )}
      <div className={`max-w-[85%] ${isUser ? "" : "flex-1"}`}>
        <div
          className={`rounded-xl px-4 py-3 text-sm font-body leading-relaxed ${
            isUser
              ? "bg-lime-dark text-primary border border-primary/30 ml-auto"
              : "bg-field-700 text-foreground border border-border"
          }`}
        >
          <p className="whitespace-pre-wrap">{msg.content}</p>
        </div>
        {msg.citations && msg.citations.length > 0 && (
          <div className="flex flex-wrap gap-1.5 mt-2 pl-1">
            {msg.citations.map((c, i) => (
              <span key={i} className="flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-mono bg-field-600 border border-border text-muted-foreground">
                <FileText size={9} />
                {c}
              </span>
            ))}
          </div>
        )}
      </div>
    </motion.div>
  );
}

// Extract citations from AI response text
function extractCitations(text: string): string[] {
  const sources = Object.keys(FARM_DOCUMENTS);
  return sources.filter(s => text.toLowerCase().includes(s.toLowerCase().replace(".pdf", "")));
}

export default function FarmGPT() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: "Hello! I'm FarmGPT, your farm document assistant. I've pre-loaded your 2024 Annual Report, Q3 Vet Summary, and Winter Feed Log. Ask me anything about your farm data!",
      citations: [],
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [apiKey, setApiKey] = useState<string>("");
  const [showKeyModal, setShowKeyModal] = useState(false);
  const [uploadedDocs, setUploadedDocs] = useState<Record<string, string>>(FARM_DOCUMENTS);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const send = async (text: string) => {
    if (!text.trim() || isLoading) return;
    const userMsg: Message = { role: "user", content: text };
    setMessages(prev => [...prev, userMsg]);
    setInput("");
    setIsLoading(true);

    if (!apiKey) {
      // Demo mode: smart canned responses
      setTimeout(() => {
        const resp = generateDemoResponse(text, uploadedDocs);
        const citations = extractCitations(resp);
        setMessages(prev => [...prev, { role: "assistant", content: resp, citations }]);
        setIsLoading(false);
      }, 900 + Math.random() * 600);
      return;
    }

    try {
      const docContext = buildDocContext(uploadedDocs);
      const response = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-api-key": apiKey,
          "anthropic-version": "2023-06-01",
        },
        body: JSON.stringify({
          model: "claude-opus-4-5",
          max_tokens: 1024,
          system: `${SYSTEM_PROMPT}\n\n[DOCUMENTS]:${docContext}`,
          messages: [
            ...messages.map(m => ({ role: m.role, content: m.content })),
            { role: "user", content: text },
          ],
        }),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();
      const content = data.content?.[0]?.text || "I couldn't generate a response.";
      const citations = extractCitations(content);
      setMessages(prev => [...prev, { role: "assistant", content, citations }]);
    } catch (err) {
      setMessages(prev => [...prev, {
        role: "assistant",
        content: `Error connecting to Claude API. Running in demo mode — your API key may be incorrect or the request failed. Demo responses are pre-generated from the farm documents.`,
        citations: [],
      }]);
      // Fallback to demo
      const resp = generateDemoResponse(text, uploadedDocs);
      const citations = extractCitations(resp);
      setTimeout(() => {
        setMessages(prev => [...prev, { role: "assistant", content: resp, citations }]);
      }, 500);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AppLayout>
      <div className="h-[calc(100vh-56px)] md:h-[calc(100vh-56px)] flex overflow-hidden">
        {/* Sidebar */}
        <div className="w-64 flex-shrink-0 border-r border-border bg-field-800/50 flex flex-col hidden md:flex">
          <div className="px-4 py-3 border-b border-border">
            <h3 className="font-display text-xs font-bold text-foreground uppercase tracking-wider">Farm Documents</h3>
          </div>

          <div className="flex-1 overflow-y-auto p-3 space-y-2">
            <p className="text-[10px] font-mono text-muted-foreground uppercase tracking-wider mb-2">Pre-loaded</p>
            {Object.keys(FARM_DOCUMENTS).map(name => (
              <div key={name} className="flex items-center gap-2 p-2 rounded-lg bg-field-700 border border-border">
                <FileText size={12} className="text-primary flex-shrink-0" />
                <div className="min-w-0">
                  <p className="text-[11px] font-body text-foreground truncate">{name}</p>
                  <p className="text-[9px] font-mono text-muted-foreground">
                    {name.includes("Annual") ? "Annual Report" : name.includes("Vet") ? "Vet Records" : "Feed Log"}
                  </p>
                </div>
              </div>
            ))}

            <div className="pt-3 border-t border-border mt-3">
              <p className="text-[10px] font-mono text-muted-foreground uppercase tracking-wider mb-2">Upload More</p>
              <label className="flex items-center gap-2 p-2 rounded-lg border border-dashed border-border hover:border-primary/50 cursor-pointer transition-colors">
                <Upload size={12} className="text-muted-foreground" />
                <span className="text-[11px] font-mono text-muted-foreground">Add document</span>
                <input type="file" accept=".pdf,.txt,.doc,.docx" className="hidden" />
              </label>
            </div>
          </div>

          {/* API Key */}
          <div className="p-3 border-t border-border">
            <button
              onClick={() => setShowKeyModal(true)}
              className="w-full flex items-center gap-2 px-3 py-2 rounded-lg bg-field-700 border border-border hover:border-primary/40 transition-colors text-left"
            >
              <Settings size={12} className="text-muted-foreground" />
              <div>
                <p className="text-[10px] font-mono text-muted-foreground">Claude API Key</p>
                <p className="text-[10px] font-mono text-primary">{apiKey ? "● Configured" : "Demo Mode"}</p>
              </div>
            </button>
          </div>
        </div>

        {/* Chat Area */}
        <div className="flex-1 flex flex-col min-w-0">
          {/* Header */}
          <div className="flex items-center justify-between px-4 py-3 border-b border-border bg-field-800/30">
            <div>
              <h2 className="font-display text-sm font-bold text-foreground">Ask about your farm data</h2>
              <p className="text-[10px] font-mono text-muted-foreground">
                {apiKey ? "Claude-powered · Real API" : "Demo Mode · Pre-cached responses"}
              </p>
            </div>
            <div className="flex items-center gap-1.5 px-2 py-1 rounded-full bg-field-700 border border-border">
              <Sparkles size={10} className="text-primary" />
              <span className="text-[10px] font-mono text-primary">Gemini-powered</span>
            </div>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 md:p-6">
            {messages.map((msg, i) => (
              <ChatMessage key={i} msg={msg} />
            ))}

            {isLoading && (
              <motion.div className="flex items-center gap-2 mb-4" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                <div className="w-7 h-7 rounded-full bg-lime-dark border border-primary/30 flex items-center justify-center">
                  <Sparkles size={12} className="text-primary" />
                </div>
                <div className="bg-field-700 border border-border rounded-xl px-4 py-3">
                  <div className="flex gap-1">
                    {[0, 1, 2].map(i => (
                      <motion.div
                        key={i}
                        className="w-1.5 h-1.5 rounded-full bg-primary/60"
                        animate={{ opacity: [0.3, 1, 0.3] }}
                        transition={{ duration: 1.2, delay: i * 0.2, repeat: Infinity }}
                      />
                    ))}
                  </div>
                </div>
              </motion.div>
            )}

            {/* Suggested questions (shown when no user messages yet) */}
            {messages.length === 1 && (
              <div className="mt-2">
                <p className="text-xs font-mono text-muted-foreground mb-3">Try asking:</p>
                <div className="flex flex-wrap gap-2">
                  {SUGGESTED_QUESTIONS.map(q => (
                    <button
                      key={q}
                      onClick={() => send(q)}
                      className="px-3 py-1.5 rounded-lg bg-field-700 border border-border text-xs font-body text-muted-foreground hover:border-primary/40 hover:text-foreground transition-all text-left"
                    >
                      {q}
                    </button>
                  ))}
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="px-4 py-3 border-t border-border bg-field-800/30">
            <div className="flex items-center gap-2 bg-field-700 border border-border rounded-xl px-3 py-2 focus-within:border-primary/50 transition-colors">
              <input
                type="text"
                value={input}
                onChange={e => setInput(e.target.value)}
                onKeyDown={e => e.key === "Enter" && !e.shiftKey && send(input)}
                placeholder="Ask about your farm data..."
                className="flex-1 bg-transparent text-sm font-body text-foreground placeholder-muted-foreground focus:outline-none"
              />
              <button
                onClick={() => send(input)}
                disabled={!input.trim() || isLoading}
                className="p-1.5 rounded-lg bg-primary text-primary-foreground hover:bg-lime-glow disabled:opacity-40 disabled:cursor-not-allowed transition-all"
              >
                <Send size={14} />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* API Key Modal */}
      <AnimatePresence>
        {showKeyModal && (
          <motion.div
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setShowKeyModal(false)}
          >
            <motion.div
              className="card-glass rounded-xl p-6 w-full max-w-md mx-4"
              initial={{ scale: 0.95, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.95, opacity: 0 }}
              onClick={e => e.stopPropagation()}
            >
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-display text-sm font-bold text-foreground">Configure Claude API Key</h3>
                <button onClick={() => setShowKeyModal(false)}><X size={16} className="text-muted-foreground" /></button>
              </div>
              <div className="flex items-start gap-2 p-3 rounded-lg bg-field-700 border border-warning/20 mb-4">
                <AlertCircle size={14} className="text-warning mt-0.5 flex-shrink-0" />
                <p className="text-xs font-body text-muted-foreground">
                  Key stored in component state only — never sent to any server except Anthropic API.
                  Leave empty to use Demo Mode with pre-cached responses.
                </p>
              </div>
              <input
                type="password"
                value={apiKey}
                onChange={e => setApiKey(e.target.value)}
                placeholder="sk-ant-..."
                className="w-full bg-field-700 border border-border rounded-lg px-3 py-2.5 text-sm font-mono text-foreground focus:outline-none focus:border-primary mb-4"
              />
              <div className="flex gap-2">
                <button
                  onClick={() => setShowKeyModal(false)}
                  className="flex-1 py-2 rounded-lg bg-primary text-primary-foreground font-display font-bold text-sm"
                >
                  {apiKey ? "Save Key" : "Use Demo Mode"}
                </button>
                {apiKey && (
                  <button
                    onClick={() => { setApiKey(""); setShowKeyModal(false); }}
                    className="px-4 py-2 rounded-lg border border-border text-muted-foreground text-sm font-mono"
                  >
                    Clear
                  </button>
                )}
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </AppLayout>
  );
}

// Demo response generator
function generateDemoResponse(question: string, docs: Record<string, string>): string {
  const q = question.toLowerCase();
  const annualDoc = docs["2024 Annual Farm Report.pdf"] || "";
  const vetDoc = docs["Q3 Vet Visit Summary.pdf"] || "";
  const feedDoc = docs["Winter Feed Log.pdf"] || "";

  if (q.includes("vet visit") || q.includes("vet intervention") || q.includes("most visits")) {
    return `Based on the **Q3 Vet Visit Summary** and **2024 Annual Report**, here are the animals with the most vet interventions this year:\n\n1. **R401** — Recurring respiratory issues, flagged in Q3 for increased monitoring\n2. **F017** — Colic episode in July, plus BCS flag in September\n3. **A142** — Feed avoidance (Feb, Sep), on pre-winter watchlist\n4. **E115** — Lameness in August, movement restriction resolved by end of Q3\n\nTotal vet interventions for the year: **41 visits** across all animals. Lameness (17 cases, 35%) and respiratory issues (15 cases, 30%) were the top health drivers.\n\n[Source: 2024 Annual Report, p.2 · Q3 Vet Summary, Visit Log]`;
  }
  if (q.includes("feed cost") || q.includes("feed") && q.includes("quarter")) {
    return `From your **2024 Annual Farm Report**, feed costs by quarter are:\n\n• **Q1**: $18,450 ($74.7/head) — Winter supplementation peak\n• **Q2**: $12,200 ($49.4/head) — Spring pasture reduced costs\n• **Q3**: $11,800 ($47.8/head) — Peak pasture season, lowest cost\n• **Q4**: $16,900 ($68.4/head) — Winter preparation ramp-up\n\n**Full Year Total: $59,350** | Per-head average: $240.30\n\nTrend: You saved ~35% on feed costs in summer compared to winter months. The Q3→Q4 jump of $5,100 reflects hay restocking and grain supplementation beginning.\n\n[Source: 2024 Annual Farm Report, Feed Costs Section]`;
  }
  if (q.includes("winter") || q.includes("health trend")) {
    return `Based on your **2024 Annual Report** and **Winter Feed Log**, here are the key health trends to monitor this winter:\n\n1. **Respiratory risk** peaks in October–March. 15 cases last year — ensure boosters are up to date (November vaccination round noted in Q4 actions ✓)\n2. **Pen 3 lameness cluster** — surface remediation was completed Oct 15, but monitor closely in cold/wet conditions\n3. **Feed avoidance episodes** increase in cold snaps — Cow A142 had an episode in Feb. Check sensor data weekly.\n4. **Water access** — Install or check trough heaters before December (trough heater installed Nov 20 per Q4 notes ✓)\n5. **BCS monitoring** — 8 animals below 2.5 BCS threshold need targeted feed increases\n\n[Source: 2024 Annual Report, Winter Prep Notes · Winter Feed Log]`;
  }
  if (q.includes("lameness") || q.includes("pen") && q.includes("risk")) {
    return `According to the **Q3 Vet Visit Summary** and **Annual Report**, **Pen 3** has the highest lameness risk:\n\n• Lameness is the #1 health issue at 17 cases (35% of all interventions)\n• **Pen 3** was specifically flagged: "flooring quality concerns raised, recommend surface replacement before winter"\n• **Pen 5** is secondary — E115 and P009 both received hoof trimming in August\n• Surface remediation for Pen 3 was completed October 15 (Q4 actions) ✓\n\nRecommendation from Dr. Okonkwo: "Consider heel horn erosion treatment for Pen 3 cohort proactively"\n\n[Source: Q3 Vet Visit Summary, Notable Findings · 2024 Annual Report]`;
  }
  if (q.includes("a142") || q.includes("cow a142")) {
    return `From the **Winter Feed Log** and **Q3 Vet Summary**, here's what the records say about **Cow A142**:\n\n• **February 19 (Winter Feed Log)**: Feed avoidance episode noted — 3-day episode, veterinary advice was to monitor. Resolved without intervention.\n• **September 10 (Q3 Vet Summary)**: Flagged in BCS assessment, placed on feed monitoring list alongside 5 other animals\n• **Q4 Annual Report**: Listed as one of 3 animals flagged for pre-winter weight monitoring (along with F017 and R401)\n\nCurrent sensor data shows reduced feeding activity >36hr — consistent with this animal's history of episodic feed avoidance. Recommend veterinary inspection.\n\n[Source: Winter Feed Log, Feed Incidents · Q3 Vet Summary · 2024 Annual Report]`;
  }
  if (q.includes("q3") && q.includes("q4") || q.includes("compare")) {
    return `Comparing **Q3 vs Q4** vet interventions from your **2024 Annual Report**:\n\n• **Q3 2024**: 11 interventions — 6 lameness, 3 respiratory, 2 metabolic\n• **Q4 2024** (to date): 7 interventions — 4 respiratory, 2 lameness, 1 wound\n\n**Key change**: Lameness cases dropped from 6 to 2 — likely due to Pen 3 surface remediation completed in October. Respiratory cases remain elevated as expected for fall season.\n\nFull year total: **41 vet visits** at approximately $185/visit average.\n\n[Source: 2024 Annual Farm Report, Health Incidents by Quarter]`;
  }

  // Fallback
  return `I searched through your uploaded farm documents (2024 Annual Report, Q3 Vet Summary, Winter Feed Log) but couldn't find specific information about "${question}".\n\nTo get a more complete answer, consider uploading:\n• Detailed breeding records\n• Individual animal vet histories\n• Monthly feed consumption logs\n\nIf you have a more specific question about health incidents, feed costs, or vet visits from your uploaded documents, I'm happy to help!\n\n[Source: HerdSense document search — no match found]`;
}
