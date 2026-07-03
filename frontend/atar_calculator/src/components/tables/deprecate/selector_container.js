import { useState,  useEffect } from "react";
import "../styles/components/selector_container.css";
import RequestDataHandler from "../../request_data_handler";
import { GRADE_TYPES, REGIONS } from "../../../constants/constants";


function BottomContainer({description}) {
    return (
        <div className="selector-container-bottom">
            <div className="selector-left-container" >
                <h1 style={{ fontSize: `2vw`, color: "black", position: "relative", top: "-10px"}}>Description</h1>
            </div>
            <div className="selector-right-components">
                <span className="description-text">
                {description}
              </span>
            </div>
        </div>
    );
}

function SelectorContainer({ handleGradeTypeChange, setSelectedRegion, updateDescription }) {
    return (
      <div className="selector-container">
        <TopContainer 
          handleGradeTypeChange={handleGradeTypeChange} 
          setSelectedRegion={setSelectedRegion}
        />
        <BottomContainer description={updateDescription} />
      </div>
    ); 
}

function TopContainer({ handleGradeTypeChange, setSelectedRegion}) {

    return (
        <div className="selector-container-top">
            <div className="selector-left-components">
                <h2>Grading Type</h2>
            </div>
            <TopContainerRightComponents 
              handleGradeTypeChange={handleGradeTypeChange} 
              setSelectedRegion={setSelectedRegion}
            />
    </div>
    );
}


function TopContainerRightComponents({handleGradeTypeChange, setSelectedRegion}) {
    const region_options = [
      "Region", ...REGIONS
    ];
    
    const grading_type_options = [
        "Grade Type",  ...GRADE_TYPES
    ]
    const ins = RequestDataHandler.getInstance();

    const onRegionChange = (option) => {
        ins.setRegionAbbr(option);
        setSelectedRegion(option);
    }
    
    const onGradeTypeChange = (option) => {
      ins.setGradeType(option);
      handleGradeTypeChange(option);
    }
    
    return (
        <div className="selector-right-components">
            <DropdownList 
              options={region_options} 
              onValueChange={onRegionChange}
            />
            <DropdownList 
              options={grading_type_options} 
              onValueChange={onGradeTypeChange} 
            />
        </div>
    );
}

function DropdownList({
    options, 
    onValueChange,
    }) {
    let width = 15;
    // for (let i = 0; i < options.length; i++) {
    //   if (options[i].length > width) {
    //     width = options[i].length;
    //   }
    // }
    //
    const [isOpen, setIsOpen] = useState(false); 
    const [selectedOption, setSelectedOption] = useState(options[0]);

    const handleOptionSelect = (option) => {
        setSelectedOption(option);
        onValueChange(option);
        setIsOpen(false);
    }

    const toggleSelect = () => { 
        setIsOpen(!isOpen);
    }
    
    const closeAllSelect = (event) => {
        if (!event.target.matches('.value-selected')) {
            setIsOpen(false);
        }
    }

    useEffect(
        () => {
           document.addEventListener('click', closeAllSelect); 
           return () => {
            document.removeEventListener('click', closeAllSelect);
           }
        }, []
    )

    const isOpenStyled =  {
        borderBottomLeftRadius: "0px",
        borderBottomRightRadius: '0px'
    }
    
    return (
        <div 
             className="selector-container-custom-select" 
             style={{ width: `${width-3}rem`, ...(isOpen ? isOpenStyled : {}) }} 
             onClick={toggleSelect}
            >
          <div className={`value-selected ${isOpen ? 'select-arrow-active' : ''}`} onClick={toggleSelect}>
            {selectedOption}
          </div>
          {isOpen && (
            <div className="value-items">
              {options.map(
                (option, index) => {
                  if ( index !== 0) { 
                    return (
                      <div
                        key={index}
                        className={option === selectedOption ? 'same-as-selected' : ''}
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
                      className={option === selectedOption ? 'same-as-selected' : ''}
                      onClick={() => handleOptionSelect(option)}
                      hidden>
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

export default SelectorContainer;
