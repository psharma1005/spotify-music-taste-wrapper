import logo from './logo.svg';
import './App.css';
import Button from "@mui/material/Button"
import SignIn from "./sign-in/SignIn"
import Test from './testUI/Test';
import LinkSpotify from './link-spotify/LinkSpotify';
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Profile from './profile/Profile';
import MainPage from './main-page/mainpage';
import MainPageTest from './main-page/mainpageTest';
import Register from './registration/registration';

function App() {
  return (
    <div>
      <BrowserRouter>
        <Routes>
          <Route index element={<SignIn />} />
          <Route path='/login' element={<SignIn />} />
          <Route path='/test' element={<Test />} />
          <Route path='/link' element={<LinkSpotify />} />
          <Route path='/profile' element={<Profile />} />
          <Route path='/main' element={<MainPageTest />} />
          <Route path='/register' element={<Register />} />

        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
