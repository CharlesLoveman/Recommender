import logo from './logo.svg';
import './App.css';
import axios from 'axios';
import Button from '@mui/material/Button';
import { useState } from 'react';

function App() {
  const [data, setData] = useState(null)

  function get() {
    console.log("hello")
    axios.get("http://127.0.0.1:5000/").then(function (response) {
      console.log(response.data)
      setData(response.data["text"]) 
    })
  }

  return (
    <div className="App">
      {(data) ? 
        <p>{data}</p>
        :
        <Button onClick={() => get()}>Get</Button>
      }
    </div>
  );
}

export default App;
