import React, { useEffect, useState } from 'react';
import { supabase } from '../lib/supabase';
import {
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  AreaChart,
  Area,
  LineChart,
  Line,
  Legend
} from 'recharts';
import { 
  TrendingUp, 
  Target, 
  Zap, 
  Utensils, 
  Skull,
  BarChart3,
  RefreshCw,
  ChevronDown
} from 'lucide-react';

interface AnalyticsPanelProps {
  farms: any[];
  initialFarmId?: string | null;
  initialKandangId?: string | null;
}

export function AnalyticsPanel({ farms, initialFarmId, initialKandangId }: AnalyticsPanelProps) {
  const [selectedFarmId, setSelectedFarmId] = useState<string | null>(initialFarmId ?? null);
  const [selectedKandangId, setSelectedKandangId] = useState<string | null>(initialKandangId ?? null);
  const [analyticsData, setAnalyticsData] = useState<any[]>([]);
  const [fetching, setFetching] = useState(false);

  // Sync when deep-linked from Gap Warnings tab
  useEffect(() => {
    if (initialFarmId) setSelectedFarmId(initialFarmId);
    if (initialKandangId) setSelectedKandangId(initialKandangId);
  }, [initialFarmId, initialKandangId]);

  const selectedFarm = farms.find(f => f.id === selectedFarmId);
  const availableKandangs = selectedFarm?.kandang || [];

  useEffect(() => {
    if (selectedKandangId) {
      fetchAnalyticsData(selectedKandangId);
    } else {
      setAnalyticsData([]);
    }
  }, [selectedKandangId]);

  async function fetchAnalyticsData(kandangId: string) {
    setFetching(true);
    try {
      const { data, error } = await supabase
        .from('weekly_production')
        .select('*')
        .eq('kandang_id', kandangId)
        .order('usia_minggu', { ascending: true });
      
      if (error) throw error;
      setAnalyticsData(data || []);
    } catch (error) {
      console.error('Error fetching analytics:', error);
    } finally {
      setFetching(false);
    }
  }

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="glass" style={{ padding: '1rem', border: '1px solid var(--border)', borderRadius: '12px', boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.5)' }}>
          <p style={{ margin: 0, fontWeight: 700, color: 'var(--primary)', marginBottom: '0.5rem' }}>Week {label}</p>
          {payload.map((entry: any, index: number) => (
            <div key={index} style={{ display: 'flex', justifyContent: 'space-between', gap: '2rem', fontSize: '0.8125rem' }}>
              <span style={{ color: 'var(--muted-foreground)' }}>{entry.name}:</span>
              <span style={{ fontWeight: 600, color: entry.color }}>{entry.value.toLocaleString()}</span>
            </div>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      {/* Selectors Bar */}
      <div className="glass" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1.25rem 2rem', borderRadius: '1.5rem', border: '1px solid var(--border)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <BarChart3 size={24} color="var(--primary)" />
          <h3 style={{ margin: 0, fontSize: '1.25rem', fontWeight: 700 }}>Production Intel</h3>
        </div>
        
        <div style={{ display: 'flex', gap: '1rem' }}>
          <div style={{ position: 'relative' }}>
            <select 
              style={{ padding: '0.625rem 2.5rem 0.625rem 1.25rem', borderRadius: '12px', border: '1px solid var(--border)', backgroundColor: 'var(--card)', color: 'white', appearance: 'none', cursor: 'pointer', fontSize: '0.875rem', minWidth: '180px' }}
              value={selectedFarmId || ''}
              onChange={(e) => {
                setSelectedFarmId(e.target.value);
                setSelectedKandangId(null);
              }}
            >
              <option value="">Select Farm</option>
              {farms.map(f => <option key={f.id} value={f.id}>{f.name}</option>)}
            </select>
            <ChevronDown size={16} style={{ position: 'absolute', right: '12px', top: '50%', transform: 'translateY(-50%)', pointerEvents: 'none', opacity: 0.5 }} />
          </div>

          <div style={{ position: 'relative' }}>
            <select 
              style={{ padding: '0.625rem 2.5rem 0.625rem 1.25rem', borderRadius: '12px', border: '1px solid var(--border)', backgroundColor: 'var(--card)', color: 'white', appearance: 'none', cursor: 'pointer', fontSize: '0.875rem', minWidth: '180px', opacity: !selectedFarmId ? 0.5 : 1 }}
              value={selectedKandangId || ''}
              onChange={(e) => setSelectedKandangId(e.target.value)}
              disabled={!selectedFarmId}
            >
              <option value="">Select Unit</option>
              {availableKandangs.map((k: any) => <option key={k.id} value={k.id}>{k.name}</option>)}
            </select>
            <ChevronDown size={16} style={{ position: 'absolute', right: '12px', top: '50%', transform: 'translateY(-50%)', pointerEvents: 'none', opacity: 0.5 }} />
          </div>
        </div>
      </div>

      {!selectedKandangId ? (
        <div className="card" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '500px', borderRadius: '2rem', borderStyle: 'dashed', borderWidth: '2px' }}>
          <div style={{ backgroundColor: 'rgba(191, 245, 73, 0.05)', padding: '2rem', borderRadius: '50%', marginBottom: '1.5rem' }}>
            <Target size={48} color="rgba(191, 245, 73, 0.3)" />
          </div>
          <h4 style={{ fontSize: '1.25rem', fontWeight: 600, marginBottom: '0.5rem' }}>No Unit Selected</h4>
          <p style={{ color: 'var(--muted-foreground)', textAlign: 'center', maxWidth: '300px' }}>Select a farm and kandang unit above to load historical performance data.</p>
        </div>
      ) : fetching ? (
        <div className="card" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '500px', borderRadius: '2rem' }}>
          <RefreshCw className="animate-spin" size={40} color="var(--primary)" />
          <p style={{ marginTop: '1.5rem', color: 'var(--muted-foreground)' }}>Crunching data points...</p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
          
          {/* HD% Chart */}
          <ChartCard 
            title="% Hen Day Performance" 
            subtitle="Actual vs Standard Yield" 
            icon={<TrendingUp size={18} color="#2563eb" />}
          >
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={analyticsData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                <XAxis dataKey="usia_minggu" stroke="rgba(255,255,255,0.3)" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="rgba(255,255,255,0.3)" fontSize={12} tickLine={false} axisLine={false} domain={[0, 100]} />
                <Tooltip content={<CustomTooltip />} />
                <Legend iconType="circle" wrapperStyle={{ paddingTop: '20px', fontSize: '12px' }} />
                <Line type="monotone" dataKey="hd_actual" name="Actual HD%" stroke="#2563eb" strokeWidth={3} dot={{ r: 3, fill: '#2563eb', strokeWidth: 0 }} activeDot={{ r: 6, strokeWidth: 0 }} />
                <Line type="monotone" dataKey="hd_std" name="Standard HD%" stroke="#ef4444" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </ChartCard>

          {/* Egg Weight Chart (Grams) */}
          <ChartCard 
            title="Egg Weight (Berat Telur)" 
            subtitle="Grams per egg" 
            icon={<Target size={18} color="#d97706" />}
          >
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={analyticsData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                <XAxis dataKey="usia_minggu" stroke="rgba(255,255,255,0.3)" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="rgba(255,255,255,0.3)" fontSize={12} tickLine={false} axisLine={false} domain={['auto', 'auto']} />
                <Tooltip content={<CustomTooltip />} />
                <Legend iconType="circle" wrapperStyle={{ paddingTop: '20px', fontSize: '12px' }} />
                <Line type="monotone" dataKey="egg_weight_actual" name="Actual EW (g)" stroke="#d97706" strokeWidth={3} dot={{ r: 3, fill: '#d97706', strokeWidth: 0 }} activeDot={{ r: 6, strokeWidth: 0 }} />
                <Line type="monotone" dataKey="egg_weight_std" name="Standard EW (g)" stroke="#991b1b" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </ChartCard>

          {/* Berat Telur Chart (Kg/1000) */}
          <ChartCard 
            title="Berat Telur (Kg/1000)" 
            subtitle="Actual vs Standard Weight" 
            icon={<Zap size={18} color="#f97316" />}
          >
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={analyticsData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                <XAxis dataKey="usia_minggu" stroke="rgba(255,255,255,0.3)" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="rgba(255,255,255,0.3)" fontSize={12} tickLine={false} axisLine={false} domain={['auto', 'auto']} />
                <Tooltip content={<CustomTooltip />} />
                <Legend iconType="circle" wrapperStyle={{ paddingTop: '20px', fontSize: '12px' }} />
                <Line type="monotone" dataKey="egg_mass_actual" name="Actual Weight (Kg)" stroke="#f97316" strokeWidth={3} dot={{ r: 3, fill: '#f97316', strokeWidth: 0 }} activeDot={{ r: 6, strokeWidth: 0 }} />
                <Line type="monotone" dataKey="egg_mass_std" name="Std Weight (Kg)" stroke="rgba(249,115,22,0.4)" strokeDasharray="5 5" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </ChartCard>

          {/* FCR Chart */}
          <ChartCard 
            title="Efficiency (FCR)" 
            subtitle="Weekly vs Cumulative performance" 
            icon={<Target size={18} color="#22c55e" />}
          >
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={analyticsData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                <XAxis dataKey="usia_minggu" stroke="rgba(255,255,255,0.3)" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="rgba(255,255,255,0.3)" fontSize={12} tickLine={false} axisLine={false} domain={['auto', 'auto']} />
                <Tooltip content={<CustomTooltip />} />
                <Legend iconType="circle" wrapperStyle={{ paddingTop: '20px', fontSize: '12px' }} />
                <Line type="monotone" dataKey="fcr_actual" name="Weekly FCR" stroke="#22c55e" strokeWidth={3} dot={{ r: 3, fill: '#22c55e', strokeWidth: 0 }} activeDot={{ r: 6, strokeWidth: 0 }} />
                <Line type="monotone" dataKey="fcr_std" name="Standard FCR" stroke="#f59e0b" strokeWidth={2} strokeDasharray="5 5" dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </ChartCard>

          {/* Feed Consumption */}
          <ChartCard 
            title="Feed Intake (Konsumsi Pakan)" 
            subtitle="Grams per ekor per day" 
            icon={<Utensils size={18} color="#a855f7" />}
          >
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={analyticsData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                <XAxis dataKey="usia_minggu" stroke="rgba(255,255,255,0.3)" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="rgba(255,255,255,0.3)" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip content={<CustomTooltip />} />
                <Legend iconType="circle" wrapperStyle={{ paddingTop: '20px', fontSize: '12px' }} />
                <Line type="monotone" dataKey="pakan_g_per_ekor_hr" name="Actual Feed" stroke="#a855f7" strokeWidth={3} dot={{ r: 3, fill: '#a855f7', strokeWidth: 0 }} activeDot={{ r: 6, strokeWidth: 0 }} />
                <Line type="monotone" dataKey="pakan_std" name="Std Feed" stroke="rgba(168,85,247,0.4)" strokeDasharray="5 5" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </ChartCard>

          {/* Mortality / Deplesi (Full Width) */}
          <ChartCard 
            title="Mortality & Depletion (Deplesi Cumm)" 
            subtitle="Cumulative depletion percentage" 
            icon={<Skull size={18} color="#ef4444" />}
          >
            <ResponsiveContainer width="100%" height={400}>
              <AreaChart data={analyticsData}>
                <defs>
                  <linearGradient id="colorDep" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#ef4444" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                <XAxis dataKey="usia_minggu" stroke="rgba(255,255,255,0.3)" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="rgba(255,255,255,0.3)" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip content={<CustomTooltip />} />
                <Legend iconType="circle" wrapperStyle={{ paddingTop: '20px', fontSize: '12px' }} />
                <Area type="monotone" dataKey="deplesi_pct" name="Cumulative Depletion %" stroke="#ef4444" strokeWidth={3} fillOpacity={1} fill="url(#colorDep)" />
              </AreaChart>
            </ResponsiveContainer>
          </ChartCard>

        </div>
      )}
    </div>
  );
}

// Helper wrapper for Chart Items
function ChartCard({ title, subtitle, icon, children }: { title: string, subtitle: string, icon: React.ReactNode, children: React.ReactNode }) {
  return (
    <div className="card" style={{ padding: '1.5rem 2rem', borderRadius: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
            {icon}
            <h4 style={{ margin: 0, fontSize: '1rem', fontWeight: 600 }}>{title}</h4>
          </div>
          <p style={{ margin: 0, fontSize: '0.75rem', color: 'var(--muted-foreground)' }}>{subtitle}</p>
        </div>
      </div>
      {children}
    </div>
  );
}


