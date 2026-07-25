import React, { useState, useEffect } from 'react';
import { FileText, Download, Eye, Sparkles } from 'lucide-react';

export const ReportsFeature: React.FC = () => {
  const [reports, setReports] = useState<any[]>([]);
  const [targetDomain, setTargetDomain] = useState('example.com');
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
      const res = await fetch(`http://localhost:8000/api/v1/reports/generate?domain=${targetDomain}&format=${format}`, { method: 'POST' });
      if (res.ok) {
        const data = await res.json();
        setActiveReport(data);
        fetchReports();
      }
    } catch (e) {}
  };

  return (
    <div className="glass-panel" style={{ padding: '24px' }}>
      <h3 style={{ fontSize: '1.2rem', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--accent-cyan)' }}>
        <FileText /> Executive & Technical Posture Reporting Engine
      </h3>
      <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: '20px' }}>
        Generate standalone styled HTML and Markdown security reports for executive stakeholders.
      </p>

      {/* Generator Form */}
      <div style={{ display: 'flex', gap: '12px', marginBottom: '24px' }}>
        <input
          type="text"
          value={targetDomain}
          onChange={(e) => setTargetDomain(e.target.value)}
          placeholder="Target Domain"
          style={{ flex: 1, padding: '10px 14px', background: 'rgba(0,0,0,0.4)', border: '1px solid var(--border-color)', borderRadius: '8px', color: '#fff', outline: 'none' }}
        />
        <select
          value={format}
          onChange={(e) => setFormat(e.target.value)}
          style={{ padding: '10px 14px', background: 'rgba(0,0,0,0.4)', border: '1px solid var(--border-color)', borderRadius: '8px', color: '#fff', outline: 'none' }}
        >
          <option value="html">HTML Report</option>
          <option value="markdown">Markdown Report</option>
        </select>
        <button
          onClick={handleGenerate}
          style={{ padding: '10px 20px', background: 'var(--accent-purple)', color: '#fff', border: 'none', borderRadius: '8px', fontWeight: 700, cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px' }}
        >
          <Sparkles size={16} /> Generate Report
        </button>
      </div>

      {/* Active Report Preview */}
      {activeReport && (
        <div style={{ marginBottom: '24px', padding: '20px', background: 'rgba(0,0,0,0.4)', borderRadius: '8px', border: '1px solid var(--accent-purple)' }}>
          <h4 style={{ color: 'var(--accent-cyan)', marginBottom: '12px' }}>{activeReport.title} Preview ({activeReport.format.toUpperCase()})</h4>
          <pre style={{ maxHeight: '250px', overflowY: 'auto', background: '#090c10', padding: '14px', borderRadius: '6px', fontSize: '0.85rem', fontFamily: 'var(--font-mono)', color: 'var(--text-main)', whiteSpace: 'pre-wrap' }}>
            {activeReport.content}
          </pre>
        </div>
      )}

      {/* Generated Reports History */}
      <h4 style={{ fontSize: '1rem', color: 'var(--text-muted)', marginBottom: '12px' }}>Recent Generated Reports</h4>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
        {reports.map((r) => (
          <div key={r.id} style={{ padding: '12px 16px', background: 'rgba(0,0,0,0.3)', borderRadius: '8px', border: '1px solid var(--border-color)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <span style={{ fontWeight: 600 }}>{r.title}</span>
              <span style={{ marginLeft: '12px', fontSize: '0.75rem', color: 'var(--accent-cyan)', fontFamily: 'var(--font-mono)' }}>[{r.format.toUpperCase()}]</span>
            </div>
            <button
              onClick={() => setActiveReport(r)}
              style={{ background: 'transparent', border: '1px solid var(--border-color)', color: 'var(--text-muted)', padding: '6px 12px', borderRadius: '6px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '4px', fontSize: '0.8rem' }}
            >
              <Eye size={14} /> View
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};
