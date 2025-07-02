import './Logo.css';

const Logo = () => {
  const handleLogoClick = () => {
    window.location.reload(); // 웹페이지 새로고침
  };

  return (
    <div className="logo-wrapper" onClick={handleLogoClick}>
      <h1 className="logo-text">Glory Scan</h1>
    </div>
  );
};

export default Logo;
