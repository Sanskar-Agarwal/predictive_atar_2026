// Library Imports
import { useState, useRef } from 'react';

/**
 * table column that encompasses all information related to subject
 * @param {Object} props - component props
 * @param {Array} subjects - an array of subjects that can be selected
 * @param {function} setEnteredSubject - an update function used to change the value of entered subject
 * @param {Object} style - style objects for    additional customisation
 * @returns {JSX.Element} The rendered table row to be displayed
 */
export function SubjectColumn({subjects, setEnteredSubject, style={}}) {
    const [inputValue, setInputValue] = useState('');
    const [isOpen, setIsOpen] = useState(false);
    const [highlight, setHighlight] = useState(0);
    const [showHoverEffect, setShowHoverEffect] = useState(false);
    // ref mirrors the current text so the (delayed) blur handler reads the
    // latest value instead of a stale closure when an option is clicked
    const valueRef = useRef('');
    const blurTimeout = useRef(null);

    const setValue = (value) => {
        valueRef.current = value;
        setInputValue(value);
    };

    // case-insensitive substring filter; empty input shows the whole list
    const query = inputValue.trim().toLowerCase();
    const filtered = subjects.filter((subject) => subject.toLowerCase().includes(query));
    const isValid = inputValue.trim() === '' || subjects.includes(inputValue.trim());

    const commitSubject = (subject) => {
        setValue(subject);
        setEnteredSubject(subject);
        setIsOpen(false);
    };

    const handleSubjectEntered = (event) => {
        const value = event.target.value;
        setValue(value);
        setIsOpen(true);
        setHighlight(0);
        // only ever propagate an exact, valid subject; clear otherwise so the
        // backend can never receive an unrecognised name (silent under-count)
        setEnteredSubject(subjects.includes(value.trim()) ? value.trim() : '');
    };

    const handleBlur = () => {
        // delay so an option's onMouseDown commits before the list closes
        blurTimeout.current = setTimeout(() => {
            setIsOpen(false);
            // discard partial/invalid text so only a valid subject survives
            if (!subjects.includes(valueRef.current.trim())) {
                setValue('');
                setEnteredSubject('');
            }
        }, 150);
    };

    const handleFocus = () => {
        clearTimeout(blurTimeout.current);
        setIsOpen(true);
    };

    const handleKeyDown = (event) => {
        if (!isOpen || filtered.length === 0) return;
        if (event.key === 'ArrowDown') {
            event.preventDefault();
            setHighlight((current) => Math.min(current + 1, filtered.length - 1));
        } else if (event.key === 'ArrowUp') {
            event.preventDefault();
            setHighlight((current) => Math.max(current - 1, 0));
        } else if (event.key === 'Enter') {
            event.preventDefault();
            if (filtered[highlight]) commitSubject(filtered[highlight]);
        } else if (event.key === 'Escape') {
            setIsOpen(false);
        }
    };

    const handleOnDoubleClicked = () => {
        setShowHoverEffect(true);
        setTimeout(() => {
            setShowHoverEffect(false);
        }, 1500);
    };

    return (
        <div className="subject-column" style={style}>
            { showHoverEffect && inputValue && <div className='hover-text'>{inputValue}</div> }
                <input
                    className="subject-datalist"
                    placeholder="Subject"
                    value={inputValue}
                    onChange={handleSubjectEntered}
                    onFocus={handleFocus}
                    onBlur={handleBlur}
                    onKeyDown={handleKeyDown}
                    onDoubleClick={handleOnDoubleClicked}
                    autoComplete="off"
                    style={{
                        color: isValid ? 'black' : 'red'
                    }}
                />
                { isOpen && filtered.length > 0 && (
                    <ul className="subject-options">
                        {filtered.map((subject, index) => (
                            <li
                                key={subject}
                                className={`subject-option${index === highlight ? ' highlighted' : ''}`}
                                // onMouseDown fires before the input's onBlur, so the
                                // selection commits before the list would close
                                onMouseDown={() => commitSubject(subject)}
                            >
                                {subject}
                            </li>
                        ))}
                    </ul>
                )}
        </div>
    );
}

