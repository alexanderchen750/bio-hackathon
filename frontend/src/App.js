import logo from './logo.svg';
import './App.css';
import ImageUploadComponent from './imageUpload';

function App() {
  return (
    <div className = "container">
      <h1 className="title">Brain Tumor Detection</h1>
      <ImageUploadComponent/>
    </div>
    
  );
}

export default App;
