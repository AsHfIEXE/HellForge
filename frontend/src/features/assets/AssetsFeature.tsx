import React from 'react';

export const AssetsFeature: React.FC<{ assets: any[] }> = ({ assets }) => (
  <div className="glass-panel" style={{ padding: '24px' }}>
    <h3 style={{ fontSize: '1.2rem', marginBottom: '20px' }}>Discovered Assets ({assets.length})</h3>
    <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontFamily: 'var(--font-mono)' }}>
      <thead>
        <tr style={{ borderBottom: '1px solid var(--border-color)', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
          <th style={{ padding: '12px' }}>SUBDOMAIN / ASSET</th>
          <th style={{ padding: '12px' }}>RISK SCORE</th>
          <th style={{ padding: '12px' }}>TAGS</th>
          <th style={{ padding: '12px' }}>SOURCE</th>
        </tr>
      </thead>
      <tbody>
        {assets.map((a) => (
          <tr key={a.id} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
            <td style={{ padding: '14px 12px', fontWeight: 600, color: 'var(--accent-cyan)' }}>{a.name}</td>
            <td style={{ padding: '14px 12px' }}>
              <span className={a.risk_score > 60 ? 'badge-critical' : 'badge-info'}>{a.risk_score}/100</span>
            </td>
            <td style={{ padding: '14px 12px' }}>{a.tags ? a.tags.join(', ') : 'none'}</td>
            <td style={{ padding: '14px 12px', color: 'var(--text-muted)' }}>{a.discovery_source}</td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
);