/**
 * table column that encompasses all information related to subject, but the subject name cannot be changed by the user
 * @param {Object} props - component props
 * @param {string} subject - the fixed subject name to be displayed
 * @param {Object} style - style objects for additional customisation
 * @returns {JSX.Element} The rendered table row to be displayed
 */
export function FixedSubjectColumn({ subject, style={}}) {
    return ( 
        <div className="subject-column" style={style}>
            {subject}
        </div>
    );
}

/**
 * table column that shows all related information regarding subject assessments
 * @param {Object} props - component props
 * @param {function} setEnteredAssessment - function to retrieved the assessment entered by user to be used in other part of the program
 * @param {Object} style - style objects for additional customisation
 * @returns {JSX.Element} The rendered table row to be displayed
 */
export function AssessmentColumn({setEnteredAssessment, style={}}) {
    const handleSubjectLevelEntered = (event) => {
        const subject = event.target.value;
        setEnteredAssessment(subject);
    };

    return (
        <div className="subject-level-column" style={style}>
            <input
                className="subject-datalist"
                placeholder="Level"
                list="levelOptions"
                onChange={handleSubjectLevelEntered}
            />
        </div>
    );
}

/**
 * table column that allows the user to enter mark in numerical value
 * @param {Object} props - component props
 * @param {number} enteredMark - the mark value entered by the user, default: 0
 * @param {function} setEnteredMark - function to retrieved the mark entered by user to be used in other part of the program
 * @param {Object} inputFormat - the formatted object that customise the input field
 * @param {Object} style - style objects for additional customisation
 * @returns {JSX.Element} The rendered table row to be displayed
 */
export function NumericalMarkColumn({ enteredMark, setEnteredMark, inputFormat = {} , style = {} }) {
    const {
      minRange = 0,
      maxRange = 100,
      step = 10
    } = inputFormat;
    
    const handleOnBlur = () => {
      const inputMark = parseFloat(enteredMark); // Parse as a floating-point number
      if (inputMark > parseFloat(maxRange)) {
        setEnteredMark(parseFloat(maxRange)); // Set to the value inside the range column
      } else {
        setEnteredMark(inputMark || 0);
      }       
    }
  
    const handleOnChange = (e) => {
        const inputMark = (e.target.value).trim();
        setEnteredMark(inputMark); 
    };
  
    return (
      <div className="mark-column" style={style}>
        <input
          type="number"
          className="numerical-input"
          min={minRange}
          step={step}
          max={maxRange.toString()}
          value={enteredMark.toString()}
          onChange={handleOnChange}
          onBlur={handleOnBlur}
        />
      </div>
    );
}

/**
 * table column that allows user to enter choose a mark from a list of options
 * @param {Object} props - component props
 * @param {Array} options - an array of options that can be selected
 * @param {Object} style - style objects for additional customisation
 * @returns {JSX.Element} The rendered table row to be displayed
 */
export function CategoricalMarkColumn({options, setSelectedMark, style={}}) {
    const handleOnSelect = (e) => {
        const mark = e.target.value;
        setSelectedMark(mark); 
    }
    return (
        <div className='mark-column' style={style}>
            <select className='mark-select' onChange={handleOnSelect}>
                {options.map((item, index) => (
                    <option key={index} value={item}>{item}</option>
                ))}
            </select>
        </div> 
    );
}

/**
 * table column that allows the user to entered both numerical & categorical mark
 * @param {Object} props - component props
 * @param {Array} options - an array of options that can be selected
 * @param {function} setEnteredMark - function to retrieved the mark entered by user to be used in other part of the program
 * @param {Object} inputFormat - format options used to customised the datalist
 * @param {Object} style - style objects for additional customisation
 * @returns {JSX.Element} The rendered table row to be displayed
 */
