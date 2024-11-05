 import logo from './logo.svg';
import './App.css';
import Button from "@mui/material/Button"
import SignIn from "./sign-in/SignIn"
import Test from './testUI/Test';
import LinkSpotify from './link-spotify/linkSpotify';
import { BrowserRouter, Routes, Route } from 'react-router-dom'

function App() {
  return (
    <div>
      <BrowserRouter>
        <Routes>
          <Route index element={<SignIn />} />
          <Route path='/login' element={<SignIn />} />
          <Route path='/test' element={<Test />} />
          <Route path='/link' element={<LinkSpotify />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
