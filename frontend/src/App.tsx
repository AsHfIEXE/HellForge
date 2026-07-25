import React, { useState, useEffect } from 'react';
import { 
  ShieldAlert, Radio, Cpu, Network, FileText, Activity, 
  Terminal, Settings as SettingsIcon, Layers, Server, Search, Bot
} from 'lucide-react';
import { D3TopologyGraph } from './components/D3TopologyGraph';
import { AssetsFeature } from './features/assets/AssetsFeature';
import { FindingsFeature } from './features/findings/FindingsFeature';
import { JSIntelFeature } from './features/js_intel/JSIntelFeature';
import { SchedulesFeature } from './features/schedules/SchedulesFeature';
import { ReportsFeature } from './features/reports/ReportsFeature';


export default function App() {
  const [activeTab, setActiveTab] = useState('overview');
  const [stats, setStats] = useState<any>({
    total_projects: 0,
    total_targets: 0,
    total_assets: 0,
    total_vulnerabilities: 0,
    average_risk_score: 0.0,
    severity_breakdown: { critical: 0, high: 0, medium: 0, low: 0 }
  });
  const [assets, setAssets] = useState<any[]>([]);
  const [findings, setFindings] = useState<any[]>([]);
  const [graphData, setGraphData] = useState<any>({ nodes: [], links: [] });
  const [plugins, setPlugins] = useState<any[]>([]);
  const [timeline, setTimeline] = useState<any[]>([]);
  const [targetInput, setTargetInput] = useState('testasp.vulnweb.com');
  const [isScanning, setIsScanning] = useState(false);
  const [aiQuery, setAiQuery] = useState('');
  const [aiResponse, setAiResponse] = useState<any>(null);


  useEffect(() => {
    fetchStats();
    fetchAssets();
    fetchFindings();
    fetchGraph();
    fetchPlugins();
    fetchTimeline();
  }, []);

  const fetchStats = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/v1/stats');
      if (res.ok) setStats(await res.json());
    } catch (e) {}
  };

  const fetchAssets = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/v1/assets');
      if (res.ok) setAssets(await res.json());
    } catch (e) {}
  };

  const fetchFindings = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/v1/findings');
      if (res.ok) setFindings(await res.json());
    } catch (e) {}
  };

  const fetchGraph = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/v1/graph');
      if (res.ok) setGraphData(await res.json());
    } catch (e) {}
  };

  const fetchPlugins = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/v1/plugins');
      if (res.ok) setPlugins(await res.json());
    } catch (e) {}
  };

  const fetchTimeline = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/v1/timeline');
      if (res.ok) setTimeline(await res.json());
    } catch (e) {}
  };

  const handleStartScan = async () => {
    if (!targetInput) return;
    setIsScanning(true);
    try {
      await fetch(`http://localhost:8000/api/v1/scans/start?domain=${targetInput}`, { method: 'POST' });
      await fetchStats();
      await fetchAssets();
      await fetchFindings();
      await fetchGraph();
      await fetchTimeline();
    } catch (e) {
    } finally {
      setIsScanning(false);
    }
  };

  const handleAiAsk = async () => {
    if (!aiQuery) return;
    try {
      const res = await fetch(`http://localhost:8000/api/v1/ai/analyze?query=${encodeURIComponent(aiQuery)}`, { method: 'POST' });
      if (res.ok) setAiResponse(await res.json());
    } catch (e) {}
  };

  return (
    <div style={{ display: 'flex', minHeight: '100vh', background: 'var(--bg-dark)' }}>
      {/* Sidebar Navigation */}
      <div style={{ width: '250px', background: 'var(--bg-sidebar)', padding: '24px 16px', borderRight: '1px solid var(--border-color)', display: 'flex', flexDirection: 'column', gap: '24px' }}>
        <div>
          <h1 style={{ color: '#f8fafc', fontSize: '1.2rem', fontWeight: 800, letterSpacing: '1px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <ShieldAlert size={22} color="var(--accent-primary)" /> HELLFORGE
          </h1>
          <p style={{ color: 'var(--text-dim)', fontSize: '0.75rem', marginTop: '4px', fontFamily: 'var(--font-mono)' }}>
            ATTACK SURFACE PLATFORM
          </p>
        </div>

        <nav style={{ display: 'flex', flexDirection: 'column', gap: '2px' }}>
          {[
            { id: 'overview', label: 'Overview', icon: Radio },
            { id: 'assets', label: 'Assets Inventory', icon: Server },
            { id: 'js_intel', label: 'JS Intelligence', icon: Terminal },
            { id: 'graph', label: 'Attack Graph', icon: Network },
            { id: 'findings', label: 'Vulnerabilities', icon: ShieldAlert },
            { id: 'schedules', label: 'Scan Schedules', icon: Layers },
            { id: 'plugins', label: 'Plugins SDK', icon: Cpu },
            { id: 'timeline', label: 'Attack Timeline', icon: Activity },
            { id: 'reports', label: 'Reports', icon: FileText },
            { id: 'ai', label: 'AI Copilot', icon: Bot },
          ].map((tab) => {
            const Icon = tab.icon;
            const active = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '10px',
                  padding: '9px 12px',
                  borderRadius: '6px',
                  background: active ? 'var(--bg-card)' : 'transparent',
                  color: active ? 'var(--text-main)' : 'var(--text-muted)',
                  border: active ? '1px solid var(--border-color)' : '1px solid transparent',
                  cursor: 'pointer',
                  fontWeight: active ? 600 : 400,
                  fontSize: '0.85rem',
                  textAlign: 'left'
                }}
              >
                <Icon size={16} color={active ? 'var(--accent-primary)' : 'var(--text-dim)'} /> {tab.label}
              </button>
            );
          })}
        </nav>

        <div style={{ marginTop: 'auto', padding: '12px', background: 'var(--bg-dark)', borderRadius: '6px', border: '1px solid var(--border-color)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
            <span className="live-dot"></span> TOPIC EVENTBUS ACTIVE
          </div>
        </div>
      </div>

      {/* Main Content Area */}
      <div style={{ flex: 1, padding: '24px 32px', overflowY: 'auto' }}>
        {/* Top Scan Bar */}
        <div className="pro-card" style={{ padding: '12px 20px', marginBottom: '24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', flex: 1, maxWidth: '600px' }}>
            <Search size={16} color="var(--text-dim)" />
            <input
              type="text"
              value={targetInput}
              onChange={(e) => setTargetInput(e.target.value)}
              placeholder="Enter target domain or host..."
              style={{
                background: 'transparent',
                border: 'none',
                color: 'var(--text-main)',
                fontSize: '0.95rem',
                width: '100%',
                outline: 'none',
                fontFamily: 'var(--font-mono)'
              }}
            />
          </div>
          <button
            onClick={handleStartScan}
            disabled={isScanning}
            style={{
              background: 'var(--accent-primary)',
              color: '#ffffff',
              border: 'none',
              padding: '8px 20px',
              borderRadius: '6px',
              fontWeight: 600,
              fontSize: '0.85rem',
              cursor: 'pointer'
            }}
          >
            {isScanning ? 'Scanning Target...' : 'Execute Scan'}
          </button>
        </div>

        {/* Tab Content */}
        {activeTab === 'overview' && (
          <div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px', marginBottom: '24px' }}>
              <div className="pro-card" style={{ padding: '20px' }}>
                <div style={{ color: 'var(--text-dim)', fontSize: '0.75rem', fontWeight: 600, letterSpacing: '0.5px' }}>TOTAL ASSETS</div>
                <div style={{ fontSize: '1.8rem', fontWeight: 700, marginTop: '6px', color: 'var(--text-main)' }}>{stats.total_assets}</div>
              </div>
              <div className="pro-card" style={{ padding: '20px' }}>
                <div style={{ color: 'var(--text-dim)', fontSize: '0.75rem', fontWeight: 600, letterSpacing: '0.5px' }}>VULNERABILITIES</div>
                <div style={{ fontSize: '1.8rem', fontWeight: 700, marginTop: '6px', color: 'var(--severity-critical)' }}>{stats.total_vulnerabilities}</div>
              </div>
              <div className="pro-card" style={{ padding: '20px' }}>
                <div style={{ color: 'var(--text-dim)', fontSize: '0.75rem', fontWeight: 600, letterSpacing: '0.5px' }}>AVG RISK SCORE</div>
                <div style={{ fontSize: '1.8rem', fontWeight: 700, marginTop: '6px', color: 'var(--severity-high)' }}>{stats.average_risk_score}/100</div>
              </div>
              <div className="pro-card" style={{ padding: '20px' }}>
                <div style={{ color: 'var(--text-dim)', fontSize: '0.75rem', fontWeight: 600, letterSpacing: '0.5px' }}>CRITICAL FINDINGS</div>
                <div style={{ fontSize: '1.8rem', fontWeight: 700, marginTop: '6px', color: 'var(--severity-critical)' }}>{stats.severity_breakdown.critical}</div>
              </div>
            </div>

            <div className="pro-card" style={{ padding: '20px', marginBottom: '24px' }}>
              <h3 style={{ fontSize: '0.95rem', marginBottom: '16px', color: 'var(--text-main)', fontWeight: 600 }}>Attack Surface Topology Graph</h3>
              <D3TopologyGraph data={graphData} />
            </div>
          </div>
        )}


        {activeTab === 'assets' && <AssetsFeature assets={assets} />}
        {activeTab === 'js_intel' && <JSIntelFeature />}
        {activeTab === 'findings' && <FindingsFeature findings={findings} />}
        {activeTab === 'schedules' && <SchedulesFeature />}
        {activeTab === 'reports' && <ReportsFeature />}

        {activeTab === 'graph' && (
          <div className="pro-card" style={{ padding: '20px' }}>
            <h3 style={{ fontSize: '0.95rem', marginBottom: '16px', fontWeight: 600 }}>Interactive Infrastructure Graph</h3>
            <D3TopologyGraph data={graphData} />
          </div>
        )}

        {activeTab === 'plugins' && (
          <div className="pro-card" style={{ padding: '20px' }}>
            <h3 style={{ fontSize: '0.95rem', marginBottom: '16px', fontWeight: 600 }}>Categorized Plugin Marketplace ({plugins.length})</h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '12px' }}>
              {plugins.map((p) => (
                <div key={p.name} style={{ padding: '14px', background: 'var(--bg-dark)', borderRadius: '6px', border: '1px solid var(--border-color)' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ fontWeight: 600, fontSize: '0.85rem', color: 'var(--text-main)', fontFamily: 'var(--font-mono)' }}>{p.name} v{p.version}</span>
                    <span className="badge badge-info">OFFICIAL</span>
                  </div>
                  <p style={{ color: 'var(--text-dim)', fontSize: '0.8rem', marginTop: '6px' }}>{p.description}</p>
                  <div style={{ marginTop: '8px', fontSize: '0.75rem', fontFamily: 'var(--font-mono)', color: 'var(--accent-primary)' }}>
                    Subscribed Topics: {p.subscriptions ? p.subscriptions.join(', ') : 'None'}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'timeline' && (
          <div className="pro-card" style={{ padding: '20px' }}>
            <h3 style={{ fontSize: '0.95rem', marginBottom: '16px', fontWeight: 600 }}>Attack Surface Timeline Tracking</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {timeline.length === 0 ? (
                <div style={{ padding: '24px', textAlign: 'center', color: 'var(--text-dim)', fontFamily: 'var(--font-mono)', fontSize: '0.85rem' }}>
                  No timeline events logged. Execute a scan to record pipeline activity.
                </div>
              ) : (
                timeline.map((t) => (
                  <div key={t.id} style={{ padding: '12px', background: 'var(--bg-dark)', borderRadius: '6px', border: '1px solid var(--border-color)', fontFamily: 'var(--font-mono)', fontSize: '0.8rem' }}>
                    <span style={{ color: 'var(--severity-high)', marginRight: '8px' }}>[{new Date(t.created_at).toLocaleTimeString()}]</span> <strong style={{ color: 'var(--text-main)' }}>{t.title}:</strong> {t.description}
                  </div>
                ))
              )}
            </div>
          </div>
        )}

        {activeTab === 'ai' && (
          <div className="pro-card" style={{ padding: '20px' }}>
            <h3 style={{ fontSize: '0.95rem', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px', fontWeight: 600, color: 'var(--text-main)' }}>
              <Bot size={18} color="var(--accent-primary)" /> HellForge AI Security Copilot
            </h3>
            <div style={{ display: 'flex', gap: '10px', marginBottom: '16px' }}>
              <input
                type="text"
                value={aiQuery}
                onChange={(e) => setAiQuery(e.target.value)}
                placeholder="Ask AI Copilot about threat vectors or remediation..."
                style={{ flex: 1, padding: '8px 12px', background: 'var(--bg-input)', border: '1px solid var(--border-color)', borderRadius: '6px', color: '#fff', outline: 'none', fontSize: '0.85rem' }}
              />
              <button
                onClick={handleAiAsk}
                style={{ padding: '8px 16px', background: 'var(--accent-primary)', color: '#ffffff', border: 'none', borderRadius: '6px', fontWeight: 600, fontSize: '0.85rem', cursor: 'pointer' }}
              >
                Analyze Threat Vector
              </button>
            </div>
            {aiResponse && (
              <div style={{ padding: '16px', background: 'var(--bg-dark)', borderRadius: '6px', border: '1px solid var(--border-color)' }}>
                <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'var(--font-mono)', fontSize: '0.8rem', color: 'var(--text-main)', lineHeight: 1.5 }}>{aiResponse.response}</pre>
              </div>
            )}
          </div>
        )}

      </div>
    </div>
  );
}
