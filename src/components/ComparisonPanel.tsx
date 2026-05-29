import React, { useEffect, useState } from 'react';
import { supabase } from '../lib/supabase';
import {
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
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
  ChevronDown,
  RefreshCw
} from 'lucide-react';

interface ComparisonPanelProps {
  farms: any[];
  gaps: any[];
}

export function ComparisonPanel({ farms, gaps }: ComparisonPanelProps) {
  // State for Unit A
  const [farmAId, setFarmAId] = useState<string | null>(null);
  const [kandangAId, setKandangAId] = useState<string | null>(null);
  const [dataA, setDataA] = useState<any[]>([]);
  const [loadingA, setLoadingA] = useState(false);

  // State for Unit B
  const [farmBId, setFarmBId] = useState<string | null>(null);
  const [kandangBId, setKandangBId] = useState<string | null>(null);
  const [dataB, setDataB] = useState<any[]>([]);
  const [loadingB, setLoadingB] = useState(false);
  const [lastSync, setLastSync] = useState<string | null>(null);

  // Derived selections
  const farmA = farms.find(f => f.id === farmAId);
  const farmB = farms.find(f => f.id === farmBId);

  const kandangA = farmA?.kandang?.find((k: any) => k.id === kandangAId);
  const kandangB = farmB?.kandang?.find((k: any) => k.id === kandangBId);

  // Fetching Data
  useEffect(() => {
    fetchLastSync();
    if (kandangAId) fetchUnitData(kandangAId, setDataA, setLoadingA);
    else setDataA([]);
  }, [kandangAId]);

  useEffect(() => {
    fetchLastSync();
    if (kandangBId) fetchUnitData(kandangBId, setDataB, setLoadingB);
    else setDataB([]);
  }, [kandangBId]);

  async function fetchLastSync() {
    try {
      const { data, error } = await supabase
        .from('weekly_production')
        .select('created_at')
        .order('created_at', { ascending: false })
        .limit(1);
      
      if (data && data.length > 0) {
        setLastSync(new Date(data[0].created_at).toLocaleString());
      }
    } catch (err) {
      console.error('Error fetching last sync:', err);
    }
  }

  async function fetchUnitData(id: string, setData: (d: any[]) => void, setLoading: (l: boolean) => void) {
    setLoading(true);
    try {
      const { data, error } = await supabase
        .from('weekly_production')
        .select('*')
        .eq('kandang_id', id)
        .not('hd_actual', 'is', null)
        .order('usia_minggu', { ascending: true });
      if (error) throw error;
      setData(data || []);
    } catch (err) {
      console.error('Error fetching unit data:', err);
    } finally {
      setLoading(false);
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
              <span style={{ fontWeight: 600, color: entry.color }}>{Number(entry.value).toFixed(2)}</span>
            </div>
          ))}
        </div>
      );
    }
    return null;
  };

  const UnitSelector = ({ label, farmId, setFarmId, kandangId, setKandangId, farm, color }: any) => (
    <div className="card" style={{ flex: 1, padding: '1.5rem', borderTop: `4px solid ${color}` }}>
      <h4 style={{ marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <BarChart3 size={18} color={color} />
        {label}
      </h4>
      <div style={{ display: 'flex', gap: '0.75rem' }}>
        <div style={{ position: 'relative', flex: 1 }}>
          <select 
            style={{ width: '100%', padding: '0.625rem 2.5rem 0.625rem 1.25rem', borderRadius: '10px', border: '1px solid var(--border)', backgroundColor: 'var(--card)', color: 'white', appearance: 'none', cursor: 'pointer', fontSize: '0.875rem' }}
            value={farmId || ''}
            onChange={(e) => { setFarmId(e.target.value); setKandangId(null); }}
          >
            <option value="">Select Farm</option>
            {farms.map(f => <option key={f.id} value={f.id}>{f.name}</option>)}
          </select>
          <ChevronDown size={14} style={{ position: 'absolute', right: '12px', top: '50%', transform: 'translateY(-50%)', pointerEvents: 'none', opacity: 0.5 }} />
        </div>
        <div style={{ position: 'relative', flex: 1 }}>
          <select 
            style={{ width: '100%', padding: '0.625rem 2.5rem 0.625rem 1.25rem', borderRadius: '10px', border: '1px solid var(--border)', backgroundColor: 'var(--card)', color: 'white', appearance: 'none', cursor: 'pointer', fontSize: '0.875rem', opacity: !farmId ? 0.5 : 1 }}
            value={kandangId || ''}
            onChange={(e) => setKandangId(e.target.value)}
            disabled={!farmId}
          >
            <option value="">Select Unit</option>
            {farm?.kandang?.map((k: any) => <option key={k.id} value={k.id}>{k.name}</option>)}
          </select>
          <ChevronDown size={14} style={{ position: 'absolute', right: '12px', top: '50%', transform: 'translateY(-50%)', pointerEvents: 'none', opacity: 0.5 }} />
        </div>
      </div>
    </div>
  );
  
  const ComparisonTable = () => {
    const latestA = dataA.length > 0 ? dataA[dataA.length - 1] : null;
    const latestB = dataB.length > 0 ? dataB[dataB.length - 1] : null;

    const rows = [
      { label: 'Week / Age', key: 'usia_minggu', unit: ' wks' },
      { label: 'Hen Day (HD)', key: 'hd_actual', unit: '%' },
      { label: 'Egg Weight', key: 'egg_weight_actual', unit: ' g' },
      { label: 'FCR', key: 'fcr_actual', unit: '' },
      { label: 'Feed Intake', key: 'pakan_g_per_ekor_hr', unit: ' g' },
      { label: 'Mortality', key: 'deplesi_pct', unit: '%' },
    ];

    return (
      <div className="card" style={{ padding: '0', overflow: 'hidden' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.875rem' }}>
          <thead>
            <tr style={{ backgroundColor: 'rgba(255,255,255,0.03)', borderBottom: '1px solid var(--border)' }}>
              <th style={{ padding: '1rem 1.5rem', fontWeight: 600, opacity: 0.7 }}>Metric</th>
              <th style={{ padding: '1rem 1.5rem', fontWeight: 600, color: 'var(--primary)' }}>{kandangA?.name || 'Unit A'}</th>
              <th style={{ padding: '1rem 1.5rem', fontWeight: 600, color: '#3b82f6' }}>{kandangB?.name || 'Unit B'}</th>
              <th style={{ padding: '1rem 1.5rem', fontWeight: 600, textAlign: 'right' }}>Variance</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row, i) => {
              const valA = latestA ? latestA[row.key] : null;
              const valB = latestB ? latestB[row.key] : null;
              const diff = (valA !== null && valB !== null) ? valA - valB : null;
              const isPositive = diff !== null && diff > 0;

              return (
                <tr key={i} style={{ borderBottom: i === rows.length - 1 ? 'none' : '1px solid var(--border)' }}>
                  <td style={{ padding: '1rem 1.5rem', fontWeight: 500, opacity: 0.9 }}>{row.label}</td>
                  <td style={{ padding: '1rem 1.5rem', fontWeight: 600 }}>{valA !== null ? `${Number(valA).toFixed(row.key === 'usia_minggu' ? 0 : 2)}${row.unit}` : '-'}</td>
                  <td style={{ padding: '1rem 1.5rem', fontWeight: 600 }}>{valB !== null ? `${Number(valB).toFixed(row.key === 'usia_minggu' ? 0 : 2)}${row.unit}` : '-'}</td>
                  <td style={{ padding: '1rem 1.5rem', textAlign: 'right', fontWeight: 700, color: diff === null ? 'inherit' : (isPositive ? 'var(--primary)' : 'var(--destructive)') }}>
                    {diff !== null ? (
                      <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-end', gap: '0.25rem' }}>
                        {isPositive ? '+' : ''}{diff.toFixed(2)}{row.unit}
                        {isPositive ? <TrendingUp size={14} /> : <TrendingUp size={14} style={{ transform: 'rotate(180deg)' }} />}
                      </span>
                    ) : '-'}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    );
  };

  const ComparisonChart = ({ title, icon, dataKey, unit, colorA, colorB, domain }: any) => (
    <div className="card" style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        {icon}
        <h4 style={{ margin: 0, fontSize: '0.95rem', fontWeight: 600 }}>{title}</h4>
      </div>
      <div style={{ height: '300px' }}>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
            <XAxis type="number" dataKey="usia_minggu" domain={['dataMin', 'dataMax']} stroke="rgba(255,255,255,0.3)" fontSize={11} tickLine={false} axisLine={false} />
            <YAxis stroke="rgba(255,255,255,0.3)" fontSize={11} tickLine={false} axisLine={false} domain={domain || ['auto', 'auto']} tickFormatter={(v) => `${v}${unit || ''}`} />
            <Tooltip content={<CustomTooltip />} />
            <Legend iconType="circle" wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
            {dataA.length > 0 && (
              <Line data={dataA} type="monotone" dataKey={dataKey} name={`A: ${kandangA?.name || 'Unit A'}`} stroke={colorA} strokeWidth={2.5} dot={{ r: 2 }} activeDot={{ r: 4 }} connectNulls />
            )}
            {dataB.length > 0 && (
              <Line data={dataB} type="monotone" dataKey={dataKey} name={`B: ${kandangB?.name || 'Unit B'}`} stroke={colorB} strokeWidth={2.5} dot={{ r: 2 }} activeDot={{ r: 4 }} connectNulls />
            )}
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: '-1rem' }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
          <h3 style={{ margin: 0, fontSize: '1.5rem', fontWeight: 700 }}>Unit Comparison</h3>
          {lastSync && (
            <p style={{ margin: 0, fontSize: '0.75rem', color: 'var(--muted-foreground)', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <RefreshCw size={12} className={loadingA || loadingB ? 'animate-spin' : ''} />
              Last sync: {lastSync}
            </p>
          )}
        </div>
      </div>

      <div style={{ display: 'flex', gap: '1.5rem' }}>
        <UnitSelector 
          label="Unit A" 
          farmId={farmAId} setFarmId={setFarmAId} 
          kandangId={kandangAId} setKandangId={setKandangAId} 
          farm={farmA} color="var(--primary)" 
        />
        <UnitSelector 
          label="Unit B" 
          farmId={farmBId} setFarmId={setFarmBId} 
          kandangId={kandangBId} setKandangId={setKandangBId} 
          farm={farmB} color="#3b82f6" 
        />
      </div>

      {(kandangAId || kandangBId) && <ComparisonTable />}


      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
        <ComparisonChart 
          title="Hen Day (HD%) Comparison" icon={<TrendingUp size={18} color="var(--primary)" />} 
          dataKey="hd_actual" unit="%" colorA="var(--primary)" colorB="#3b82f6" domain={[0, 100]} 
        />
        <ComparisonChart 
          title="Egg Weight (g) Comparison" icon={<Target size={18} color="var(--primary)" />} 
          dataKey="egg_weight_actual" unit="g" colorA="var(--primary)" colorB="#3b82f6" 
        />
        <ComparisonChart 
          title="Efficiency (FCR) Comparison" icon={<Zap size={18} color="var(--primary)" />} 
          dataKey="fcr_actual" colorA="var(--primary)" colorB="#3b82f6" 
        />
        <ComparisonChart 
          title="Feed Intake (g/bird) Comparison" icon={<Utensils size={18} color="var(--primary)" />} 
          dataKey="pakan_g_per_ekor_hr" unit="g" colorA="var(--primary)" colorB="#3b82f6" 
        />
        <ComparisonChart 
          title="Mortality (Deplesi %) Comparison" icon={<Skull size={18} color="var(--destructive)" />} 
          dataKey="deplesi_pct" unit="%" colorA="var(--primary)" colorB="#3b82f6" 
        />
      </div>

      {(!kandangAId && !kandangBId) && (
        <div className="card" style={{ padding: '4rem', textAlign: 'center', borderStyle: 'dashed', borderWidth: '2px' }}>
          <div style={{ fontSize: '1.1rem', fontWeight: 600, marginBottom: '0.5rem' }}>Start Comparing Units</div>
          <p style={{ opacity: 0.5, maxWidth: '400px', margin: '0 auto' }}>Select Farm and Kandang units above to see side-by-side production data and performance analysis.</p>
        </div>
      )}
    </div>
  );
}
