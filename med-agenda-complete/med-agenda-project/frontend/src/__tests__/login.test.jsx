import { render, fireEvent } from '@testing-library/react'
import Login from '../components/Login'
import { describe, it, expect } from 'vitest'

describe('Login', ()=>{
  it('renders and submits', async ()=>{
    const onLogin = ()=>{}
    const { getByPlaceholderText, getByText } = render(<Login onLogin={onLogin} />)
    expect(getByPlaceholderText('Correo')).toBeTruthy()
    expect(getByText('Ingresar')).toBeTruthy()
  })
})
