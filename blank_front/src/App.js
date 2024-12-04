import Header from './components/Layout/Header';
import UploadSection from './components/Upload/UploadSection';
import AnalyzeSection from './components/Analyze/AnalyzeSection';
import './App.css';

function App() {
  return (
    <div className="app">
      <Header />
      <div className="content">
        <UploadSection />
        <AnalyzeSection/>
      </div>
    </div>
  );
}

export default App;
