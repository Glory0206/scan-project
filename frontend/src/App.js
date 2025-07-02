import Header from './components/Layout/Header';
import UploadSection from './components/Upload/UploadSection';
import './App.css';

function App() {
  return (
    <div className="app">
      <Header />
      <div className="content">
        <UploadSection />
      </div>
    </div>
  );
}

export default App;
