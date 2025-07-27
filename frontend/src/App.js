import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import PlantList from './components/PlantList';
import PlantDetail from './components/PlantDetail';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<PlantList />} />
        <Route path="/plant/:id" element={<PlantDetail />} />
      </Routes>
    </Router>
  );
}

export default App;