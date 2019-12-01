import React, { Component } from 'react';
import { Link } from 'react-router-dom';


    function RunConfirmationComponent() {
        return (
            <div class="container">
                <div>
                    <h1> Data Collection Configuration Confirmation </h1>
                    <p> You have selected the following configuration for the data collection episode: </p>
                </div>
                <div class="text-center">
                    <p> Network Name: </p>
                </div>
                <div class="text-center">
                    <p> Database Details </p>
                </div>
                <Link to="/databaseContainer">
                    <button type="button" class="btn btn-primary btn-lg float-left">Back</button>
                </Link>
                <button type="button" class="btn btn-primary btn-lg float-right">Begin Collection</button>
            </div>
        );
    }


export default RunConfirmationComponent;