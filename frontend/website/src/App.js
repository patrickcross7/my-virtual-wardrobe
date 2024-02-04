import './App.css';
import NavBar from './Components/NavBar/NavBar';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';  
import Collection from './Pages/Collection';
import DrawingPage from './Pages/DrawingPage';
function App() {
  return (
    <div className='main'>
      
      <Router>
        <NavBar></NavBar>
    
        <Routes>
          <Route path='/Collections' element={<Collection/>}></Route>
          <Route path='/' element={<DrawingPage></DrawingPage>}></Route>

        </Routes>
      </Router> 

    </div>



  );
}

export default App;
