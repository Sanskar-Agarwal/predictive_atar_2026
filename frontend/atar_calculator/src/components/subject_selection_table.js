// Library Imports
import React  from 'react';
import { useState, useEffect, useRef } from 'react';

// Package Imports
import { DEFAULT_VALUES, MIN_ROW_GENERATED, TABLE_HEADERS } from '../constants/constants';
import TableRowFactory from './table_row_factory';

// Data Handlers
import RequestHandler from './data_handlers/request_handler';
import RowDataHandler from './data_handlers/row_data_handler';

// CSS Imports
import '../styles/components/subject_selection_table.css';

// Asset Imports 
import PlusIcon from '../assets/images/plus-solid.svg';

/**
 * Web page table element that allows the user to enter subjects and their relevant information.
 * @returns {JSX.Element} The rendered table component for subject selection.
 */
function SubjectSelectionTable({gradeType, region}) {
  const headers = TABLE_HEADERS;
  const [subjects, setSubjects] = useState([]);
  
  useEffect(
    () => {
      fetchRegionSubjects(region, setSubjects);
    }, [region]
  )
  
  return (
    <div className="subject-table">
        {
            (!gradeType || gradeType === 'Grade Type')? <div /> : <>
            <TableHeader headers={headers[gradeType] || []}/>
            <TableBody gradeType={gradeType} subjects={subjects} />
            </>
        }
    </div>
  );
}

/**
 * method to fetch a list of subjects based on selected region from the backend 
 * @param {string} selectedRegion region selected by the user
 * @param {function} setSubjects function used to set the current arrary of subjects to be displayed
 */
async function fetchRegionSubjects(selectedRegion, setSubjects) { 
  if (!selectedRegion || selectedRegion === DEFAULT_VALUES['region']) {
    return;
  }

  try {
      const ins = RequestHandler.getInstance();
      const fetchedSubjects = await ins.getSubjectsByRegionAbbr(selectedRegion);
      setSubjects(fetchedSubjects); // Assuming fetchedSubjects is an object
  } catch (error) {
      console.error("Error fetching subjects:", error);
  }
}

/**
 * the header component of the table 
 * @param {Object} props - The component props
 * @param {Array} headers - an array of headers
 * @returns {JSX.Element} The rendered table header component for subject selection.
 */
function TableHeader({headers}) {
    const headerLength = headers.length;
    return (
        <div className="table-header">
            { 
                headers.map(
                    (item, index) => {
                        const headerStyle = {
                            width: `${100 / headers.length}%`,
                            borderTopLeftRadius: index === 0 ? '10px' : '0px',
                            borderTopRightRadius: index !== (headers.length-1) ? '0px' : '10px',
                            borderRight: index === headerLength-1 ? '2px solid black' : "None",
                        };
                        return <div key={index} className="header-item" style={headerStyle}>{item}</div>   
                    }
                )
          }  
        </div>
    )
}

/**
 * the body component of the table 
 * @param {Object} props - the component props
 * @param {string} gradeType - the selected grade type for table row creation, default: ''
 * @param {Array} subjects - an array of subjects to be shown in a dropdown list, default: [] 
 * @returns {JSX.Element} The rendered table body component for subject selection.
 */
function TableBody({gradeType='', subjects=[]}) {
  const minRow = MIN_ROW_GENERATED;
  // Each row gets a stable unique id (not its array index) so deleting a row
  // doesn't shift the ids of the others — their entered data is keyed by id.
  const nextId = useRef(0);
  const generateRows = (count) => Array.from({ length: count }, () => nextId.current++);

  const [rows, setRows] = useState(() => generateRows(minRow));

  // Reset to the default rows whenever the grade type changes, and clear any
  // previously entered data so rows from another grade type aren't submitted.
  useEffect(() => {
    RowDataHandler.getInstance().clear();
    nextId.current = 0;
    setRows(generateRows(minRow));
  }, [gradeType, minRow]);

  const handleAddRow = () => {
    setRows((prev) => [...prev, nextId.current++]);
  };

  const handleDeleteRow = (id) => {
    RowDataHandler.getInstance().removeData(id);
    setRows((prev) => prev.filter((rowId) => rowId !== id));
  };

  return (
    <div className="table-body">
      { rows.map( (id) => {
          return <TableRow
                    key={id}
                    rowId={id}
                    gradeType={gradeType}
                    subjects={subjects}
                    onDelete={() => handleDeleteRow(id)}
                  />
          }
        )
      }
      <div
        className="add-more-subject-row"
      >
        <div
            className="add-button"
            onClick={handleAddRow}
        >
          <img src={PlusIcon} alt='plus icon'/>
        </div>
      </div>
    </div>
  );
}

/**
 * the row component of the table 
 * @param {Object} props - the component props
 * @param {number} rowId - the id of the row
 * @param {string} gradeType - the selected grade type for determined which row to produce
 * @param {Array} subjects - an array of subjects for dropdown list
 * @returns {JSX.Element} The rendered table row component for subject selection.
 */
function TableRow({rowId, gradeType, subjects, onDelete}) {
    const defaultSubjects = [
        "Math", "English", "Physics", 'Chemistry',
        'Biology',
    ];

    subjects = subjects && Object.keys(subjects).length > 0 ? subjects : defaultSubjects;
    const tableRowFactory = new TableRowFactory(rowId, subjects);
    // IB's first two rows are fixed to Theory of Knowledge / Extended Essay
    // (see ib_row.js, rowId < 2) and are required for the ToK/EE bonus points
    // calculation. Deleting one leaves no row for that subject at all, which
    // crashes the backend calculation instead of showing a useful error.
    const isFixedIBRow = gradeType === 'IB' && rowId < 2;
    // Wrap the factory-produced row so the delete control works for every grade
    // type without modifying each individual row component.
    return (
        <div className="table-row-wrapper">
            {tableRowFactory.makeTableRow(gradeType)}
            {!isFixedIBRow && (
                <button
                    type="button"
                    className="delete-row-button"
                    onClick={onDelete}
                    aria-label="Delete row"
                    title="Delete row"
                >
                    &times;
                </button>
            )}
        </div>
    );
}

export default SubjectSelectionTable;
