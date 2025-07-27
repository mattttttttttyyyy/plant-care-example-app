import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import PlantList from './components/PlantList';
import PlantDetail from './components/PlantDetail';

function App() {
  return (
    <Router>
      <Switch>
        <Route path="/" exact component={PlantList} />
        <Route path="/plant/:id" component={PlantDetail} />
      </Switch>
    </Router>
  );
}

export default App;