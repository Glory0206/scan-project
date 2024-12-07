import React, { useState, useEffect } from 'react';
import './AnalyzeSection.css';

const AnalyzeSection = ({ fileData = [], onClearFileData }) => {
  const [selectedFileIndex, setSelectedFileIndex] = useState(0);
  const [selectedFile, setSelectedFile] = useState({ areas: [] });

  useEffect(() => {
    if (fileData[selectedFileIndex]) {
      setSelectedFile(fileData[selectedFileIndex]);
    } else {
      setSelectedFile({ areas: [] });
    }
  }, [fileData, selectedFileIndex]);

  const handleClearAllData = () => {
    setSelectedFileIndex(0);
    setSelectedFile({ areas: [] });
    if (onClearFileData) onClearFileData();
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
          {/* 데이터 목록 */}
          <div className="image-list">
            <h3>데이터 목록</h3>
            {fileData.map((file, index) => (
              <div
                key={index}
                className={`image-list-item ${index === selectedFileIndex ? 'active' : ''}`}
                onClick={() => setSelectedFileIndex(index)}
              >
                <span className="image-number">{index + 1}</span>
                <span className="image-name">{file.sheetName || 'No Sheet Name'}</span>
              </div>
            ))}
          </div>

          {/* 영역 상세 정보 */}
          <div className="view-section">
            <div className="data-controls">
              <button className="delete-image-button" onClick={handleClearAllData}>
                데이터 초기화
              </button>
            </div>
            <div className="data-preview">
              {selectedFile.areas.length > 0 ? (
                selectedFile.areas.map((area, index) => (
                  <div key={index} className="analysis-result">
                    <div className="number-blank">
                      <p className="label">
                        <span>문제 번호:</span> {area.areaName}
                      </p>
                      <p className="label">
                        <span>공백 상태:</span> {area.isBlank === 'T' ? '공백' : '적혀있음'}
                      </p>
                    </div>
                    {area.croppedImage && (
                      <div className="cropped-image">
                        <img
                          src={area.croppedImage}
                          alt={`Cropped ${index}`}
                          loading="lazy"
                        />
                      </div>
                    )}
                  </div>
                ))
              ) : (
                <p>선택된 데이터가 없습니다.</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalyzeSection;
