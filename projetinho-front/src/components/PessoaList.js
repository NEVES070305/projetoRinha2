// PessoaList.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const PessoaList = () => {
  const [pessoas, setPessoas] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:8000/pessoas')
      .then(response => setPessoas(response.data))
      .catch(error => console.error('Error fetching pessoas:', error));
  }, []);

  return (
    <div>
      <h2>Pessoas</h2>
      <ul>
        {pessoas.map(pessoa => (
          <li key={pessoa.id}>{pessoa.nome} - {pessoa.apelido}</li>
        ))}
      </ul>
    </div>
  );
};

export default PessoaList;
