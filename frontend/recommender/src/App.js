import logo from './logo.svg';
import './App.css';
import axios from 'axios';
import Button from '@mui/material/Button';
import { useState } from 'react';
import Username from './Username.js';
import Show from './Show.js';


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
      console.log(response.data)
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
          {data.map(x => Show(x['title'], x['rating'], x["https://myanimelist.net/anime/" + x['id'] + "/" + x['title']], x['image_url']))}
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
