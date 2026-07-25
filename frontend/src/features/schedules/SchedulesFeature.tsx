import React, { useState, useEffect } from 'react';
import { Calendar, Clock, Play, Plus, CheckCircle } from 'lucide-react';

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
      const res = await fetch(`http://localhost:8000/api/v1/schedules?domain=${newDomain}&cron=${cron}`, { method: 'POST' });
      if (res.ok) {
        setNewDomain('');
        fetchSchedules();
      }
    } catch (e) {}
  };

  return (
    <div className="glass-panel" style={{ padding: '24px' }}>
      <h3 style={{ fontSize: '1.2rem', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--accent-cyan)' }}>
        <Calendar /> Recurring Scan Schedules & Delta Tracking
      </h3>
      <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: '20px' }}>
        Configure continuous monitoring schedules and receive automated change-delta alerts.
      </p>

      {/* Schedule Creator Bar */}
      <div style={{ display: 'flex', gap: '12px', marginBottom: '24px' }}>
        <input
          type="text"
          value={newDomain}
          onChange={(e) => setNewDomain(e.target.value)}
          placeholder="Target Domain (e.g. example.com)"
          style={{ flex: 1, padding: '10px 14px', background: 'rgba(0,0,0,0.4)', border: '1px solid var(--border-color)', borderRadius: '8px', color: '#fff', outline: 'none' }}
        />
        <select
          value={cron}
          onChange={(e) => setCron(e.target.value)}
          style={{ padding: '10px 14px', background: 'rgba(0,0,0,0.4)', border: '1px solid var(--border-color)', borderRadius: '8px', color: '#fff', outline: 'none' }}
        >
          <option value="0 0 * * *">Daily ( midnight )</option>
          <option value="0 0 * * 0">Weekly ( Sunday )</option>
          <option value="0 */6 * * *">Every 6 Hours</option>
        </select>
        <button
          onClick={handleCreate}
          style={{ padding: '10px 20px', background: 'var(--accent-cyan)', color: '#090c10', border: 'none', borderRadius: '8px', fontWeight: 700, cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px' }}
        >
          <Plus size={16} /> Add Schedule
        </button>
      </div>

      {/* Schedules List */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
        {schedules.length === 0 ? (
          <div style={{ padding: '20px', textAlign: 'center', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
            No active schedules configured. Add a target domain above to enable continuous scanning.
          </div>
        ) : (
          schedules.map((s) => (
            <div key={s.id} style={{ padding: '16px', background: 'rgba(0,0,0,0.3)', borderRadius: '8px', border: '1px solid var(--border-color)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <div style={{ fontWeight: 700, fontSize: '1rem', color: 'var(--text-main)' }}>{s.target_domain}</div>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '4px', fontFamily: 'var(--font-mono)' }}>
                  <Clock size={12} style={{ marginRight: '4px' }} /> Schedule Cron: <code>{s.cron_expression}</code>
                </div>
              </div>
              <span className="badge-info" style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                <CheckCircle size={12} /> ACTIVE
              </span>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
