// Library Imports
import { useState } from 'react';

// Package Imports

// CSS Imports
import "../../styles/components/drawer.css";

/**
 * the left drawer element for future use
 * @returns {JSX.Element} div elements to be dislayed on the webpage
 */
function Drawer() {
  const [isOpen, setIsOpen] = useState(false);

  const openDrawer = () => {
    setIsOpen(true);
  };

  const closeDrawer = () => {
    setIsOpen(false);
  };

  const spanStyle = {
      fontSize: '30px',
      cursor: 'pointer',
      margin: '10px'
  }


  return (
    <div>
      <div className={`drawer ${isOpen ? 'open' : ''}`}
        style={{width: `${isOpen ? '250px' : '0px'}`}}>
        <a href="#" className="closebtn" onClick={closeDrawer}>&times;</a>
        <a href="#">About</a>
        <a href="#">Services</a>
        <a href="#">Clients</a>
        <a href="#">Contact</a>
      </div>
      <span style={spanStyle} onClick={openDrawer}>&#9776;</span>
    </div>
  );
};

export default Drawer;

