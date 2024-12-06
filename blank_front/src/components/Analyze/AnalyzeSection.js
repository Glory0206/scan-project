import React, { useState, useEffect } from 'react';
import './AnalyzeSection.css';

const AnalyzeSection = ({ fileData = [] }) => {
  const [selectedFileIndex, setSelectedFileIndex] = useState(0); // 선택된 파일의 인덱스
  const [selectedFile, setSelectedFile] = useState({areas: []});

  useEffect(() => {
    console.log('AnalyzeSection에서 받은 fileData:', fileData);
    if(fileData[selectedFileIndex]){
      setSelectedFile(fileData[selectedFileIndex])
    }
  }, [fileData, selectedFileIndex]);

  useEffect(() =>{
    console.log("areas: ", selectedFile.areas)
  })

  const handleClearData = () => {
    fileData = []
    setSelectedFileIndex(0); // 선택된 파일 인덱스 초기화
    setSelectedFile({ areas: [] }); // 선택된 파일 초기화
  };

  return (
    <div className="analyze-section">
      <div className="analyze-container">
        <div className="input-group">
          <div className="file-information">
            <h3>영역 상세 정보</h3>
          </div>
        </div>
        <div className="content-wrapper">
          {/* 이미지 목록: Sheet Names */}
          <div className="image-list">
            <h3>이미지 목록</h3>
            {fileData.map((file, index) => (
              <div
                key={index}
                className={`image-list-item ${
                  index === selectedFileIndex ? 'active' : ''
                }`}
                onClick={() => setSelectedFileIndex(index)} // 클릭 시 해당 파일 선택
              >
                <span className="image-number">{index + 1}</span>
                <span className="image-name">{file.sheetName || 'No Sheet Name'}</span>
              </div>
            ))}
          </div>

          {/* 영역 상세 정보 */}
          <div className="view-section">
            <div className="data-controls">
              <div className="left-controls">
                  <button 
                    className="delete-image-button"
                    onClick={handleClearData}
                  >
                    <span>데이터 초기화</span>
                  </button>
              </div>
            </div>
            <div className='data-preview'>
              {selectedFile.areas && selectedFile.areas.length > 0 ? (
                selectedFile.areas.map((area, index) => (
                  <div key={index} className="analysis-result">
                    <div className='number-blank'>
                      <p className='label'>
                        <span>문제 번호:</span> {area.areaName}
                      </p>
                      <p className='label'>
                        <span>공백 상태:</span> {area.isBlank === 'T' ? '공백' : '적혀있음'}
                      </p>
                    </div>
                    <div className="cropped-image">
                      <img
                        src={area.croppedImage}
                        alt={`Cropped ${index}`}
                        loading="lazy"
                      />
                    </div>
                  </div>
                ))
              ) : (<div></div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalyzeSection;
