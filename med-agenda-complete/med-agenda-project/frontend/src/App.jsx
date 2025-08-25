import React, {useEffect, useState} from 'react'
import API, { setAuthToken } from './services/api'
import Login from './components/Login'
import AdminPanel from './components/AdminPanel'
import Calendar from '@fullcalendar/react'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'

export default function App(){
  const [events, setEvents] = useState([])
  const [logged, setLogged] = useState(Boolean(localStorage.getItem('token')))
  const [view, setView] = useState('calendar') // 'calendar' or 'admin'

  useEffect(()=>{ if(logged) loadEvents() },[logged])

  async function loadEvents(){
    try{
      const r = await API.get('/api/calendar/events')
      setEvents(r.data || r)
    }catch(e){ console.error(e) }
  }

  async function onEventDrop(info){
    const id = info.event.id;
    const start = info.event.start;
    const end = info.event.end || info.event.start;
    // format date/time
    const fecha = start.toISOString().slice(0,10);
    const hora_inicio = start.toTimeString().slice(0,5);
    const hora_fin = end.toTimeString().slice(0,5);
    try{
      await API.patch(`/api/appointments/${id}`, { fecha, hora_inicio, hora_fin });
    }catch(e){ alert('Error actualizando cita'); console.error(e) }
  }

  if(!logged) return <Login onLogin={()=>setLogged(true)} />

  return (
    <div className="min-h-screen bg-slate-50">
      <header className="bg-white shadow p-4">
        <div className="max-w-6xl mx-auto flex justify-between items-center">
          <h1 className="font-bold">MedAgenda</h1>
          <div className="space-x-2">
            <button onClick={()=>setView('calendar')} className="px-3 py-1 rounded bg-emerald-100">Calendario</button>
            <button onClick={()=>setView('admin')} className="px-3 py-1 rounded bg-emerald-100">Admin</button>
            <button onClick={()=>{ setAuthToken(null); setLogged(false); }} className="px-3 py-1 rounded bg-red-100">Salir</button>
          </div>
        </div>
      </header>
      <main className="max-w-6xl mx-auto p-6">
        {view==='calendar' && <div className="bg-white p-4 rounded shadow"><Calendar plugins={[ dayGridPlugin, timeGridPlugin ]} initialView="dayGridMonth" events={events} editable={true} eventDrop={onEventDrop} /></div>}
        {view==='admin' && <div className="bg-white p-4 rounded shadow"><AdminPanel /></div>}
      </main>
    </div>
  )
}
