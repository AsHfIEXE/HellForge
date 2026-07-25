import React from 'react';

export const FindingsFeature: React.FC<{ findings: any[] }> = ({ findings }) => (
  <div className="pro-card" style={{ padding: '20px' }}>
    <h3 style={{ fontSize: '0.95rem', marginBottom: '16px', fontWeight: 600 }}>Vulnerabilities & Misconfigurations ({findings.length})</h3>
    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
      {findings.length === 0 ? (
        <div style={{ padding: '24px', textAlign: 'center', color: 'var(--text-dim)', fontFamily: 'var(--font-mono)', fontSize: '0.85rem' }}>
          No security findings logged. Scan a target host to run real-time vulnerability audits.
        </div>
      ) : (
        findings.map((f) => (
          <div key={f.id} style={{ padding: '16px', background: 'var(--bg-dark)', borderRadius: '6px', border: '1px solid var(--border-color)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontWeight: 600, fontSize: '0.9rem', color: 'var(--text-main)' }}>{f.title}</span>
              <span className={`badge ${f.severity === 'Critical' ? 'badge-critical' : f.severity === 'High' ? 'badge-high' : f.severity === 'Medium' ? 'badge-medium' : 'badge-low'}`}>
                {f.severity}
              </span>
            </div>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginTop: '6px', lineHeight: 1.5 }}>{f.description}</p>
            <div style={{ marginTop: '10px', fontSize: '0.8rem', color: 'var(--accent-primary)', fontFamily: 'var(--font-mono)' }}>
              <strong>Remediation:</strong> {f.remediation}
            </div>
          </div>
        ))
      )}
    </div>
  </div>
);

