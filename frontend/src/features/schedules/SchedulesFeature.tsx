import React, { useState, useEffect } from 'react';
import { Calendar, Clock, Plus, CheckCircle } from 'lucide-react';

export const SchedulesFeature: React.FC = () => {
  const [schedules, setSchedules] = useState<any[]>([]);
  const [newDomain, setNewDomain] = useState('');
  const [cron, setCron] = useState('0 0 * * *');

  useEffect(() => {
    fetchSchedules();
  }, []);

  const fetchSchedules = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/v1/schedules');
      if (res.ok) setSchedules(await res.json());
    } catch (e) {}
  };

  const handleCreate = async () => {
    if (!newDomain) return;
    try {
      const res = await fetch(`http://localhost:8000/api/v1/schedules?domain=${encodeURIComponent(newDomain)}&cron=${encodeURIComponent(cron)}`, { method: 'POST' });
      if (res.ok) {
        setNewDomain('');
        fetchSchedules();
      }
    } catch (e) {}
  };

  return (
    <div className="pro-card" style={{ padding: '20px' }}>
      <h3 style={{ fontSize: '0.95rem', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '8px', fontWeight: 600, color: 'var(--text-main)' }}>
        <Calendar size={18} color="var(--accent-primary)" /> Recurring Scan Schedules & Delta Tracking
      </h3>
      <p style={{ color: 'var(--text-dim)', fontSize: '0.8rem', marginBottom: '20px' }}>
        Configure continuous monitoring schedules and receive automated change-delta alerts.
      </p>

      {/* Schedule Creator Bar */}
      <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
        <input
          type="text"
          value={newDomain}
          onChange={(e) => setNewDomain(e.target.value)}
          placeholder="Target Domain or Host (e.g. example.com)"
          style={{ flex: 1, padding: '8px 12px', background: 'var(--bg-input)', border: '1px solid var(--border-color)', borderRadius: '6px', color: '#fff', outline: 'none', fontFamily: 'var(--font-mono)', fontSize: '0.85rem' }}
        />
        <select
          value={cron}
          onChange={(e) => setCron(e.target.value)}
          style={{ padding: '8px 12px', background: 'var(--bg-input)', border: '1px solid var(--border-color)', borderRadius: '6px', color: '#fff', outline: 'none', fontSize: '0.85rem' }}
        >
          <option value="0 0 * * *">Daily ( Midnight )</option>
          <option value="0 0 * * 0">Weekly ( Sunday )</option>
          <option value="0 */6 * * *">Every 6 Hours</option>
        </select>
        <button
          onClick={handleCreate}
          style={{ padding: '8px 16px', background: 'var(--accent-primary)', color: '#ffffff', border: 'none', borderRadius: '6px', fontWeight: 600, fontSize: '0.85rem', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px' }}
        >
          <Plus size={16} /> Add Schedule
        </button>
      </div>

      {/* Schedules List */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
        {schedules.length === 0 ? (
          <div style={{ padding: '24px', textAlign: 'center', color: 'var(--text-dim)', fontFamily: 'var(--font-mono)', fontSize: '0.85rem' }}>
            No active continuous schedules configured. Enter a target above to register recurring scans.
          </div>
        ) : (
          schedules.map((s) => (
            <div key={s.id} style={{ padding: '14px', background: 'var(--bg-dark)', borderRadius: '6px', border: '1px solid var(--border-color)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <div style={{ fontWeight: 600, fontSize: '0.9rem', color: 'var(--text-main)' }}>{s.target_domain}</div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)', marginTop: '4px', fontFamily: 'var(--font-mono)' }}>
                  <Clock size={12} style={{ marginRight: '4px' }} /> Cron Expression: <code>{s.cron_expression}</code>
                </div>
              </div>
              <span className="badge badge-clean" style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                <CheckCircle size={12} /> ACTIVE
              </span>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