export function MixedMarkColumn({options, setEnteredMark, inputFormat={}, style={}}) {
    const { 
        minRange=0, 
        maxRange=100
    } = inputFormat;
    const [placeholder, setPlaceholder] = useState('');

    const handleMarkEntered = (event) => {
        const mark = ((event.target.value).trim()).toUpperCase(); 
        setPlaceholder(mark); 
        setEnteredMark(mark);
    }
    
    const handleOnBlur = () => { 
        const mark = (placeholder).trim(); 
        const markNumber = parseFloat(mark);
        
        if (!markNumber) { 
            return;
        }

        let displayValue = markNumber;
        if (markNumber < minRange) {
            displayValue = minRange;
        } else if (markNumber > maxRange) {
            displayValue = maxRange;
        }
        setPlaceholder(displayValue);
        setEnteredMark(displayValue);
    }
    
    return (
        <div className="mark-column" style={style}>
                <input
                    className="mark-datalist"
                    value={placeholder}
                    placeholder='Mark'
                    onChange={handleMarkEntered}
                    onBlur={handleOnBlur}
                    list="markOptions"
                />
                <datalist id="markOptions">
                    {options.map((option, index) => (
                        <option key={index} className="custom-option" value={option} />
                    ))}
                </datalist>
        </div>
    );  
}

/**
 * table column that allows the user to enter the maximum mark a certain subject has
 * @param {Object} props - component props
 * @param {number} enteredMark - mark entered by user, used to determine if the entered mark is greater than the maximum mark
 * @param {function} setEnteredMark - function to update the entered mark to match the current max mark
 * @param {number} enteredMaxMark - the maximum mark value entered by the user
 * @param {function} setEnteredMaxMark - function to retrieved and update the maximum mark entered by user to be used in other part of the program
 * @param {Object} style - style objects for additional customisation
 * @returns {JSX.Element} The rendered table row to be displayed
 */
export function MaxMarkColumn({ 
    enteredMark, 
    setEnteredMark,
    enteredMaxMark, 
    setEnteredMaxMark, 
    style = {} }) {

    const handleOnChange = (e) => {
        let inputRange = e.target.value.trim(); // Parse as a floating-point number
        setEnteredMaxMark(inputRange);
    };

    const handleOnBlur = (e) => { 
      const inputRange = parseFloat((e.target.value).trim()); // Parse as a floating-point number
      setEnteredMark(Math.min(enteredMark, inputRange));
      setEnteredMaxMark(inputRange || 100);
    }
  
    return (
      <div className="max-mark-column" style={style}>
        <input
            type='text'
            className='numerical-input'
            value={enteredMaxMark.toString()}
            onChange={handleOnChange}
            onBlur={handleOnBlur}
        />
      </div>
    );
}
  
/**
 * table column that allows the user to entered the weighting that a certain subject has
 * @param {Object} props - component props
 * @param {number} enteredWeighting - the number of weighting that a subject has 
 * @param {function} setEnteredWeighting - function to retrieved the weighting entered by user to be used in other part of the program
 * @param {Object} style - style objects for additional customisation
 * @returns {JSX.Element} The rendered table row to be displayed
 */
export function WeightingColumn({ enteredWeighting, setEnteredWeighting, style = {} }) {
    const handleOnChange = (e) => {
      const inputWeighting = parseFloat((e.target.value).trim()); // Parse as a floating-point number
      setEnteredWeighting(inputWeighting);
    };
  
    return (
      <div className="weighting-column" style={style}>
        <input
          type="number"
          className="numerical-input"
          min="0"
          max="100"
          step="10"
          value={enteredWeighting.toString()}
          onChange={handleOnChange} // Parse input value to a floating-point number
        />
      </div>
    );
}
  
/**
 * table column that allows the user to entered both numerical & categorical mark
 * @param {Object} props - component props
 * @param {number} enteredYear - the year value entered by user;
 * @param {function} setEnteredYear - function to retrieved the year entered by user to be used in other part of the program
 * @param {number} currentYear - the current year we are living in right now, this would use to set the minimum number of year the user can entered, default: currentYear - 20
 * @param {Object} style - style objects for additional customisation
 * @returns {JSX.Element} The rendered table row to be displayed
 */
export function YearColumn({enteredYear, setEnteredYear, currentYear, style={}}) {
    const handleOnChange = (e) => {
        const value = parseInt(e.target.value, 10);
        if (value > currentYear) {
            setEnteredYear(currentYear);
        } else {
            setEnteredYear(value);
        }
    }

    return (
        <div className="year-column" style={style}> 
            <input 
                type="number"
                className="numerical-input"
                min={currentYear - 20}
                max={currentYear}
                step='1'
                value={enteredYear.toString()}
                onChange={handleOnChange}
            />
        </div>
    );
}