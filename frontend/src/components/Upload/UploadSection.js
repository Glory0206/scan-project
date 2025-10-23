import { useState, useEffect, useCallback } from "react";
import "./UploadSection.css";
import axios from "axios";
import AnalyzeSection from "../Analyze/AnalyzeSection";
import { API_URL } from "../config/config";

const UploadSection = () => {
  const [selectedImages, setSelectedImages] = useState([]);
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [fileName, setFileName] = useState("이미지를 선택해주세요");
  const [showError, setShowError] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const [scale, setScale] = useState(1);
  const [imageState, setImageState] = useState({
    position: { x: 0, y: 0 },
    dragStart: { x: 0, y: 0 },
  });
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isCoordMode, setIsCoordMode] = useState(false);
  const [fileData, setFileData] = useState([]);

  // 초기화 함수
  const resetImageState = () => {
    setScale(1);
    setImageState({
      position: { x: 0, y: 0 },
      dragStart: { x: 0, y: 0 },
    });
  };

  const handleImageChange = (e) => {
    const files = Array.from(e.target.files);
    if (files.length > 0) {
      setFileName(`${files.length}개의 이미지 선택됨`);
      const imageUrls = files.map((file) => ({
        url: URL.createObjectURL(file),
        name: file.name,
        state: {
          position: { x: 0, y: 0 },
          dragStart: { x: 0, y: 0 },
          scale: 1,
        },
      }));
      setSelectedImages(imageUrls);
      setCurrentImageIndex(0);
      setShowError(false);
      resetImageState();
    }
  };

  const handleAnalyze = async () => {
    if (!selectedImages.length) {
      alert("이미지를 업로드 해주세요.");
      return;
    }

    try {
      setIsAnalyzing(true);
      const formData = new FormData();

      for (const image of selectedImages) {
        const response = await fetch(image.url);
        const blob = await response.blob();
        formData.append("images", blob, image.name);
      }

      const { data } = await axios.post(`${API_URL}/analyze`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
        onUploadProgress: ({ loaded, total }) => {
          setUploadProgress(Math.round((loaded * 100) / total));
        },
        timeout: 100000,
      });

      if (data.results?.length) {
        setFileData((prev) => [...prev, ...data.results]);
      } else {
        console.error("results 배열이 없습니다:", data);
      }
    } catch (error) {
      if (error.response && error.response.data && error.response.data.detail) {
        alert(error.response.data.detail);
      } else {
        alert("이미지 분석 실패: 알 수 없는 오류가 발생했습니다.");
      }
      console.error("이미지 분석 실패:", error);
    } finally {
      setIsAnalyzing(false);
      setUploadProgress(0);
    }
  };

  const handleWheel = useCallback(
    (e) => {
      e.preventDefault();
      if (isCoordMode) return;
      const direction = e.deltaY > 0 ? -1 : 1;
      const newScale =
        Math.min(Math.max(scale * 100 + direction * 10, 50), 400) / 100;
      setScale(newScale);
    },
    [scale, isCoordMode]
  );

  const handleDeleteImage = () => {
    setSelectedImages([]);
    setFileName("이미지를 선택해주세요");
    resetImageState();
    document.getElementById("image-upload").value = "";
  };

  const handleImageSelect = (index) => {
    setCurrentImageIndex(index);
    resetImageState();
  };

  const handleCoordToggle = () => setIsCoordMode((prev) => !prev);

  const handleMouseDown = (e) => {
    if (isCoordMode) return;
    setIsDragging(true);
    setImageState((prev) => ({
      ...prev,
      dragStart: {
        x: e.clientX - prev.position.x,
        y: e.clientY - prev.position.y,
      },
    }));
  };

  const handleMouseMove = (e) => {
    if (isDragging) {
      setImageState((prev) => ({
        ...prev,
        position: {
          x: e.clientX - prev.dragStart.x,
          y: e.clientY - prev.dragStart.y,
        },
      }));
    }
  };

  const handleMouseUp = () => setIsDragging(false);

  // 마우스 이벤트 핸들러 등록 및 해제
  useEffect(() => {
    if (isDragging) {
      window.addEventListener("mousemove", handleMouseMove);
      window.addEventListener("mouseup", handleMouseUp);
    } else {
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", handleMouseUp);
    }
    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", handleMouseUp);
    };
  }, [isDragging]);

  // 스케일 변경 이벤트 등록 및 해제
  useEffect(() => {
    const imagePreview = document.querySelector(".image-preview");
    if (imagePreview) {
      imagePreview.addEventListener("wheel", handleWheel, { passive: false });
      return () => imagePreview.removeEventListener("wheel", handleWheel);
    }
  }, [handleWheel]);

  // Object URL 정리
  useEffect(() => {
    return () => {
      selectedImages.forEach((image) => URL.revokeObjectURL(image.url));
    };
  }, [selectedImages]);

  return (
    <div className="upload-section">
      <div className="upload-container">
        <div className="input-group">
          <div className="file-input-container">
            <input
              type="file"
              id="image-upload"
              className="file-input"
              accept="image/*"
              multiple
              onChange={handleImageChange}
            />
            <label htmlFor="image-upload" className="file-label">
              <span className="upload-icon">📁</span>
              <span className="file-name">{fileName}</span>
            </label>
          </div>
          <button
            className={`analyze-button ${isAnalyzing ? "analyzing" : ""}`}
            onClick={handleAnalyze}
            disabled={isAnalyzing}
          >
            {isAnalyzing ? `분석 중 ${uploadProgress}%` : "분석"}
          </button>
        </div>

        <div className={`error-message ${showError ? "show" : ""}`}>
          이미지를 업로드 해주세요.
        </div>

        <div className="content-wrapper">
          <div className="image-list">
            <h3>이미지 목록</h3>
            {selectedImages.map((image, index) => (
              <div
                key={image.name}
                className={`image-list-item ${
                  index === currentImageIndex ? "active" : ""
                }`}
                onClick={() => handleImageSelect(index)}
              >
                <span className="image-number">{index + 1}</span>
                <span className="image-name">{image.name}</span>
              </div>
            ))}
          </div>

          <div className="preview-section">
            <div className="image-controls">
              <div className="left-controls">
                <button
                  className="delete-image-button"
                  onClick={handleDeleteImage}
                >
                  사진삭제
                </button>
              </div>
              <div className="scale-indicator">{Math.round(scale * 100)}%</div>
            </div>
            <div className="image-preview">
              {selectedImages.length > 0 && (
                <div
                  className="image-container"
                  style={{
                    cursor: isCoordMode
                      ? "crosshair"
                      : isDragging
                      ? "grabbing"
                      : "grab",
                  }}
                  onMouseDown={handleMouseDown}
                >
                  <img
                    src={selectedImages[currentImageIndex].url}
                    alt={`Preview ${currentImageIndex + 1}`}
                    style={{
                      transform: `scale(${scale}) translate(${imageState.position.x}px, ${imageState.position.y}px)`,
                      transition: isDragging
                        ? "none"
                        : "transform 0.1s ease-out",
                    }}
                    draggable={false}
                  />
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
      <AnalyzeSection
        fileData={fileData}
        onClearFileData={() => setFileData([])}
      />
    </div>
  );
};

export default UploadSection;
