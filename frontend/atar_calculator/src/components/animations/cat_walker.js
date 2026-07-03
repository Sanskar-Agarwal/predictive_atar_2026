// Library Imports
import { useState, useEffect } from 'react';

// Package Imports
import { 
    CatWalkRightState, 
    CatPetState,
} from './states/cat_states';

// CSS Imports
import '../../styles/animations/cat_walker.css';

/**
 * a webpage element used to display the walking cat animation 
 * @returns {JSX.Element} div elements to be displayed on the webpage
 */
function CatWalker({catAlive}) {
    const [catSprite, setCatSprite] = useState('');
    const [xPos, setXPos] = useState(0);
    const [catState, setCatState] = useState(new CatWalkRightState(setXPos));
    const [isPet, setIsPet] = useState(false);

    useEffect(() => {
        const interval = setInterval(() => setCatSprite(animate(catState, setCatState))
        , 300);
        return () => clearInterval(interval);
    }, [xPos, catState]);

    const handleOnPet = () => {
        if (!isPet) {
            setCatState(new CatPetState(catState, setIsPet));
        } else {
            setCatState(new CatWalkRightState(setXPos));
        }
    };

    const style = {
        height: catAlive ? '80px' : '0px',
        width: catAlive ? '100px' : '0px'
    }

    return (
        <div className='cat-container' style={style}>
            <img
                src={catSprite}
                alt='Cat Walker'
                onClick={handleOnPet}
                hidden={catAlive ? false : true}
                style={{
                    transform: `translateX(${xPos}px)`,
                }}
            />
        </div>
    );
} 

/**
 * method used to run the animation of the cat sprite  
 * @param {Object} petState the state object to determined if the cat is being petted right now
 * @param {Object} catState the state object to determined what walking state the cat is at
 * @param {function} setPetState function used to set the petState for the cat
 * @param {function} setCatState function used to set the walkingSate for the cat
 * @returns {Object} the cat sprite to be animated
 */
function animate( catState, setCatState) {
    return (catState.animate(setCatState));
}

export default CatWalker;

