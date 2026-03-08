import { useState, useEffect, useRef } from "react";
import AppLayout from "@/components/AppLayout";
import { motion } from "framer-motion";
import { Camera, Bell, Info } from "lucide-react";

const VISION_API_BASE = "http://localhost:5001";
const POLL_MS = 500;
const LOG_MAX = 20;

interface VisionResults {
  behavior: string;
  confidence: number;
  risk: "LOW" | "MEDIUM" | "HIGH";
  alert: string | null;
  detections: number;
  timestamp: number;
  camera_available?: boolean;
}

interface LogEntry {
  time: string;
  behavior: string;
  confidence: number;
  risk: string;
}

const RISK_STYLES = {
  LOW: "bg-healthy/15 text-healthy border-healthy/40",
  MEDIUM: "bg-warning/15 text-warning border-warning/40",
  HIGH: "bg-danger/15 text-danger border-danger/40",
};

const CONFIDENCE_BAR_COLORS = {
  LOW: "bg-healthy",
  MEDIUM: "bg-warning",
  HIGH: "bg-danger",
};

export default function Vision() {
  const [results, setResults] = useState<VisionResults | null>(null);
  const [streamOnline, setStreamOnline] = useState(false);
  const [behaviorLog, setBehaviorLog] = useState<LogEntry[]>([]);
  const prevBehaviorRef = useRef<string | null>(null);

  // Poll /results
  useEffect(() => {
    const poll = async () => {
      try {
        const r = await fetch(`${VISION_API_BASE}/results`);
        if (r.ok) {
          const data: VisionResults = await r.json();
          setResults(data);
          setStreamOnline(true); // server is up
          if (prevBehaviorRef.current !== data.behavior) {
            prevBehaviorRef.current = data.behavior;
            setBehaviorLog((log) => {
              const entry: LogEntry = {
                time: new Date().toLocaleTimeString("en-US", { hour12: false }),
                behavior: data.behavior,
                confidence: data.confidence,
                risk: data.risk,
              };
              return [entry, ...log].slice(0, LOG_MAX);
            });
          }
        }
      } catch {
        setResults(null);
        setStreamOnline(false);
      }
    };
    poll();
    const id = setInterval(poll, POLL_MS);
    return () => clearInterval(id);
  }, []);

  // Check if video stream is reachable
  useEffect(() => {
    const img = new Image();
    img.onload = () => setStreamOnline(true);
    img.onerror = () => setStreamOnline(false);
    img.src = `${VISION_API_BASE}/video_feed?t=${Date.now()}`;
    const t = setInterval(() => {
      img.src = `${VISION_API_BASE}/video_feed?t=${Date.now()}`;
    }, 3000);
    return () => clearInterval(t);
  }, []);

  return (
    <AppLayout>
      <div className="px-4 md:px-8 py-6 max-w-screen-2xl mx-auto space-y-4">
        <div className="rounded-lg border border-primary/20 bg-primary/5 px-4 py-2.5 flex items-center gap-2">
          <Info size={16} className="text-primary shrink-0" />
          <p className="text-sm font-body text-foreground/90">
            Computer Vision Mode — YOLOv8 running locally via Python backend. Point camera at any animal or person to classify behavior in real time.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left — Live camera feed */}
          <div className="card-glass rounded-xl overflow-hidden border-2 border-primary/20 shadow-glow-lime">
            <div className="relative aspect-video bg-field-900">
              {streamOnline ? (
                <img
                  src={`${VISION_API_BASE}/video_feed`}
                  alt="Live vision feed"
                  className="w-full h-full object-contain"
                />
              ) : (
                <div className="absolute inset-0 flex flex-col items-center justify-center gap-4 text-muted-foreground p-6 text-center">
                  <Camera size={48} className="opacity-50" />
                  <p className="font-display font-semibold text-foreground">Camera offline</p>
                  <p className="text-sm font-body max-w-sm">
                    To see live camera + classification here, start the vision server from the <strong>backend</strong> directory:
                  </p>
                  <pre className="bg-field-800 border border-border rounded-lg px-4 py-3 text-left text-xs font-mono text-primary w-full max-w-md overflow-x-auto">
                    cd backend{"\n"}
                    pip install ultralytics flask flask-cors opencv-python{"\n"}
                    python vision_server.py
                  </pre>
                  <p className="text-xs">
                    Then allow camera access when prompted. The feed and behavior labels will appear above.
                  </p>
                </div>
              )}
              {streamOnline && (
                <div className="absolute top-3 left-3 px-2.5 py-1 rounded-md bg-primary/90 text-primary-foreground font-mono text-xs font-bold flex items-center gap-1.5 animate-pulse-lime">
                  <span className="w-2 h-2 rounded-full bg-white" />
                  LIVE
                </div>
              )}
              <div className="absolute bottom-0 left-0 right-0 py-2 px-3 bg-black/70 font-mono text-xs text-primary">
                YOLOv8 · Real-time Detection · MPS Accelerated
              </div>
            </div>
          </div>

          {/* Right — Results panel */}
          <div className="space-y-4">
            <div className="card-glass rounded-xl overflow-hidden p-4 md:p-6">
              {results ? (
                <>
                  <p className="font-display text-3xl md:text-4xl font-bold text-foreground mb-3">
                    {results.behavior}
                  </p>
                  <div className="mb-4">
                    <div className="h-3 rounded-full bg-field-700 overflow-hidden">
                      <div
                        className={`h-full rounded-full transition-all duration-300 ${CONFIDENCE_BAR_COLORS[results.risk]}`}
                        style={{ width: `${results.confidence * 100}%` }}
                      />
                    </div>
                    <p className="text-xs font-mono text-muted-foreground mt-1">
                      Confidence {Math.round(results.confidence * 100)}%
                    </p>
                  </div>
                  <div className="flex items-center gap-2 mb-4">
                    <span
                      className={`inline-flex px-2.5 py-1 rounded-lg border font-mono text-sm font-bold ${RISK_STYLES[results.risk]}`}
                    >
                      {results.risk} RISK
                    </span>
                    <span className="text-sm font-mono text-muted-foreground">
                      {results.detections} detection{results.detections !== 1 ? "s" : ""}
                    </span>
                  </div>
                  {results.alert && (
                    <div className="flex items-start gap-2 rounded-lg border-2 border-danger/40 bg-danger/15 p-3 mb-4">
                      <Bell size={18} className="text-danger shrink-0 mt-0.5" />
                      <p className="text-sm font-body text-foreground">{results.alert}</p>
                    </div>
                  )}
                </>
              ) : (
                <p className="text-muted-foreground font-mono text-sm">Waiting for vision server…</p>
              )}
            </div>

            {/* Behavior log */}
            <div className="card-glass rounded-xl overflow-hidden">
              <div className="px-4 py-3 border-b border-border">
                <h3 className="font-display text-sm font-bold text-foreground">Behavior log</h3>
              </div>
              <div className="p-3 max-h-48 overflow-y-auto font-mono text-xs space-y-1">
                {behaviorLog.length === 0 ? (
                  <p className="text-muted-foreground">No entries yet.</p>
                ) : (
                  behaviorLog.map((entry, i) => (
                    <div
                      key={`${entry.time}-${i}`}
                      className="flex items-center gap-2 py-1 border-b border-border/50 last:border-0"
                    >
                      <span className="text-muted-foreground shrink-0">{entry.time}</span>
                      <span className="text-foreground">{entry.behavior}</span>
                      <span className="text-muted-foreground">{Math.round(entry.confidence * 100)}%</span>
                      <span className={`shrink-0 ${entry.risk === "HIGH" ? "text-danger" : entry.risk === "MEDIUM" ? "text-warning" : "text-healthy"}`}>
                        {entry.risk}
                      </span>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Classification key */}
        <div className="card-glass rounded-xl overflow-hidden">
          <div className="px-4 py-3 border-b border-border">
            <h3 className="font-display text-sm font-bold text-foreground">Behavior classification key</h3>
          </div>
          <div className="p-4 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3 font-body text-sm text-foreground/90">
            <div className="rounded-lg border border-healthy/30 bg-healthy/10 p-3">
              <p className="font-display font-semibold text-healthy">Standing/Walking</p>
              <p className="text-xs mt-0.5">Normal activity, LOW risk.</p>
            </div>
            <div className="rounded-lg border border-healthy/30 bg-healthy/10 p-3">
              <p className="font-display font-semibold text-healthy">Grazing</p>
              <p className="text-xs mt-0.5">Normal feeding behavior, LOW risk.</p>
            </div>
            <div className="rounded-lg border border-warning/30 bg-warning/10 p-3">
              <p className="font-display font-semibold text-warning">Lying Down</p>
              <p className="text-xs mt-0.5">Normal rest or extended lying concern if &gt;4hrs, MEDIUM risk.</p>
            </div>
            <div className="rounded-lg border border-danger/30 bg-danger/10 p-3">
              <p className="font-display font-semibold text-danger">Abnormal Gait</p>
              <p className="text-xs mt-0.5">Possible lameness or injury, HIGH risk — flag for vet.</p>
            </div>
            <div className="rounded-lg border border-border bg-field-700/50 p-3">
              <p className="font-display font-semibold text-muted-foreground">No animal detected</p>
              <p className="text-xs mt-0.5">Camera obstruction or animal out of frame.</p>
            </div>
          </div>
        </div>
      </div>
    </AppLayout>
  );
}
