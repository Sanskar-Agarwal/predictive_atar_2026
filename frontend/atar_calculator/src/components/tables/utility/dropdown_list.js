// Library Imports
import { useState, useEffect } from 'react';

// CSS Imports
import '../../../styles/dropdown_list/dropdown_list.css';

/**
 * 
 * @param {Object} props - component props 
 * @param {String} optionSelected - the first option to be displayed by default, by default 'Select' if not provided
 * @param {Array} options - an array of options that can be selected
 * @param {function} handleValueChange - function for setting the selected option to be used in other part of the program
 * @param {Object} style - a style object that can be used to style different parts of the componenets
 * @returns {JSX.Element} The rendered dropdown list.
 */
export function DropDownList({ optionSelected="Select", options, handleValueChange=()=>{}, style = {} }) {
    const [showOptions, setShowOptions] = useState(false);

    const toggleShowOption = () => {
        setShowOptions(!showOptions);
    };

    const handleOptionSelected = (e) => {
        const option = e.target.textContent;
        handleValueChange(option);
        toggleShowOption();
    };

    return (
        <div className="dropdown-list-container" onClick={toggleShowOption} style={style['dropdown-list-container']}>
            <DropdownListDisplay optionSelected={optionSelected} showOptions={showOptions} setShowOptions={setShowOptions} style={style} />
            <DropdownOptions showOptions={showOptions} options={options} 
                handleOptionSelected={handleOptionSelected} style={style} />
        </div>
    );
}

/**
 * a rendered component that is the primary display when the screen is rendered, with/without the dropdown list expanded.
 * this would always be displayed on the screen, and illustrated only the option that has been selected prior. 
 * @param {Object} props - component props 
 * @param {string} optionSelected - the option that has been selected by the user to be displayed 
 * @param {boolean} showOptions - boolean toggle to determine the direction of the arrow
 * @param {function} setShowOptions - update function for determine if the system should expand the dropdown or not
 * @param {Object} style - style objects for additional customisation
 * @returns {JSX.Element} The rendered primary displayed for the selected option of dropdown list
 */
function DropdownListDisplay({optionSelected, showOptions, setShowOptions, style}) {
    const [id, ]  = useState( `${optionSelected}-dropdown-list`);

    const selectedOptionStyle = {
        borderRadius: !showOptions ? '8px' : '8px 8px 0px 0px',
        backgroundColor: !showOptions ? 'white' : 'var(--default-bg-color)',
        color: !showOptions ? 'black' : 'white',
        ...style['selected-option']
    };

    useEffect(() => {
        const closeAllSelect = (e) => { 
            if (e.target.id !== id) {
                setShowOptions(false); 
            }
        }
        document.addEventListener('click', closeAllSelect);
        return () => {
          document.removeEventListener('click', closeAllSelect);
        };
      }, [id, setShowOptions]);

    return (   
        <div id={id} className="selected-option" style={selectedOptionStyle}>
            <div id={id} className='selected-option-text'>
                {optionSelected}
            </div>
            <div id={id} className={showOptions ? 'option-arrow-up' : 'option-arrow-down'}
                style={showOptions ? style['option-arrow-up'] : style['option-arrow-down']}>
            </div>
    </div>
    );
}

/**
 * a rendered component that shows the expanded dropdown options
 * @param {Object} props - component props
 * @param {boolean} showOptions - boolean toggle to expand/contract the dropdown options
 * @param {function} handleOptionSelected - function used to retrieve the value of the selected option
 * @param {Object} style - style object for additional customisation
 * @returns 
 */
function DropdownOptions({showOptions, options, handleOptionSelected, style})  {
    return (
        <>
            {!showOptions ? <div /> :
                (
                <div className="dropdown-option" style={style['dropdown-option']}>
                    {options.map(
                        (option, index) => (
                            <div
                                key={index}
                                value={option}
                                onClick={handleOptionSelected}
                                hidden={option==='Other' ? true : false}
                                style={{
                                }}
                            >
                                {option}
                            </div>
                        )
                    )}
                </div>
            )}
        </>
    );
}
