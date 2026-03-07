import { ReactNode } from "react";
import { Link, useLocation } from "react-router-dom";
import { Bell, Settings, LayoutDashboard, MessageSquare, Radio } from "lucide-react";
import { motion } from "framer-motion";
import { RECENT_ALERTS } from "@/data/syntheticData";
import { HerdSenseLogo } from "@/components/brand/HerdSenseLogo";

interface AppLayoutProps {
  children: ReactNode;
}

const NAV_ITEMS = [
  { to: "/dashboard", icon: LayoutDashboard, label: "Dashboard" },
  { to: "/livefeed",  icon: Radio,           label: "Live Feed" },
  { to: "/field-oracle", icon: MessageSquare, label: "Field Oracle" },
  { to: "/settings",  icon: Settings,        label: "Settings" },
];

export default function AppLayout({ children }: AppLayoutProps) {
  const location = useLocation();
  const criticalCount = RECENT_ALERTS.filter(a => a.severity === "HIGH").length;

  return (
    <div className="min-h-screen bg-background bg-grid flex flex-col">
      {/* Top Nav */}
      <header className="sticky top-0 z-50 border-b border-border bg-field-900/90 backdrop-blur-md">
        <div className="flex items-center justify-between px-4 md:px-8 h-14">
          {/* Logo */}
          <Link to="/dashboard" className="flex items-center gap-2.5 group">
            <div className="relative">
              <HerdSenseLogo className="w-8 h-8" />
              <div className="absolute -top-0.5 -right-0.5 w-2 h-2 rounded-full bg-primary animate-pulse-lime" />
            </div>
            <span className="font-display font-bold text-lg text-primary group-hover:text-lime-glow transition-colors">
              HerdSense
            </span>
          </Link>

          {/* Center nav */}
          <nav className="hidden md:flex items-center gap-1">
            {NAV_ITEMS.map(({ to, icon: Icon, label }) => {
              const active = location.pathname === to || location.pathname.startsWith(to + "/");
              return (
                <Link
                  key={to}
                  to={to}
                  className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-sm font-medium transition-all duration-200 ${
                    active
                      ? "bg-lime-dark text-primary shadow-glow-lime"
                      : "text-muted-foreground hover:text-foreground hover:bg-field-600"
                  }`}
                >
                  <Icon size={14} />
                  {label}
                </Link>
              );
            })}
          </nav>

          {/* Right side */}
          <div className="flex items-center gap-3">
            <span className="hidden sm:block text-xs font-mono text-muted-foreground">Meadowbrook Farm</span>
            <button className="relative p-2 rounded-md hover:bg-field-600 transition-colors">
              <Bell size={18} className="text-muted-foreground" />
              {criticalCount > 0 && (
                <span className="absolute top-1 right-1 w-4 h-4 rounded-full bg-danger text-white text-[9px] font-bold flex items-center justify-center animate-pulse-danger">
                  {criticalCount}
                </span>
              )}
            </button>
            <div className="w-8 h-8 rounded-full bg-field-500 border border-border flex items-center justify-center text-xs font-display font-bold text-primary">
              JC
            </div>
          </div>
        </div>

        {/* Mobile nav */}
        <div className="md:hidden flex items-center gap-0.5 px-2 pb-2">
          {NAV_ITEMS.map(({ to, icon: Icon, label }) => {
            const active = location.pathname === to;
            return (
              <Link
                key={to}
                to={to}
                className={`flex-1 flex flex-col items-center gap-0.5 py-1.5 rounded-md text-[10px] font-medium transition-all ${
                  active ? "bg-lime-dark text-primary" : "text-muted-foreground"
                }`}
              >
                <Icon size={14} />
                {label}
              </Link>
            );
          })}
        </div>
      </header>

      {/* Page content */}
      <motion.main
        className="flex-1"
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -8 }}
        transition={{ duration: 0.25, ease: "easeOut" }}
      >
        {children}
      </motion.main>
    </div>
  );
}
