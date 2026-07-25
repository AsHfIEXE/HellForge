import React, { useState, useEffect } from 'react';
import { FileText, Eye, Sparkles } from 'lucide-react';

export const ReportsFeature: React.FC = () => {
  const [reports, setReports] = useState<any[]>([]);
  const [targetDomain, setTargetDomain] = useState('');
  const [format, setFormat] = useState('html');
  const [activeReport, setActiveReport] = useState<any>(null);

  useEffect(() => {
    fetchReports();
  }, []);

  const fetchReports = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/v1/reports');
      if (res.ok) setReports(await res.json());
    } catch (e) {}
  };

  const handleGenerate = async () => {
    if (!targetDomain) return;
    try {
      const res = await fetch(`http://localhost:8000/api/v1/reports/generate?domain=${encodeURIComponent(targetDomain)}&format=${format}`, { method: 'POST' });
      if (res.ok) {
        const data = await res.json();
        setActiveReport(data);
        fetchReports();
      }
    } catch (e) {}
  };

  return (
    <div className="pro-card" style={{ padding: '20px' }}>
      <h3 style={{ fontSize: '0.95rem', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '8px', fontWeight: 600, color: 'var(--text-main)' }}>
        <FileText size={18} color="var(--accent-primary)" /> Executive & Technical Posture Reporting Engine
      </h3>
      <p style={{ color: 'var(--text-dim)', fontSize: '0.8rem', marginBottom: '20px' }}>
        Generate standalone styled HTML and Markdown security reports for executive stakeholders.
      </p>

      {/* Generator Form */}
      <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
        <input
          type="text"
          value={targetDomain}
          onChange={(e) => setTargetDomain(e.target.value)}
          placeholder="Target Domain or Scope Name"
          style={{ flex: 1, padding: '8px 12px', background: 'var(--bg-input)', border: '1px solid var(--border-color)', borderRadius: '6px', color: '#fff', outline: 'none', fontFamily: 'var(--font-mono)', fontSize: '0.85rem' }}
        />
        <select
          value={format}
          onChange={(e) => setFormat(e.target.value)}
          style={{ padding: '8px 12px', background: 'var(--bg-input)', border: '1px solid var(--border-color)', borderRadius: '6px', color: '#fff', outline: 'none', fontSize: '0.85rem' }}
        >
          <option value="html">HTML Report</option>
          <option value="markdown">Markdown Report</option>
        </select>
        <button
          onClick={handleGenerate}
          style={{ padding: '8px 16px', background: 'var(--accent-primary)', color: '#ffffff', border: 'none', borderRadius: '6px', fontWeight: 600, fontSize: '0.85rem', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px' }}
        >
          <Sparkles size={16} /> Generate Report
        </button>
      </div>

      {/* Active Report Preview */}
      {activeReport && (
        <div style={{ marginBottom: '20px', padding: '16px', background: 'var(--bg-dark)', borderRadius: '6px', border: '1px solid var(--border-color)' }}>
          <h4 style={{ color: 'var(--text-main)', fontSize: '0.85rem', fontWeight: 600, marginBottom: '10px' }}>{activeReport.title} Preview ({activeReport.format.toUpperCase()})</h4>
          <pre style={{ maxHeight: '250px', overflowY: 'auto', background: 'var(--bg-card)', padding: '12px', borderRadius: '4px', fontSize: '0.8rem', fontFamily: 'var(--font-mono)', color: 'var(--text-muted)', whiteSpace: 'pre-wrap', border: '1px solid var(--border-subtle)' }}>
            {activeReport.content}
          </pre>
        </div>
      )}

      {/* Generated Reports History */}
      <h4 style={{ fontSize: '0.85rem', color: 'var(--text-dim)', marginBottom: '10px', fontWeight: 600 }}>Recent Generated Reports</h4>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
        {reports.length === 0 ? (
          <div style={{ padding: '24px', textAlign: 'center', color: 'var(--text-dim)', fontFamily: 'var(--font-mono)', fontSize: '0.85rem' }}>
            No executive reports generated yet.
          </div>
        ) : (
          reports.map((r) => (
            <div key={r.id} style={{ padding: '10px 14px', background: 'var(--bg-dark)', borderRadius: '6px', border: '1px solid var(--border-color)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <span style={{ fontWeight: 500, fontSize: '0.85rem', color: 'var(--text-main)' }}>{r.title}</span>
                <span style={{ marginLeft: '12px', fontSize: '0.75rem', color: 'var(--accent-primary)', fontFamily: 'var(--font-mono)' }}>[{r.format.toUpperCase()}]</span>
              </div>
              <button
                onClick={() => setActiveReport(r)}
                style={{ background: 'transparent', border: '1px solid var(--border-color)', color: 'var(--text-muted)', padding: '4px 10px', borderRadius: '4px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '4px', fontSize: '0.75rem' }}
              >
                <Eye size={12} /> View
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
