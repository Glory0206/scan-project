import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';

import '../css/Home.css';

const Home = () => {
  return (
    <div className="container">
      <div className="left">
        <button className="home-left-button">
          <Link to="/trainmodel">
            <img 
              src="../public/CreateModel.png" 
              alt="Scan Image" 
              className="home-image"
            />  
          </Link>
        </button>
      </div>
      <div className="right">
        <button className="home-right-button">
          <Link to="/rotation">
            <img 
              src="../public/ScanImage.png" 
              alt="Scan Image" 
              className="home-image"
            />  
          </Link>
        </button>
      </div>
    </div>
  );
}
  
export default Home