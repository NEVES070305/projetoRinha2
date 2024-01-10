// PessoaForm.js
import React, { useState } from 'react';
import axios from 'axios';

const PessoaForm = () => {
  const [apelido, setApelido] = useState('');
  const [nome, setNome] = useState('');
  const [nascimento, setNascimento] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const response = await axios.post('http://localhost:8000/pessoas', {
        apelido,
        nome,
        nascimento
      });

      console.log('Pessoa criada:', response.data);
    } catch (error) {
      console.error('Erro ao criar pessoa:', error);
    }
  };

  return (
    <div>
      <h2>Criar Pessoa</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Apelido:
          <input type="text" value={apelido} onChange={(e) => setApelido(e.target.value)} />
        </label>
        <br />
        <label>
          Nome:
          <input type="text" value={nome} onChange={(e) => setNome(e.target.value)} />
        </label>
        <br />
        <label>
          Nascimento:
          <input type="text" value={nascimento} onChange={(e) => setNascimento(e.target.value)} />
        </label>
        <br />
        <button type="submit">Criar Pessoa</button>
      </form>
    </div>
  );
};

export default PessoaForm;
