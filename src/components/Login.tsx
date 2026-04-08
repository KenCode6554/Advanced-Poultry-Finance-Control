import React, { useState } from 'react';
import { supabase } from '../lib/supabase';
import { Lock, Mail, AlertCircle, Loader2 } from 'lucide-react';

export function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const { error } = await supabase.auth.signInWithPassword({
        email,
        password,
      });

      if (error) {
        setError(error.message);
      }
    } catch (err: any) {
      setError(err.message || 'An unexpected error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      {/* Left Section: Visual Anchor */}
      <div className="login-left">
        {/* Background Image */}
        <img 
          src="https://lh3.googleusercontent.com/aida-public/AB6AXuCVETdIltEU-ROY7LJ9lzXgF-qtRinJaBhNx2rEcSf_UMNLdevkRfILIpuVGAgbgkfdfqdv7vuGGeiz7UZZJmzahgYHFn08Sxs1ujQG3jl3piu22ANN7fXkVuAaffCCIJA5srKikjNrQ7GedImCu7RqdS5pkMM6US_RnPqQX09fTilNtHf13B5E4pe5CpZVb_YWSBM3EEth6XduHaDHDKkm4n9XQUX9YaurcQiscBVt2yBsPSjas-Qrg6ubg2RHzbPyArZqt2lYnkM" 
          alt="Modern poultry farm" 
          style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover' }}
        />
        {/* Overlay */}
        <div style={{ position: 'absolute', inset: 0, backgroundColor: 'rgba(16, 34, 19, 0.6)', mixBlendMode: 'multiply' }} />
        <div style={{ position: 'absolute', inset: 0, background: 'linear-gradient(to top, rgba(16, 34, 19, 0.9), transparent)' }} />
        
        {/* Content over image */}
        <div style={{ position: 'relative', zIndex: 10, display: 'flex', flexDirection: 'column', justifyContent: 'flex-end', padding: '3rem', width: '100%', color: 'white' }}>
          <div style={{ marginBottom: '2rem' }}>
            <div style={{ width: '48px', height: '48px', backgroundColor: '#13ec37', borderRadius: '0.5rem', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '1.5rem', boxShadow: '0 10px 15px -3px rgba(19, 236, 55, 0.2)' }}>
              <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 96 960 960" width="24" fill="#102213">
                <path d="M160 856V356h160v500H160Zm240 0V356h160v500H400Zm240 0V356h160v500H640ZM160 276V176h640v100H160Z"/>
              </svg>
            </div>
            <h2 style={{ fontSize: '2.25rem', fontWeight: 700, marginBottom: '1rem', lineHeight: 1.2, letterSpacing: '-0.02em' }}>Advanced Poultry <br/>Finance Control</h2>
            <p style={{ color: 'rgba(255,255,255,0.8)', fontSize: '1.125rem', maxWidth: '28rem', fontWeight: 300, lineHeight: 1.6 }}>
              Streamline your farm operations, track production metrics, and manage finances in one unified dashboard.
            </p>
          </div>
          
        </div>
      </div>

      {/* Right Section: Login Form */}
      <div className="login-right animate-fade-in">
        <div style={{ width: '100%', maxWidth: '400px' }}>
          
          {/* Header */}
          <div style={{ marginBottom: '2rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
              <span style={{ color: '#13ec37', fontWeight: 700, fontSize: '1.25rem', letterSpacing: '0.05em' }}>PPFC</span>
            </div>
            <h1 style={{ fontSize: '1.875rem', fontWeight: 700, color: '#111827', margin: '0 0 0.5rem 0', letterSpacing: '-0.025em' }}>Welcome Back</h1>
            <p style={{ fontSize: '0.875rem', color: '#6b7280', margin: 0 }}>Please enter your details to access your dashboard.</p>
          </div>

          {/* Form */}
          <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
            
            {error && (
              <div style={{ padding: '0.75rem 1rem', backgroundColor: '#fef2f2', border: '1px solid #fee2e2', borderRadius: '0.5rem', display: 'flex', alignItems: 'flex-start', gap: '0.5rem' }}>
                <AlertCircle size={18} color="#ef4444" style={{ flexShrink: 0, marginTop: '2px' }} />
                <p style={{ fontSize: '0.875rem', color: '#b91c1c', margin: 0 }}>{error}</p>
              </div>
            )}

            <div>
              <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: 500, color: '#374151', marginBottom: '0.25rem' }}>Email Address</label>
              <div style={{ position: 'relative' }}>
                <div style={{ position: 'absolute', top: 0, bottom: 0, left: 0, paddingLeft: '0.75rem', display: 'flex', alignItems: 'center', pointerEvents: 'none' }}>
                  <Mail size={20} color="#9ca3af" />
                </div>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="login-input"
                  placeholder="manager@farm.com"
                  required
                />
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
                <label style={{ fontSize: '0.875rem', fontWeight: 500, color: '#374151' }}>Password</label>
              </div>
              <div style={{ position: 'relative' }}>
                <div style={{ position: 'absolute', top: 0, bottom: 0, left: 0, paddingLeft: '0.75rem', display: 'flex', alignItems: 'center', pointerEvents: 'none' }}>
                  <Lock size={20} color="#9ca3af" />
                </div>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="login-input"
                  placeholder="••••••••"
                  required
                />
              </div>
            </div>

            <button type="submit" disabled={loading} className="login-button" style={{ marginTop: '0.5rem' }}>
              {loading ? <Loader2 size={18} className="animate-spin" /> : 'Sign In'}
              {!loading && (
                <span style={{ position: 'absolute', right: '1rem', display: 'flex', alignItems: 'center' }}>
                  <svg xmlns="http://www.w3.org/2000/svg" height="18" viewBox="0 96 960 960" width="18" fill="rgba(16, 34, 19, 0.5)">
                    <path d="m321 856-43-43 250-250-250-250 43-43 293 293-293 293Z"/>
                  </svg>
                </span>
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
