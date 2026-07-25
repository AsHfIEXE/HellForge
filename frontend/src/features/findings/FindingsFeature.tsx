import React from 'react';

export const FindingsFeature: React.FC<{ findings: any[] }> = ({ findings }) => (
  <div className="glass-panel" style={{ padding: '24px' }}>
    <h3 style={{ fontSize: '1.2rem', marginBottom: '20px' }}>Security Findings & Misconfigurations ({findings.length})</h3>
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      {findings.map((f) => (
        <div key={f.id} style={{ padding: '16px', background: 'rgba(0,0,0,0.3)', borderRadius: '8px', borderLeft: f.severity === 'Critical' ? '4px solid var(--accent-red)' : '4px solid var(--accent-orange)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontWeight: 700, fontSize: '1rem' }}>{f.title}</span>
            <span className={f.severity === 'Critical' ? 'badge-critical' : 'badge-high'}>{f.severity}</span>
          </div>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginTop: '8px' }}>{f.description}</p>
          <div style={{ marginTop: '12px', fontSize: '0.85rem', color: 'var(--accent-cyan)', fontFamily: 'var(--font-mono)' }}>
            <strong>Remediation:</strong> {f.remediation}
          </div>
        </div>
      ))}
    </div>
  </div>
);
