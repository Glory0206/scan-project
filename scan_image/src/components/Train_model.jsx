import React, { useState } from 'react';
import axios from 'axios';  // axios가 필요한지 확인
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';

function TrainModel() {
    // 버튼 클릭 시 호출될 함수 정의
    const [showScanImage, setShowScanImage] = useState(false);

    const handleSetClick = async () => {
      try {
        const response = await axios.post('http://localhost:8000/set');
        console.log(response.data);
      } catch (error) {
        console.error("Error during set operation:", error);
      }
    };
  
    const handleModelClick = async () => {
      try {
        const response = await axios.post('http://localhost:8000/model');
        console.log(response.data);
      } catch (error) {
        console.error("Error during model operation:", error);
      }
    };
  
    const handleTrainClick = async () => {
      try {
        const response = await axios.post('http://localhost:8000/train');
        console.log(response.data);
      } catch (error) {
        console.error("Error during training operation:", error);
      }
    };

    // TrainModel 컴포넌트가 렌더링되었는지 확인하는 로그 추가
    console.log('TrainModel component rendered');
  
    return (
      <div>
        <h1>Train Model Component</h1> {/* 이 텍스트가 화면에 출력되는지 확인 */}
        <button onClick={handleSetClick}>Set</button>
        <button onClick={handleModelClick}>Model</button>
        <button onClick={handleTrainClick}>Train</button>
      </div>
    );
  }
  
  export default TrainModel;