import logo from './logo.svg';
import './App.css';
import axios from 'axios';
import Button from '@mui/material/Button';
import { useState } from 'react';
import Username from './Username.js';
import Show from './Show.js';
import { Input } from '@mui/material';
import ArrowBackIosNewIcon from '@mui/icons-material/ArrowBackIosNew';


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
    if (members.length > 0) {
      axios.get("http://127.0.0.1:5000/", { params }, header).then(function (response) {
        console.log(response)
        if (response.data["Error"]) {
          console.log("trol")
          setMembers([])
          return
        }
        setData(response.data)
        console.log(response.data)
      })
    }

  }

  const usernameOnChange = (e) => {
    setUsername(e.target.value)
  }

  const clearData = (e) => {
    setData(null)
  }

  const addMember = (e) => {
    e.preventDefault()
    if (username !== "") {
      setMembers([...members, username])
    }

    setUsername("")
  }

  const removeMember = (m) => {
    setMembers(members.filter((n) => n !== m))
  }

  return (
    <div className="App">
      {(data) ?
        <div>
          <Button onClick={() => clearData()}>  <ArrowBackIosNewIcon sx={{ fontSize: 100 }} /> </Button>
          {data.map(x => Show(x['title'], x['rating'], "https://myanimelist.net/anime/" + x['id'], x['image_url']))}
        </div>
        :
        <div>

          <form onSubmit={(e) => addMember(e)}>
            <label>
              <br></br>

              <Input placeholder="Put your username here!" style={{ fontSize: 50, margin: "100px", padding: "100px" }} type="text" value={username} onChange={(e) => usernameOnChange(e)} />
              <Button onClick={(e) => addMember(e)} style={{ fontSize: 50, margin: "100px", padding: "100px" }}> + </Button>
            </label>
          </form>
          {members.map(m => Username(m, removeMember))}

          <Button style={{ fontSize: 50, margin: "100px", padding: "100px" }} onClick={() => get()}>Give me a recommendation!</Button>        </div>
      }

    </div >
  );
}

export default App;
