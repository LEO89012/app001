import React, {useState} from 'react'
import API, { setAuthToken } from '../services/api'

export default function Login({onLogin}){
  const [email, setEmail] = useState('admin@medagenda.com');
  const [passw, setPassw] = useState('adminpass');
  async function submit(e){
    e.preventDefault();
    try{
      const fd = new URLSearchParams();
      fd.append('username', email);
      fd.append('password', passw);
      const r = await API.post('/api/auth/token', fd.toString(), { headers: {'Content-Type':'application/x-www-form-urlencoded'} });
      if (r.data && r.data.access_token){
        setAuthToken(r.data.access_token);
        onLogin();
      } else {
        alert('Credenciales inválidas');
      }
    }catch(e){ console.error(e); alert('Error de login') }
  }
  return (
    <div className="max-w-md mx-auto mt-20 bg-white p-6 rounded shadow">
      <h2 className="text-xl font-bold mb-4">Iniciar sesión</h2>
      <form onSubmit={submit} className="space-y-3">
        <input className="w-full border p-2 rounded" value={email} onChange={e=>setEmail(e.target.value)} placeholder="Correo" />
        <input type="password" className="w-full border p-2 rounded" value={passw} onChange={e=>setPassw(e.target.value)} placeholder="Contraseña" />
        <button className="w-full bg-emerald-600 text-white p-2 rounded">Ingresar</button>
      </form>
    </div>
  )
}
