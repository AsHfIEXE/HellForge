import React, { useState, useEffect } from 'react';
import { Key, FileCode } from 'lucide-react';

export const JSIntelFeature: React.FC = () => {
  const [secrets, setSecrets] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSecrets();
  }, []);

  const fetchSecrets = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/v1/findings');
      if (res.ok) {
        const data = await res.json();
        // Filter JS miner & secret leak findings
        const secretFindings = data.filter((f: any) => 
          f.category === 'Secret Leak' || f.discovery_source === 'js_miner'
        );
        setSecrets(secretFindings);
      }
    } catch (e) {
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="pro-card" style={{ padding: '20px' }}>
      <h3 style={{ fontSize: '0.95rem', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '8px', fontWeight: 600, color: 'var(--text-main)' }}>
        <FileCode size={18} color="var(--accent-primary)" /> JavaScript Intelligence & Secret Mining
      </h3>
      <p style={{ color: 'var(--text-dim)', fontSize: '0.8rem', marginBottom: '20px' }}>
        Real-time AST parsing and credential discovery inside fetched frontend JavaScript bundles.
      </p>

      {loading ? (
        <div style={{ padding: '20px', textAlign: 'center', color: 'var(--text-dim)', fontFamily: 'var(--font-mono)', fontSize: '0.85rem' }}>
          Querying JS Intelligence database...
        </div>
      ) : secrets.length === 0 ? (
        <div style={{ padding: '24px', textAlign: 'center', color: 'var(--text-dim)', fontFamily: 'var(--font-mono)', fontSize: '0.85rem' }}>
          No exposed API keys or secrets detected in scanned JavaScript bundles. Execute a target scan to run real-time AST parsing.
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {secrets.map((s) => (
            <div key={s.id} style={{ padding: '16px', background: 'var(--bg-dark)', borderRadius: '6px', border: '1px solid var(--border-color)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontWeight: 600, color: 'var(--text-main)', fontFamily: 'var(--font-mono)', fontSize: '0.85rem', display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <Key size={14} color="var(--severity-high)" /> {s.title}
                </span>
                <span className={`badge ${s.severity === 'High' ? 'badge-high' : 'badge-low'}`}>{s.severity}</span>
              </div>
              <div style={{ marginTop: '8px', fontFamily: 'var(--font-mono)', fontSize: '0.8rem', color: 'var(--text-main)', background: 'var(--bg-card)', padding: '10px', borderRadius: '4px', border: '1px solid var(--border-subtle)' }}>
                {s.description}
              </div>
              <div style={{ marginTop: '8px', fontSize: '0.75rem', color: 'var(--text-dim)', fontFamily: 'var(--font-mono)' }}>
                Remediation: <span style={{ color: 'var(--accent-primary)' }}>{s.remediation}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
