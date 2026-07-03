// Library Imports
import React, { useState, useEffect } from 'react';

// Package Imports
import Login  from "../../pages/login.js";
import RootManager from '../data_handlers/root_manager.js';
import GradeTypeObserver from '../observers/grade_type_observer.js';
import { DEFAULT_VALUES, PROJECT_TITLE } from '../../constants/constants.js';
import { PAGE_COMPONENTS, getPersistedPage, setPersistedPage } from './page_registry.js';

// CSS Imports
import "../../styles/components/navbar.css";

/**
 * the navbar of the webpage for navigating between different pages 
 * @returns {JSX.Element} div elements to be dislayed on the webpage
 */
function Navbar(){
  return (
    <div className="navbar-container">
      <LeftContainer />
      <RightContainer />
    </div>
  );
}

/**
 * the left components of the navbar that contains the name of the application
 * @returns {JSX.Element} div elements to be dislayed on the webpage
 */
function LeftContainer() {
  return (
    <div className="left-container">
      <h2>{PROJECT_TITLE}</h2>
    </div>
  );
}

/**
 * the right components of the navbar that contains the login button and the dropdown button
 * @returns {JSX.Element} div elements to be dislayed on the webpage
 */
function RightContainer() {
  return (
    <div className="right-container">
      <LoginButton />
      <DropdownButton />
    </div>
  );
}

/**
 * the login button that render the login page
 * @returns {JSX.Element} div elements to be dislayed on the webpage
 */
function LoginButton() {
  const handleClick = () => {
    RenderPage(<Login />);
  }

  return (
    <button className="login-button" onClick={handleClick}>
      Login
    </button>
  );
}

/**
 * the dropdown button that allows the user to naviage to the different calculator pages
 * @returns {JSX.Element} div elements to be dislayed on the webpage
 */
function DropdownButton() {
  const options = [
    'Calculator',
    'Manual', 'Automatic', 'Mirror Mode'
  ];

  const [isOpen, setIsOpen] = useState(false);
  // reflect whatever page is actually on screen (persisted across refresh),
  // rather than always defaulting the label back to the 'Calculator' placeholder
  const [selectedOption, setSelectedOption] = useState(getPersistedPage());

  const handleOptionSelect = (option) => {
    setSelectedOption(option);
    setIsOpen(false);
    setPersistedPage(option);
    const Page = PAGE_COMPONENTS[option];
    RenderPage(<Page />);
  };

  const toggleSelect = () => {  
    setIsOpen(!isOpen);
  };

  const closeAllSelect = (event) => {
    if (!event.target.matches('.navbar-dropdown-list')) {
      setIsOpen(false);
    }
  };

  useEffect(() => {
    document.addEventListener('click', closeAllSelect);
    return () => {
      document.removeEventListener('click', closeAllSelect);
    };
  }, []);

  return (
    <div className="navbar-dropdown-list-container" style={{ width: '200px' }} onClick={toggleSelect}>
      <div className={`navbar-dropdown-list ${isOpen ? 'arrow-active-icon' : ''}`} onClick={toggleSelect}>
        {selectedOption}
      </div>
      {isOpen && (
        <div className="navbar-dropdown-items">
          {options.map(
            (option, index) => {
              if ( index !== 0) { 
                return (
                  <div
                    key={index}
                    className={option === selectedOption ? 'navbar-selected-item' : ''}
                    onClick={() => handleOptionSelect(option)}
                  >
                    <h3>
                      {option}
                    </h3>
                  </div>
                );
              } else { 
                return (
                  <div
                  key={index}
                  className={option === selectedOption ? 'navbar-selected-item' : ''}
                  onClick={() => handleOptionSelect(option)}
                  hidden
                >
                  {option}
                </div>  
                );
              }
            }
          )}
        </div>
      )}
    </div>
    );
}

/**
 * utility function used for rendering different pages
 * @param {JSX.Element} page to be rendered
 */
function RenderPage(page) {
  const instance = RootManager.getInstance();
  instance.createRoot();
  const observer = GradeTypeObserver.getInstance();
  observer.updateValue(DEFAULT_VALUES['grade_type']);

  const root = instance.getRoot();
  root.render(page);
}

export default Navbar;


