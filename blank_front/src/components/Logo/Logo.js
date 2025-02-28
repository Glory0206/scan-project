import './Logo.css';

const Logo = () => {
  const handleLogoClick = () => {
    window.location.reload();
  };

  return (
    <div className="logo-wrapper" onClick={handleLogoClick}>
      <h1 className="logo-text">Glory Scan</h1>
    </div>
  );
};

export default Logo;
