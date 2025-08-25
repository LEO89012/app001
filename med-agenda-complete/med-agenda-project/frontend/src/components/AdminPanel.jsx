import React, {useEffect, useState} from 'react'
import API from '../services/api'

export default function AdminPanel(){
  const [empresas, setEmpresas] = useState([]);
  const [name, setName] = useState('');
  useEffect(()=>{ load() },[])
  async function load(){ const r = await API.get('/api/admin/empresas'); setEmpresas(r.data || r); }
  async function create(){ if(!name) return; await API.post('/api/admin/empresas', { nombre:name }); setName(''); load(); }
  async function remove(id){ if(!confirm('Eliminar empresa?')) return; await API.delete(`/api/admin/empresas/${id}`); load(); }
  return (
    <div>
      <h2 className="text-lg font-bold mb-2">Administración de Empresas</h2>
      <div className="mb-4 flex gap-2">
        <input value={name} onChange={e=>setName(e.target.value)} className="border p-2 rounded" placeholder="Nombre empresa" />
        <button onClick={create} className="bg-emerald-600 text-white px-3 rounded">Crear</button>
      </div>
      <ul className="space-y-2">
        {empresas.map(e=> (
          <li key={e.id} className="bg-white p-2 rounded shadow flex justify-between">
            <div>{e.nombre} <span className="text-sm text-gray-500">#{e.id}</span></div>
            <div><button onClick={()=>remove(e.id)} className="text-red-600">Eliminar</button></div>
          </li>
        ))}
      </ul>
    </div>
  )
}
