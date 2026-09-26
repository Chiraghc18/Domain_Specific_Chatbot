// src/App.js
import { Provider } from 'react-redux';
import store from './store/store';
import Chat from './components/chat';
import './App.css';

function App() {
  return (
    <Provider store={store}>
      <div className="App">
        
        <Chat />
      </div>
    </Provider>
  );
}

export default App;