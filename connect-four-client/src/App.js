import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import { connect } from './Request';
import Navbar from './Navbar';
import Home from './Home';
import NotFound from './NotFound';
import Signup from './Signup';
import NewMatch from './NewMatch';
import HomepageRedirect from './HomepageRedirect';
import JoinMatch from './JoinMatch';

function App() {
  const [ws, setWS] = useState(null);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    setWS(connect('ws://localhost:8080/'));
  }, []);

  if (ws) {
    if (!ws.onopen) {
      ws.onopen = () => {
        setReady(true);
      }
    }
  }

  if (ready) {
    return (
      <Router>
        <div className="app">
          <Navbar />
          <div className="content">
            <Switch>
              <Route exact path="/">
                <Home websocket={ws} />
              </Route>
              <Route path="/redirect/:username/:token">
                <HomepageRedirect websocket={ws} />
              </Route>
              <Route path="/signup">
                <Signup websocket={ws} />
              </Route>
              <Route path="/newmatch/:username/:token">
                <NewMatch websocket={ws} />
              </Route>
              <Route path="/joinmatch/:username/:token">
                <JoinMatch websocket={ws} />
              </Route>
              <Route path="*">
                <NotFound />
              </Route>
            </Switch>
          </div>
        </div>
      </Router>
    );
  }
}

export default App;
