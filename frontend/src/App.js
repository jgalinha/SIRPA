import { Route } from 'react-router-dom';
import './App.css';
import Login from './pages/Login';
import Student from './pages/Student';

function App() {
  return (
    <>
      <Route path="/" exact>
        <Login />
      </Route>
      <Route path="/student">
        <Student />
      </Route>
    </>
  );
}

export default App;
