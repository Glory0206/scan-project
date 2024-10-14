'use client';

import { useState, useCallback } from 'react';

import '../css/Rotation.css';

const Rotation = () => {
  // 이미지 데이터 저장 상태
  const [images, setImages] = useState([]);

  //이미지 로딩 여부
  const [isLoading, setIsLoading] = useState(false);

  // 파일 개수 저장 상태
  const [fileCount, setFileCount] = useState(0);  

  //폴더 업로드 함수
  const handleFolderUpload = useCallback(async (event) => { //비동기로 효율 올리기
    const files = event.target.files; //사용자가 선택한 파일 리스트

    //파일이 없을 경우 종료
    if (!files) return;

    //로딩 중
    setIsLoading(true);
    const imageFiles = Array.from(files).filter(file => file.type.startsWith('image/')); //각 파일의 MIME 타입 확인 ex) image/gif, image/png

    // 파일 개수 상태 업데이트
    setFileCount(imageFiles.length);

    try {
      // 서버로 이미지 파일 전송 (FormData 사용)
      const formData = new FormData(); // 브라우저에서 파일이나 기타 데이터를 HTTP 요청으로 보낼 때 사용되는 객체
      imageFiles.forEach((file) => formData.append('images', file)); // 폴더 내의각 파일을 images라는 키에 추가하여 서버에 보낼 준비를 한다

      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData, // 파일 데이터를 그대로 전송
      });

      if (!response.ok) {
        throw new Error('Failed to upload images');
      }

      console.log('Images uploaded successfully');
    } catch (error) {
        console.error('Error uploading images:', error);
    } finally {
        setIsLoading(false); // 로딩 종료
    }
  }, []);

  const handleClearImages = async () => {
    try {
      const response = await fetch('/api/delete-images', { // 서버의 파일 삭제 API 경로
        method: 'DELETE',
      });
  
      if (!response.ok) {
        throw new Error('Failed to delete images from server');
      }
  
      // 클라이언트 측에서도 상태 초기화
      setImages([]);
      setFileCount(0); // 파일 개수 초기화
      console.log('Images deleted successfully from server');
    } catch (error) {
      console.error('Error deleting images from server:', error);
    }
  };
  

  return (
    <div>
      <div className='container'>
        <div className='box'>
          <h2 className="title">Scan Image</h2>
          <div>
            <div>
              <label htmlFor="folder-upload">폴더 선택</label>
              <input
                id="folder-upload"
                type="file"
                webkitdirectory="true"
                onChange={handleFolderUpload}
                disabled={isLoading}
              />
            </div>
              {isLoading && <p>이미지 로딩 중...</p>}{/* 업로드 중 */}
            <div>
              {images.map((src, index) => (
                <img key={index} src={src} alt={`Image ${index + 1}`}/>
              ))}
            </div>
            <div>
              {fileCount > 0 && (
                <button onClick={handleClearImages}>초기화</button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Rotation;