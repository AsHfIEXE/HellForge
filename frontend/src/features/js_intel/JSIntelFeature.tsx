import React from 'react';
import { Code, Key, ShieldAlert, FileCode } from 'lucide-react';

export const JSIntelFeature: React.FC = () => {
  const sampleSecrets = [
    { type: 'AWS Access Key', val: 'AKIAIOSFODNN7EXAMPLE', loc: 'bundle.8f9a2.js:142', severity: 'High' },
    { type: 'JWT Token', val: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...', loc: 'auth.chunk.js:89', severity: 'Medium' },
    { type: 'Firebase DB URL', val: 'https://hellforge-prod.firebaseio.com', loc: 'config.js:12', severity: 'Info' }
  ];

  return (
    <div className="glass-panel" style={{ padding: '24px' }}>
      <h3 style={{ fontSize: '1.2rem', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--accent-cyan)' }}>
        <FileCode /> JavaScript Intelligence & Secret Mining
      </h3>
      <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: '20px' }}>
        Automated AST parsing and secret discovery inside fetched frontend JavaScript bundles.
      </p>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
        {sampleSecrets.map((s, idx) => (
          <div key={idx} style={{ padding: '16px', background: 'rgba(0,0,0,0.3)', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontWeight: 700, color: 'var(--accent-orange)', fontFamily: 'var(--font-mono)' }}>
                <Key size={14} style={{ marginRight: '6px' }} /> {s.type}
              </span>
              <span className={s.severity === 'High' ? 'badge-critical' : 'badge-info'}>{s.severity}</span>
            </div>
            <div style={{ marginTop: '8px', fontFamily: 'var(--font-mono)', fontSize: '0.85rem', color: 'var(--text-main)', background: '#090c10', padding: '8px', borderRadius: '4px' }}>
              {s.val}
            </div>
            <div style={{ marginTop: '6px', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
              Extracted from: <code>{s.loc}</code>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
