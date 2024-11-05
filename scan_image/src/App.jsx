import React from 'react';
import {Navbar, Container, Nav} from 'react-bootstrap'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';  // Bootstrap CSS를 import
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

import ScanImage from './components/Rotation';
import Home from './components/Home';
import TrainModel from './components/CreateModel';

const App = () => {
  return (
    <Router>
      <div>
        {/* 상단 네비게이션 바 */}
        <Navbar bg="dark" variant="dark" expand="lg" fixed="top">
          <Container fluid>
            <Navbar.Brand href="/">Scan Image</Navbar.Brand> {/* 좌측 브랜드명 */}
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
              <Nav className="me-auto">
                  <Nav.Link as={Link} to="/trainmodel">Create Model</Nav.Link>
                  <Nav.Link as={Link} to="/rotation">Rotation</Nav.Link>
              </Nav>
            </Navbar.Collapse>
          </Container>
        </Navbar>

        <div style={{ paddingTop: '60px' }}></div> {/* 네비게이션 바의 크기만큼 띄우기 */}

        {/* 라우팅 설정 */}
        <Routes>
          <Route path="/" element={<Home/>} />
          <Route path="/about" element={<div>About</div>} />
          <Route path="/rotation" element={<ScanImage />} />
          <Route path="/trainmodel" element={<TrainModel/>} />
          <Route path="*" element={<div>해당 페이지는 없는 페이지입니다.</div>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App