import React from 'react';

export const AssetsFeature: React.FC<{ assets: any[] }> = ({ assets }) => (
  <div className="pro-card" style={{ padding: '20px' }}>
    <h3 style={{ fontSize: '0.95rem', marginBottom: '16px', fontWeight: 600 }}>Discovered Assets ({assets.length})</h3>
    <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontFamily: 'var(--font-mono)', fontSize: '0.85rem' }}>
      <thead>
        <tr style={{ borderBottom: '1px solid var(--border-color)', color: 'var(--text-dim)' }}>
          <th style={{ padding: '10px 12px' }}>SUBDOMAIN / ASSET</th>
          <th style={{ padding: '10px 12px' }}>RISK SCORE</th>
          <th style={{ padding: '10px 12px' }}>TAGS</th>
          <th style={{ padding: '10px 12px' }}>SOURCE</th>
        </tr>
      </thead>
      <tbody>
        {assets.length === 0 ? (
          <tr>
            <td colSpan={4} style={{ padding: '24px', textAlign: 'center', color: 'var(--text-dim)' }}>
              No assets discovered yet. Enter a target domain above to begin real-time scanning.
            </td>
          </tr>
        ) : (
          assets.map((a) => (
            <tr key={a.id} style={{ borderBottom: '1px solid var(--border-subtle)' }}>
              <td style={{ padding: '12px', fontWeight: 500, color: 'var(--text-main)' }}>{a.name}</td>
              <td style={{ padding: '12px' }}>
                <span className={a.risk_score > 60 ? 'badge badge-critical' : a.risk_score > 30 ? 'badge badge-high' : 'badge badge-low'}>
                  {a.risk_score}/100
                </span>
              </td>
              <td style={{ padding: '12px', color: 'var(--text-muted)' }}>{a.tags ? a.tags.join(', ') : 'none'}</td>
              <td style={{ padding: '12px', color: 'var(--text-dim)' }}>{a.discovery_source}</td>
            </tr>
          ))
        )}
      </tbody>
    </table>
  </div>
);

