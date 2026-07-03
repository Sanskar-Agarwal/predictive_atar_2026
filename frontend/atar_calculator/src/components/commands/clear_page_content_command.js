// Package Imports
import { DEFAULT_VALUES } from "../../constants/constants";

// Observers
import GradeTypeObserver from "../observers/grade_type_observer";
import RegionObserver from "../observers/region_observer";
import ApplicationIDObserver from "../observers/application_id_observer";
import ApplicantNameObserver from "../observers/applicant_name_observer";
import NoteObserver from '../observers/note_observer';

// Data Handlers
import RowDataHandler from "../data_handlers/row_data_handler";
import RequestDataHandler from "../data_handlers/request_data_handler";

class ClearPageContentCommand {
  /** Command class that focuses on clearing all page content to allow the user to start fresh
   * @param {function} setGradeType - updater function used to reset the grade type dropdown list
   * @param {function} setSelectedRegion - updater function used to reset the region dropdown list
   * @param {function} setApplicationID - updater function used to reset the application id textfield
   * @param {function} setApplicantName - updater function used to reset the applicant name textfield
   * @param {function} setNote - updater function used to reset the note textfield
   * @param {function} rowDataHandler - updater function used to reset the data inside row data handler
   * @param {function} outputDataHandler - updater function used to reset the data inside output handler
   */
  constructor() {
    this.observers = {
      'grade_type': GradeTypeObserver.getInstance(),
      'region': RegionObserver.getInstance(),
      'application_id': ApplicationIDObserver.getInstance(),
      'applicant_name': ApplicantNameObserver.getInstance(),
      'note': NoteObserver.getInstance(),
    }
  }

  /**
   * run all relevant operations to clear the page content
   */
  execute() {
    this.clearObservers();
    this.clearDataHandler();
  }

  /**
   * clear all the data inside every observers
   */
  clearObservers() { 
    this.observers['grade_type'].updateValue(DEFAULT_VALUES['grade_type']);
    this.observers['region'].updateValue(DEFAULT_VALUES['region']);
    this.observers['application_id'].updateValue('');
    this.observers['applicant_name'].updateValue('');
    this.observers['note'].updateValue('');
  }

  /**
   * clear all data inside all relevant data handlers 
   */
  clearDataHandler() {
    const rowDataHandler = RowDataHandler.getInstance(); 
    const requestDataHandler = RequestDataHandler.getInstance(); 
    rowDataHandler.clear();
    requestDataHandler.clearData();
  }
}

export default ClearPageContentCommand;