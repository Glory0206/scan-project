import React, { useState } from 'react';
import axios from 'axios';  // axios가 필요한지 확인

const TrainModel = () => {
    const handleSetClick = async () => {
      try {
        const response = await axios.post('http://localhost:8000/set');
        alert("라벨링이 완료되었습니다.");
      } catch (error) {
        alert("라벨링에 문제가 발생했습니다.");
        console.error("Error during set operation:", error);
      }
    };
  
    const handleTrainClick = async () => {
      try {
        const response = await axios.post('http://localhost:8000/train');
        alert("학습이 정상적으로 완료되었습니다.");
      } catch (error) {
        alert("학습에 문제가 발생했습니다.");
        console.error("Error during training operation:", error);
      }
    };

    // TrainModel 컴포넌트가 렌더링되었는지 확인하는 로그 추가
    console.log('TrainModel component rendered');
  
    return (
      <div>
        <h1>Train Model Component</h1> {/* 이 텍스트가 화면에 출력되는지 확인 */}
        <button onClick={handleSetClick}>Set</button>
        <button onClick={handleTrainClick}>Train</button>
      </div>
    );
  }
  
  export default TrainModel;