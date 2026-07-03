// Library Imports
import { useState } from "react";

// Package Imports 
import Template from "../components/template.js"; 
import RequestHandler from "../components/data_handlers/request_handler.js";
import { PROJECT_TITLE } from "../constants/constants.js";

// CSS Imports
import "../styles/login.css";

// Asset Imports
import USYDLogo from '../assets/images/usyd_logo.png';
import EmailIcon from "../assets/images/email_icon.png"; 
import LockIcon from "../assets/images/lock_icon.png"; 
import ShowPasswordIcon from '../assets/images/show_password_icon.svg';
import UnShowPasswordIcon from '../assets/images/unshow_password_icon.svg';

/**
 * the login page that allows the user to login, reset their password
 * @returns {JSX.Element} rendered login page 
 */
function Login() {
    return (
        <>
            <Template />
            <div className='login-container'>
                <LeftComponent />
                <RightComponent />
            </div>
        </>
    );
}

/**
 * the left components of the login page that contains the page logo and title
 * @returns {JSX_Element} rendered left component of the login page
 */
function LeftComponent() {
    return (
        <div className='login-left-component'>
            <div className='logo-icon'> 
                <img src={USYDLogo} alt="usyd logo"/>
            </div>
            <div className='title-text'>{PROJECT_TITLE}</div>
        </div>
    );
}

/**
 * the right components of the login page that contains all the textfield and the login button
 * @returns {JSX_Element} rendered component of the login page
 */
function RightComponent() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    return (
        <div className='login-right-component'>
            <h1>Login</h1>
            <EmailContainer setEmail={setEmail}/>
            <PasswordContainer setPassword={setPassword}/>
            <LoginUtilityContainer />
            <LoginButton email={email} password={password}/>
        </div>
    );
}

/**
 * container that encapsulates all information related to email textfield
 * @param {Object} props - component props
 * @param {function} setEmail - updater for changing the value of email 
 * @returns {JSX_Element} rendered textfield
 */
function EmailContainer({setEmail}) {
    const handleOnChange = (e) => { 
        const value = e.target.value; 
        setEmail(value);
    }

    return (
        <div className='input-container'>
            <div className='icon-container'>
                <img src={EmailIcon} alt="email" />
            </div>
            <div className='textfield-container'>
                <input 
                    className='custom-input'
                    placeholder='Email'
                    onChange={handleOnChange}
                />
            </div>
        </div>
    );
}

/**
 * container that encapsulates all information related to password textfield
 * @param {Object} props - component props
 * @param {function} setPassword - updater for changing the value of password
 * @returns {JSX_Element} rendered textfield
 */
function PasswordContainer({setPassword}) {
    const [showPassword, setShowPassword] = useState(false);
    
    const toggleShowPassword = () => { 
        setShowPassword(!showPassword);
    }
    
    const handleOnChange = (e) => { 
        const value = e.target.value;
        setPassword(value);
    }
    
    const styles = {
        'lock': {
            opacity: 0.5,
        },
        'toggle_password': {
            border: 'None',
            scale: 0.8,
            margin: '0px 10px'
        }
    }
    return ( 
        <div className='input-container'>
            <div className='icon-container'>
                <img src={LockIcon} alt="password" id='password-icon'/>
            </div>
            <div className='textfield-container'>
                <input 
                    type={showPassword ? 'text' : 'password'}
                    className='custom-input'
                    placeholder='Password'
                    onChange={handleOnChange}
                />
                <div className='icon-container' onClick={toggleShowPassword} style={styles['toggle_password']}>
                    {
                        showPassword ?
                        <img src={ShowPasswordIcon} alt='show-password'/>: 
                        <img src={UnShowPasswordIcon} alt='show-password'/>
                    }
                </div> 
            </div>
        </div>
    );
}

/**
 * containers that holds the toggle for remember me and forget password
 * @returns {JSX_Element} rendered utility components of the textfield 
 */
function LoginUtilityContainer() {
    const [rememberMe, setRememberMe] = useState(false);

    const onToggle = () => {
        setRememberMe(!rememberMe);
    }
    return (
        <div className='login-utility-container'> 
            <div className='remember-me-container'> 
                <label className='toggle-switch'>
                    <input type='checkbox' checked={rememberMe} onChange={onToggle} />
                    <span className='slider round' />
                </label>
                Remember me?
            </div>
            <a href='https://www.youtube.com/watch?v=dQw4w9WgXcQ'>
                Forget Password
            </a>
        </div>
    );
}

/**
 * button that submitted user information upon pressed 
 * @param {Object} props - component props 
 * @param {string} email - the email entered by user
 * @param {string} password - the password entered by user
 * @returns {JSX_Element} rendered submit button
 */
function LoginButton({email, password}) {
    const handleOnClick = () => {
         LoginUser(email, password);
    }

    return (
        <button className='login-submit-button' onClick={handleOnClick}>Login</button>
    );
}

/**
 * asynchronous function that log the user into the system based on the provided credential
 * @param {string} email 
 * @param {string} password 
 */
async function LoginUser(email, password) {
    try { 
        const ins = RequestHandler.getInstance(); 
        const fetchedData = await ins.loginUser(email, password);
        console.log(fetchedData);
    } catch (error) { 
        console.error("Error logging in user:", error);
    }
}

export default Login;
