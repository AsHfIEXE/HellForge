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
    total_projects: 1,
    total_targets: 1,
    total_assets: 5,
    total_vulnerabilities: 2,
    average_risk_score: 55.0,
    severity_breakdown: { critical: 1, high: 1, medium: 0, low: 0 }
  });
  const [assets, setAssets] = useState<any[]>([]);
  const [findings, setFindings] = useState<any[]>([]);
  const [graphData, setGraphData] = useState<any>({ nodes: [], links: [] });
  const [plugins, setPlugins] = useState<any[]>([]);
  const [timeline, setTimeline] = useState<any[]>([]);
  const [targetInput, setTargetInput] = useState('example.com');
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
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      {/* Sidebar Navigation */}
      <div className="glass-panel" style={{ width: '260px', padding: '20px', borderRadius: '0', borderRight: '1px solid var(--border-color)', display: 'flex', flexDirection: 'column', gap: '24px' }}>
        <div>
          <h1 style={{ color: 'var(--accent-red)', fontSize: '1.4rem', fontWeight: 800, letterSpacing: '1px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <ShieldAlert size={24} /> HELLFORGE
          </h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.75rem', marginTop: '4px', fontFamily: 'var(--font-mono)' }}>
            Build the attack surface.
          </p>
        </div>

        <nav style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
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
                  gap: '12px',
                  padding: '10px 14px',
                  borderRadius: '8px',
                  background: active ? 'rgba(0, 240, 255, 0.1)' : 'transparent',
                  color: active ? 'var(--accent-cyan)' : 'var(--text-muted)',
                  border: active ? '1px solid rgba(0, 240, 255, 0.3)' : '1px solid transparent',
                  cursor: 'pointer',
                  fontWeight: 600,
                  fontSize: '0.9rem',
                  textAlign: 'left'
                }}
              >
                <Icon size={18} /> {tab.label}
              </button>
            );
          })}
        </nav>


        <div style={{ marginTop: 'auto', padding: '12px', background: 'rgba(0,0,0,0.4)', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
            <span className="live-indicator"></span> Split Topic Bus Active
          </div>
        </div>
      </div>

      {/* Main Content Area */}
      <div style={{ flex: 1, padding: '32px', overflowY: 'auto' }}>
        {/* Top Scan Bar */}
        <div className="glass-panel" style={{ padding: '16px 24px', marginBottom: '24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', flex: 1, maxWidth: '600px' }}>
            <Search size={18} color="var(--text-muted)" />
            <input
              type="text"
              value={targetInput}
              onChange={(e) => setTargetInput(e.target.value)}
              placeholder="Enter target domain (e.g. example.com)"
              style={{
                background: 'transparent',
                border: 'none',
                color: 'var(--text-main)',
                fontSize: '1rem',
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
              background: 'linear-gradient(135deg, var(--accent-red), var(--accent-orange))',
              color: '#fff',
              border: 'none',
              padding: '10px 24px',
              borderRadius: '8px',
              fontWeight: 700,
              cursor: 'pointer',
              boxShadow: '0 0 15px rgba(255, 59, 92, 0.4)'
            }}
          >
            {isScanning ? 'Executing Pipeline...' : 'Launch Scan'}
          </button>
        </div>

        {/* Tab Content */}
        {activeTab === 'overview' && (
          <div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '20px', marginBottom: '24px' }}>
              <div className="glass-panel" style={{ padding: '20px' }}>
                <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>TOTAL ASSETS</div>
                <div style={{ fontSize: '2rem', fontWeight: 800, marginTop: '8px', color: 'var(--accent-cyan)' }}>{stats.total_assets}</div>
              </div>
              <div className="glass-panel" style={{ padding: '20px' }}>
                <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>FINDINGS</div>
                <div style={{ fontSize: '2rem', fontWeight: 800, marginTop: '8px', color: 'var(--accent-red)' }}>{stats.total_vulnerabilities}</div>
              </div>
              <div className="glass-panel" style={{ padding: '20px' }}>
                <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>AVERAGE RISK SCORE</div>
                <div style={{ fontSize: '2rem', fontWeight: 800, marginTop: '8px', color: 'var(--accent-orange)' }}>{stats.average_risk_score}/100</div>
              </div>
              <div className="glass-panel" style={{ padding: '20px' }}>
                <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>CRITICAL SEVERITY</div>
                <div style={{ fontSize: '2rem', fontWeight: 800, marginTop: '8px', color: 'var(--accent-red)' }}>{stats.severity_breakdown.critical}</div>
              </div>
            </div>

            <div className="glass-panel" style={{ padding: '24px', marginBottom: '24px' }}>
              <h3 style={{ fontSize: '1.1rem', marginBottom: '16px', color: 'var(--accent-cyan)' }}>Attack Surface Network Topology</h3>
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
          <div className="glass-panel" style={{ padding: '24px' }}>
            <h3 style={{ fontSize: '1.2rem', marginBottom: '20px' }}>Interactive Infrastructure Graph</h3>
            <D3TopologyGraph data={graphData} />
          </div>
        )}


        {activeTab === 'plugins' && (
          <div className="glass-panel" style={{ padding: '24px' }}>
            <h3 style={{ fontSize: '1.2rem', marginBottom: '20px' }}>Categorized Plugin Marketplace ({plugins.length})</h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '16px' }}>
              {plugins.map((p) => (
                <div key={p.name} style={{ padding: '16px', background: 'rgba(0,0,0,0.3)', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ fontWeight: 700, color: 'var(--accent-cyan)' }}>{p.name} v{p.version}</span>
                    <span className="badge-info">OFFICIAL</span>
                  </div>
                  <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginTop: '8px' }}>{p.description}</p>
                  <div style={{ marginTop: '8px', fontSize: '0.75rem', fontFamily: 'var(--font-mono)', color: 'var(--accent-purple)' }}>
                    Subscribed Topics: {p.subscriptions ? p.subscriptions.join(', ') : 'None'}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'timeline' && (
          <div className="glass-panel" style={{ padding: '24px' }}>
            <h3 style={{ fontSize: '1.2rem', marginBottom: '20px' }}>Attack Surface Timeline Tracking</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {timeline.map((t) => (
                <div key={t.id} style={{ padding: '14px', background: 'rgba(0,0,0,0.3)', borderRadius: '8px', fontFamily: 'var(--font-mono)', fontSize: '0.85rem' }}>
                  <span style={{ color: 'var(--accent-orange)' }}>[{new Date(t.created_at).toLocaleTimeString()}]</span> <strong style={{ color: 'var(--text-main)' }}>{t.title}:</strong> {t.description}
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'ai' && (
          <div className="glass-panel" style={{ padding: '24px' }}>
            <h3 style={{ fontSize: '1.2rem', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--accent-purple)' }}>
              <Bot /> HellForge AI Security Copilot
            </h3>
            <div style={{ display: 'flex', gap: '12px', marginBottom: '20px' }}>
              <input
                type="text"
                value={aiQuery}
                onChange={(e) => setAiQuery(e.target.value)}
                placeholder="Ask AI Copilot about threat vectors or remediation..."
                style={{ flex: 1, padding: '10px 14px', background: 'rgba(0,0,0,0.4)', border: '1px solid var(--border-color)', borderRadius: '8px', color: '#fff', outline: 'none' }}
              />
              <button
                onClick={handleAiAsk}
                style={{ padding: '10px 20px', background: 'var(--accent-purple)', color: '#fff', border: 'none', borderRadius: '8px', fontWeight: 700, cursor: 'pointer' }}
              >
                Analyze Threat Vector
              </button>
            </div>
            {aiResponse && (
              <div style={{ padding: '20px', background: 'rgba(0,0,0,0.4)', borderRadius: '8px', border: '1px solid var(--accent-purple)' }}>
                <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'var(--font-mono)', fontSize: '0.9rem', color: 'var(--text-main)' }}>{aiResponse.response}</pre>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
