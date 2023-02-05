import logo from './logo.svg';
import './App.css';
import axios from 'axios';
import Button from '@mui/material/Button';
import { useState } from 'react';
import Username from './Username.js';

function App() {
  const [data, setData] = useState(null)
  const [members, setMembers] = useState([])
  const [username, setUsername] = useState("")

  function get() {
    axios.get("http://127.0.0.1:5000/").then(function (response) {
      setData(response.data["text"]) 
    })
  }

  const usernameOnChange = (e) => {
    setUsername(e.target.value)
  }

  const addMember = (e) => {
    e.preventDefault()
    setMembers([...members, username]) 
    setUsername("")
  }

  const removeMember = (m) => {
    setMembers(members.filter((n) => n !== m))
  }

  return (
    <div className="App">
      {(data) ? 
        <div>
          <p>{data}</p>
          <img src="https://myanimelist.net/images/anime/6/73245.jpg"/>
        </div>
        :
        <Button onClick={() => get()}>Get</Button>
      }
      <div>
        <form onSubmit={(e) => addMember(e)}>
          <label>
            Username:
            <input type="text" value={username} onChange={(e) => usernameOnChange(e)}/>
          </label>
        </form>
        {members.map(m => Username(m, removeMember))}
      </div>
    </div>
  );
}

export default App;
