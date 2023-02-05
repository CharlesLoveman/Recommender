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
    const params = {
      'members': members
    }
    const header = {
      'Content-Type': "application/json"
    }
    axios.get("http://127.0.0.1:5000/", { params }, header).then(function (response) {
      setData(response.data)
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
          <h1>Our recommendation is:</h1>
          <p>{data['title']}!</p>
          <p>It is rated {data['rating']}, if you're curious</p>
          <a href={"https://myanimelist.net/anime/" + data['id'] + "/" + data['title']}><img src={data['image_url']} /></a>
        </div>
        :
        <div>
          <Button onClick={() => get()}>Get</Button>
          <form onSubmit={(e) => addMember(e)}>
            <label>
              Username:
              <input type="text" value={username} onChange={(e) => usernameOnChange(e)} />
            </label>
          </form>
          {members.map(m => Username(m, removeMember))}
        </div>
      }

    </div >
  );
}

export default App;
