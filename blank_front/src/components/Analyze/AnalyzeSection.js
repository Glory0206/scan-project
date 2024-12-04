import React, { useState, useEffect } from 'react';
import './AnalyzeSection.css';

const AnalyzeSection = ({ fileData = [] }) => {
  const [selectedFileIndex, setSelectedFileIndex] = useState(0); // 선택된 파일의 인덱스

  useEffect(() => {
    console.log('AnalyzeSection에서 받은 fileData:', fileData);
  }, [fileData]);

  // 선택된 파일 데이터 가져오기
  const selectedFile = fileData[selectedFileIndex] || {};

  if (!fileData || fileData.length === 0) {
    return <p>분석 결과가 없습니다.</p>;
  }

  return (
    <div className="analyze-section">
      <div className="analyze-container">
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
            <h3>영역 상세 정보</h3>
            {selectedFile.areas && selectedFile.areas.length > 0 ? (
              selectedFile.areas.map((area, index) => (
                <div key={index} className="analysis-result">
                  <p>
                    <strong>Area Name:</strong> {area.areaName || 'Unnamed'}
                  </p>
                  <p>
                    <strong>Is Blank:</strong> {area.isBlank === 'T' ? 'Yes' : 'No'}
                  </p>
                  <div className="cropped-image">
                    <img
                      src={area.croppedImage}
                      alt={`Cropped ${index}`}
                      loading="lazy"
                    />
                  </div>
                </div>
              ))
            ) : (
              <p>영역 데이터가 없습니다.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalyzeSection;
