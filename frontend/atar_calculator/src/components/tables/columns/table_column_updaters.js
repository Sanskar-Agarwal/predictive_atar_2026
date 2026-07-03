/**
 * updater to change the weighting based on the subject selected
 * @param {string} enteredSubject - the subject that has been entered
 * @param {number} subjectWeighting - the weighting of the entered subject
 * @param {function} setEnteredWeighting - function used to change the weighting
 */
export function updateSubjectWeighting(enteredSubject, subjectWeighting, setEnteredWeighting) {
    if (enteredSubject) {
        if (subjectWeighting[enteredSubject]) {
            // Assuming setEnteredWeighting is a passed function to update state
            setEnteredWeighting(subjectWeighting[enteredSubject]);
        } else {
            subjectWeighting[enteredSubject] = 0;
        }
    }
}