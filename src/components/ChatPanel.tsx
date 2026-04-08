import React, { useState, useRef, useEffect } from 'react';
import { supabase } from '../lib/supabase';
import { getGeminiResponse } from '../lib/gemini';
import { Send, Paperclip, X, User, Bot, Loader2, FileText, Image as ImageIcon, Plus, PanelLeftClose, PanelLeftOpen } from 'lucide-react';
import * as XLSX from 'xlsx';
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import 'katex/dist/katex.min.css';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  file_url?: string;
  created_at: string;
}

export const ChatPanel: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [sessions, setSessions] = useState<{id: string, created_at: string, first_msg?: string}[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [attachedFile, setAttachedFile] = useState<{ file: File, preview: string | null } | null>(null);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    initSession();
  }, []);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const initSession = async () => {
    const { data: allSessions } = await supabase
      .from('chat_sessions')
      .select(`
        id, 
        created_at,
        chat_messages (
          content,
          created_at
        )
      `)
      .order('created_at', { ascending: false });

    if (allSessions && allSessions.length > 0) {
      const formattedSessions = allSessions.map((s: any) => {
        // Find the earliest message to use as title snippet
        const msgs = s.chat_messages || [];
        msgs.sort((a: any, b: any) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime());
        return {
          id: s.id,
          created_at: s.created_at,
          first_msg: msgs[0]?.content || 'New Chat'
        };
      });
      setSessions(formattedSessions);
      loadSession(formattedSessions[0].id);
    } else {
      createNewSession();
    }
  };

  const loadSession = async (id: string) => {
    setSessionId(id);
    const { data: msgs } = await supabase
      .from('chat_messages')
      .select('*')
      .eq('session_id', id)
      .order('created_at', { ascending: true });
    
    if (msgs) {
      setMessages(msgs);
    } else {
      setMessages([]);
    }
  };

  const createNewSession = async () => {
    const { data: newSession } = await supabase
      .from('chat_sessions')
      .insert([{ user_id: (await supabase.auth.getUser()).data.user?.id }])
      .select()
      .single();
      
    if (newSession) {
      setSessions(prev => [newSession, ...prev]);
      setSessionId(newSession.id);
      setMessages([]);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = (rev) => setAttachedFile({ file, preview: rev.target?.result as string });
      reader.readAsDataURL(file);
    } else {
      setAttachedFile({ file, preview: null });
    }
  };

  const uploadToStorage = async (file: File) => {
    const fileName = `${Date.now()}-${file.name}`;
    const { data, error } = await supabase.storage
      .from('chat_files')
      .upload(fileName, file);
    
    if (error) throw error;
    
    const { data: { publicUrl } } = supabase.storage
      .from('chat_files')
      .getPublicUrl(data.path);
      
    return publicUrl;
  };

  const handleSend = async () => {
    if ((!input.trim() && !attachedFile) || loading || !sessionId) return;

    setLoading(true);
    let fileUrl = '';
    let mimeType = '';

    try {
      if (attachedFile) {
        fileUrl = await uploadToStorage(attachedFile.file);
        mimeType = attachedFile.file.type;
      }

      // 1. Save User Message
      const userMsg = {
        session_id: sessionId,
        role: 'user' as const,
        content: input,
        file_url: fileUrl || undefined
      };

      const { data: savedUserMsg } = await supabase
        .from('chat_messages')
        .insert([userMsg])
        .select()
        .single();

      if (savedUserMsg) setMessages(prev => [...prev, savedUserMsg]);
      setInput('');
      setAttachedFile(null);

      // 2. Prepare payload for Gemini
      let finalPrompt = input || "Analyze this file.";
      const filesForGemini: { url: string, mimeType: string }[] = [];

      if (attachedFile && fileUrl) {
        if (
          attachedFile.file.name.endsWith('.xlsx') || 
          attachedFile.file.name.endsWith('.xls') || 
          attachedFile.file.name.endsWith('.csv')
        ) {
          const buffer = await attachedFile.file.arrayBuffer();
          const workbook = XLSX.read(buffer, { type: 'array' });
          const firstSheetName = workbook.SheetNames[0];
          const worksheet = workbook.Sheets[firstSheetName];
          const csvText = XLSX.utils.sheet_to_csv(worksheet);
          
          // Truncate if insanely large to prevent overwhelming the request, but Gemini supports a lot.
          finalPrompt += `\n\n[Spreadsheet Data attached: ${attachedFile.file.name}]\n${csvText.substring(0, 100000)}`;
        } else {
          filesForGemini.push({ url: fileUrl, mimeType });
        }
      }

      const aiResponse = await getGeminiResponse(finalPrompt, filesForGemini);

      // 3. Save AI Message
      const aiMsg = {
        session_id: sessionId,
        role: 'assistant' as const,
        content: aiResponse
      };

      const { data: savedAiMsg } = await supabase
        .from('chat_messages')
        .insert([aiMsg])
        .select()
        .single();

      if (savedAiMsg) setMessages(prev => [...prev, savedAiMsg]);

    } catch (err) {
      console.error("Chat Error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="animate-fade-in" style={{ flex: 1, display: 'flex', gap: '1.5rem', minHeight: 0, position: 'relative' }}>
      {/* Sidebar */}
      <div style={{ width: isSidebarOpen ? '260px' : '0px', overflow: 'hidden', display: 'flex', flexDirection: 'column', gap: '1rem', borderRight: isSidebarOpen ? '1px solid var(--border)' : 'none', paddingRight: isSidebarOpen ? '1.5rem' : '0', flexShrink: 0, transition: 'all 0.3s ease', opacity: isSidebarOpen ? 1 : 0 }}>
        <button onClick={createNewSession} className="primary-button" style={{ width: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem', backgroundColor: 'var(--card)', color: 'white', border: '1px solid var(--border)' }}>
          <Plus size={16} /> New Chat
        </button>
        <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
          {sessions.map(s => {
            const d = new Date(s.created_at);
            const now = new Date();
            const diffHours = Math.max(0, Math.floor((now.getTime() - d.getTime()) / (1000 * 60 * 60)));
            const timeAgo = diffHours < 24 ? `${diffHours}h` : `${Math.floor(diffHours/24)}d`;
            
            return (
              <div key={s.id} onClick={() => loadSession(s.id)} style={{ padding: '0.75rem', borderRadius: '8px', cursor: 'pointer', backgroundColor: sessionId === s.id ? 'var(--muted)' : 'transparent', display: 'flex', alignItems: 'center', gap: '0.75rem', fontSize: '0.875rem', color: sessionId === s.id ? 'white' : 'var(--muted-foreground)', transition: 'background-color 0.2s' }}>
                <span style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: sessionId === s.id ? 'var(--primary)' : 'var(--muted-foreground)', opacity: sessionId === s.id ? 1 : 0.2 }} />
                <span style={{ whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', flex: 1, fontWeight: sessionId === s.id ? 500 : 400 }}>
                   {s.first_msg}
                </span>
                <span style={{ fontSize: '0.7rem', opacity: 0.5 }}>{timeAgo}</span>
              </div>
            );
          })}
        </div>
        
        <button 
          onClick={() => setIsSidebarOpen(false)}
          style={{ background: 'none', border: 'none', color: 'var(--muted-foreground)', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '0.5rem', padding: '0.5rem', borderRadius: 'var(--radius)', marginTop: 'auto', alignSelf: 'flex-start', transition: 'color 0.2s ease', fontSize: '0.875rem' }}
          title={"Collapse sidebar"}
        >
          <PanelLeftClose size={18} />
          <span>Collapse</span>
        </button>
      </div>

      {/* Main Chat Area */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '1rem', minWidth: 0 }}>

      <div ref={scrollRef} style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '1rem', padding: '1rem', backgroundColor: 'rgba(255,255,255,0.02)', borderRadius: '16px', border: '1px solid var(--border)' }}>
        {messages.length === 0 && !loading && (
          <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', opacity: 0.5, textAlign: 'center' }}>
            <Bot size={48} style={{ marginBottom: '1rem' }} />
            <p>How can I help you today?</p>
            <p style={{ fontSize: '0.875rem' }}>Upload an image or spreadsheet for analysis.</p>
          </div>
        )}
        {messages.map((m) => (
          <div key={m.id} style={{ display: 'flex', gap: '1rem', maxWidth: '80%', alignSelf: m.role === 'user' ? 'flex-end' : 'flex-start', flexDirection: m.role === 'user' ? 'row-reverse' : 'row' }}>
            <div style={{ width: '32px', height: '32px', borderRadius: '50%', backgroundColor: m.role === 'user' ? 'var(--primary)' : 'var(--muted)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
              {m.role === 'user' ? <User size={16} color="black" /> : <Bot size={16} color="var(--primary)" />}
            </div>
            <div style={{ padding: '0.75rem 1rem', borderRadius: '12px', backgroundColor: m.role === 'user' ? 'var(--muted)' : 'transparent', border: m.role === 'user' ? 'none' : '1px solid var(--border)', fontSize: '0.925rem', lineHeight: 1.5, minWidth: 0, overflow: 'hidden' }}>
              {m.file_url && (
                <div style={{ marginBottom: '0.5rem' }}>
                   {m.file_url.match(/\.(jpg|jpeg|png|gif|webp)$/) ? (
                     <img src={m.file_url} alt="Uploaded" style={{ maxWidth: '100%', borderRadius: '8px', maxHeight: '200px' }} />
                   ) : (
                     <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', padding: '0.5rem', backgroundColor: 'rgba(255,255,255,0.05)', borderRadius: '8px' }}>
                       <FileText size={16} />
                       <span style={{ fontSize: '0.75rem' }}>Attached File</span>
                     </div>
                   )}
                 </div>
              )}
              <div className="markdown-body">
                <ReactMarkdown remarkPlugins={[remarkMath]} rehypePlugins={[rehypeKatex]}>{m.content}</ReactMarkdown>
              </div>
            </div>
          </div>
        ))}
        {loading && (
          <div style={{ display: 'flex', gap: '1rem', alignSelf: 'flex-start' }}>
            <div style={{ width: '32px', height: '32px', borderRadius: '50%', backgroundColor: 'var(--muted)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Bot size={16} color="var(--primary)" />
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--muted-foreground)' }}>
              <Loader2 className="animate-spin" size={16} />
              <span style={{ fontSize: '0.875rem' }}>Analyzing...</span>
            </div>
          </div>
        )}
      </div>

      <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'flex-end', width: '100%' }}>
        {!isSidebarOpen && (
          <button 
            onClick={() => setIsSidebarOpen(true)}
            style={{ 
              background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.1)', color: 'var(--muted-foreground)', 
              cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0, 
              width: '42px', height: '42px', borderRadius: '50%', marginBottom: '8px',
              transition: 'background-color 0.2s, color 0.2s'
            }}
            title={"Expand sidebar"}
          >
            <PanelLeftOpen size={18} />
          </button>
        )}
        <div style={{ flex: 1, position: 'relative', display: 'flex', flexDirection: 'column', gap: '0.5rem', padding: '0.5rem', backgroundColor: 'rgba(255,255,255,0.03)', borderRadius: '24px', border: '1px solid rgba(255,255,255,0.1)' }}>
        {attachedFile && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', padding: '0.5rem', backgroundColor: 'var(--muted)', borderRadius: '8px', marginBottom: '0.5rem', alignSelf: 'flex-start' }}>
            {attachedFile.preview ? <ImageIcon size={16} /> : <FileText size={16} />}
            <span style={{ fontSize: '0.75rem', maxWidth: '150px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{attachedFile.file.name}</span>
            <button onClick={() => setAttachedFile(null)} style={{ border: 'none', background: 'none', color: 'var(--destructive)', cursor: 'pointer' }}><X size={14} /></button>
          </div>
        )}
        <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
          <button onClick={() => fileInputRef.current?.click()} style={{ padding: '0', borderRadius: '50%', backgroundColor: 'rgba(255,255,255,0.05)', border: 'none', color: 'var(--muted-foreground)', cursor: 'pointer', width: '38px', height: '38px', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0, transition: 'background-color 0.2s' }}>
            <Paperclip size={18} />
          </button>
          <input type="file" ref={fileInputRef} onChange={handleFileUpload} style={{ display: 'none' }} accept="image/*,.pdf,.csv,.xlsx,.xls" />
          <textarea 
            value={input}
            rows={1}
            onChange={(e) => {
              setInput(e.target.value);
              e.target.style.height = 'auto';
              e.target.style.height = `${Math.min(e.target.scrollHeight, 120)}px`;
            }}
            onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && (e.preventDefault(), handleSend())}
            placeholder="Ask anything about your farm data..."
            style={{ flex: 1, backgroundColor: 'transparent', border: 'none', outline: 'none', color: 'white', resize: 'none', padding: '10px 0.5rem', minHeight: '38px', maxHeight: '120px', fontSize: '0.9rem', lineHeight: '1.2' }}
          />
          <button 
            onClick={handleSend}
            disabled={loading || (!input.trim() && !attachedFile)}
            style={{ padding: '0', borderRadius: '50%', backgroundColor: 'var(--primary)', border: 'none', color: 'black', cursor: 'pointer', opacity: loading ? 0.5 : 1, width: '38px', height: '38px', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0, transition: 'transform 0.1s ease' }}
          >
            {loading ? <Loader2 className="animate-spin" size={18} /> : <Send size={18} />}
          </button>
        </div>
      </div>
      </div>
      </div>
    </div>
  );
};
