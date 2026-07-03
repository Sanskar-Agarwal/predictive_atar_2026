// Package Imports
import Navbar from "./navbars/navbar.js";

// CSS Imports
import '../styles/template.css';

/**
 * template page that can be reused by future pages
 * @returns {JSX.Element} div elements to be dislayed on the webpage
 */
function Template() {   
    return (
        <Navbar />
    );
}

export default Template;
