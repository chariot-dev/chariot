import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Button from 'react-bootstrap/Button';

class DatabaseManager extends Component {
  render() {
    return (
      <div className="container">
        <h1>Database Manager</h1>
          <p className="screenInfo">Add, delete, or manage a database.</p>
          
          <div>
            <Link to="/">Add a Database</Link>
            <br></br>
            <br></br>
            <Link to="/deleteDatabaseConfiguration">Delete a Database</Link>
            <br></br>
            <br></br>
            <Link to="/manageExistingDatabaseConfiguration">Manage Existing Database</Link>
          </div>

          <Link to="/welcome">
            <Button variant="primary" className="float-left footer-button">Back</Button>
          </Link>
      </div>
    );
  }
}
 
export default DatabaseManager; 