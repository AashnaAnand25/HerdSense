import { RECENT_ALERTS, ANIMALS_LIST, BARN_NAMES, RiskLevel } from "@/data/syntheticData";
import { useNavigate, Link } from "react-router-dom";
import { motion } from "framer-motion";
import { ChevronRight, AlertTriangle, Activity, Thermometer, Footprints, Scale } from "lucide-react";

const SEVERITY_STYLES: Record<RiskLevel, { bg: string; text: string; border: string; label: string }> = {
  HIGH:   { bg: "bg-danger/15", text: "text-danger", border: "border-danger/40", label: "HIGH" },
  MEDIUM: { bg: "bg-warning/15", text: "text-warning", border: "border-warning/40", label: "MEDIUM" },
  LOW:    { bg: "bg-healthy/15", text: "text-healthy", border: "border-healthy/40", label: "LOW" },
  "NO-CALL": { bg: "bg-field-600", text: "text-muted-foreground", border: "border-border", label: "NO-CALL" },
};

const ALERT_ICONS: Record<string, typeof Activity> = {
  Feed: Activity, Temp: Thermometer, Gait: Footprints, Weight: Scale,
  Posture: Activity, Activity: Activity,
};

/** Strip "Cow #ID — " prefix for compact display */
function shortMessage(message: string): string {
  return message.replace(/^Cow #[\w-]+ —\s*/i, "").trim();
}

export default function PriorityAlerts() {
  const navigate = useNavigate();
  const criticalCount = RECENT_ALERTS.filter((a) => a.severity === "HIGH").length;
  const animalById = new Map(ANIMALS_LIST.map((a) => [a.id, a]));

  const items = RECENT_ALERTS.map((alert) => ({
    ...alert,
    animal: animalById.get(alert.animalId),
    name: BARN_NAMES[alert.animalId] ?? `#${alert.animalId}`,
  })).sort((a, b) => {
    const order: Record<RiskLevel, number> = { HIGH: 0, MEDIUM: 1, LOW: 2, "NO-CALL": 3 };
    const diff = order[a.severity] - order[b.severity];
    return diff !== 0 ? diff : a.minutesAgo - b.minutesAgo;
  });

  return (
    <div className="card-glass rounded-xl overflow-hidden" id="alerts-section">
      <div className="flex items-center justify-between px-4 py-3 border-b border-border">
        <h3 className="font-display text-base font-bold text-foreground">Priority alerts</h3>
        <div className="flex items-center gap-2">
          {criticalCount > 0 && (
            <span className="text-sm font-mono text-danger font-semibold animate-pulse-danger flex items-center gap-1">
              <AlertTriangle size={14} />
              {criticalCount} critical
            </span>
          )}
          <span className="text-sm font-mono text-muted-foreground">{items.length} total</span>
        </div>
      </div>

      <div className="p-4 space-y-3">
        {items.map((item, i) => {
          const style = SEVERITY_STYLES[item.severity];
          const Icon = ALERT_ICONS[item.type] ?? Activity;
          return (
            <motion.button
              key={item.id}
              type="button"
              onClick={() => navigate(`/animal/${item.animalId}`)}
              className={`w-full text-left rounded-xl border-2 p-4 transition-all hover:scale-[1.01] active:scale-[0.99] ${style.bg} ${style.border} hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-primary/50`}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.04 }}
            >
              <div className="flex items-start gap-3">
                <div className={`flex-shrink-0 p-2 rounded-lg ${style.bg} border ${style.border}`}>
                  <Icon size={18} className={style.text} />
                </div>
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="font-display font-bold text-foreground">{item.name}</span>
                    <span className="font-mono text-sm text-muted-foreground">#{item.animalId}</span>
                    {item.animal && (
                      <span className="text-sm text-muted-foreground">· {item.animal.breed}</span>
                    )}
                  </div>
                  <p className="mt-1 text-sm text-foreground/90 line-clamp-2">{shortMessage(item.message)}</p>
                  <div className="flex items-center gap-2 mt-1.5 flex-wrap">
                    <span className="text-xs font-mono text-muted-foreground">{item.timestamp}</span>
                  </div>
                </div>
                <div className="flex items-center gap-2 flex-shrink-0">
                  <span className={`inline-flex flex-col items-end px-2.5 py-1 rounded-lg border ${style.border} ${style.text}`}>
                    <span className="text-[10px] font-mono uppercase tracking-wider">{item.severity}</span>
                  </span>
                  <ChevronRight size={20} className={`${style.text} opacity-70`} />
                </div>
              </div>
            </motion.button>
          );
        })}

        <Link
          to="/livefeed"
          className="flex items-center justify-center gap-2 w-full py-3 rounded-xl border-2 border-dashed border-border text-muted-foreground hover:border-primary/40 hover:text-primary hover:bg-primary/5 transition-colors text-sm font-medium mt-2"
        >
          View all animals in Live Feed
          <ChevronRight size={16} />
        </Link>
      </div>
    </div>
  );
}
