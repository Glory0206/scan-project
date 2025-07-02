import { useState, useEffect } from 'react';
import './DatasetModal.css';
import axios from 'axios';

const DatasetModal = ({ isOpen, onClose }) => {
  const [imageCount, setImageCount] = useState(1);
  const [fileName, setFileName] = useState('이미지를 선택해주세요');
  const [isClosing, setIsClosing] = useState(false);
  const [clickStartTarget, setClickStartTarget] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [showMessage, setShowMessage] = useState(false);
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState('');

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFileName(file.name);
      setSelectedFile(file);
    }
  };

  const hideMessageWithDelay = (callback) => {
    setTimeout(() => {
      setShowMessage(false);
      if (callback) callback();
    }, 2000);
  };

  const displayMessage = (text, type = 'error', callback) => {
    setShowMessage(true);
    setMessage(text);
    setMessageType(type);
    hideMessageWithDelay(callback === onClose ? handleClose : callback);
  };

  const handleSubmit = async () => {
    if (!selectedFile) {
      displayMessage('이미지를 선택해주세요.', 'error');
      return;
    }

    setIsLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('count', imageCount);

      const response = await axios.post('http://localhost:8000/generate', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        responseType: 'blob',
      });
      
      // 파일명을 Content-Disposition에서 추출
      const contentDisposition = response.headers['content-disposition'];
      let fileName = 'dataset.zip'; // 기본 파일명

      if (contentDisposition) {
        // 정규표현식으로 filename 값만 추출해서 실제 저장될 파일 이름으로 설정
        const match = contentDisposition.match(/filename="?([^"]+)"?/);
        if (match && match[1]) {
          fileName = decodeURIComponent(match[1]);
        }
      }

      // blob 데이터를 다운로드 링크로 만들어 다운로드
      // blob: 브라우저 메모리 상에서 바이너리 데이터를 파일처럼 다룰 수 있는 객체
      const blob = new Blob([response.data], { type: 'application/zip' });

      // createObjectURL()은 메모리에 있는 Blob을 URL로 변환해서 <a> 태그에 넣을 수 있게 함
      const url = window.URL.createObjectURL(blob);

      const a = document.createElement('a'); // <a> 태그 생성
      a.href = url; // <a> 태그를 만들고 href를 blob URL로 지정
      a.download = fileName; // download 속성에 추출했던 파일명을 지정
      a.click(); // 사용자가 누르지 않아도 자동으로 다운로드

      // 메모리 정리
      window.URL.revokeObjectURL(url);

      displayMessage('데이터셋 생성 성공', 'success', onClose);
    } catch (error) {
      console.error(error);
      displayMessage('데이터셋 생성에 실패했습니다.', 'error');
    } finally {
      setIsLoading(false);
    }
  };

  const handleOverlayMouseDown = (e) => {
    setClickStartTarget(e.target.className);
  };

  const handleOverlayMouseUp = (e) => {
    if (clickStartTarget === 'modal-overlay') {
      setIsClosing(true);
      setTimeout(() => {
        setIsClosing(false);
        handleClose();
      }, 400);
    }
    setClickStartTarget(null);
  };

  const handleClose = () => {
    setImageCount(1);
    setFileName('이미지를 선택해주세요');
    setSelectedFile(null);
    onClose();
  };

  useEffect(() => {
    const handleEscKey = (e) => {
      if (e.key === 'Escape' && isOpen) {
        setIsClosing(true);
        setTimeout(() => {
          setIsClosing(false);
          handleClose();
        }, 400);
      }
    };

    // ESC 키 이벤트 리스너 등록
    window.addEventListener('keydown', handleEscKey);

    // 컴포넌트 언마운트 시 이벤트 리스너 제거
    return () => {
      window.removeEventListener('keydown', handleEscKey);
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div 
      className="modal-overlay" 
      onMouseDown={handleOverlayMouseDown}
      onMouseUp={handleOverlayMouseUp}
    >
      <div className={`modal-content ${isClosing ? 'slide-out' : ''}`}>
        <div className="modal-header">
          <h2>데이터셋 생성</h2>
          <button className="close-button" onClick={handleClose}>×</button>
        </div>
        
        <div className="modal-body">
          <div className="input-section">
            <label className="input-label">원본 이미지</label>
            <div className="file-input-wrapper">
              <input
                type="file"
                id="dataset-image"
                className="file-input"
                accept="image/*"
                onChange={handleImageChange}
              />
              <label htmlFor="dataset-image" className="file-label">
                <span className="upload-icon">📁</span>
                <span className="file-name">{fileName}</span>
              </label>
            </div>
          </div>

          <div className="input-section">
            <label className="input-label">생성할 이미지 수</label>
            <div className="number-input-wrapper">
              <input
                type="number"
                min="1"
                max="100"
                value={imageCount}
                onChange={(e) => setImageCount(e.target.value)}
                className="number-input"
              />
              <span className="number-suffix">장</span>
            </div>
          </div>
        </div>
        <p className="info-text">
          ＊ 무작위 방향으로 회전, 텍스트가 입력된 샘플 데이터셋이 생성됩니다.
        </p>
        <div 
          className={`message ${messageType} ${showMessage ? 'show' : ''}`}
        >
          {message}
        </div>
        <div className="modal-footer">
          <button 
            className="cancel-button" 
            onClick={handleClose}
            disabled={isLoading}
          >
            취소
          </button>
          <button 
            className="create-button" 
            onClick={handleSubmit}
            disabled={isLoading}
          >
            {isLoading ? '생성 중...' : '생성'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default DatasetModal; 
