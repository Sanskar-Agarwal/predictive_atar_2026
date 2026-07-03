// Asset Imports
import CatWalkRight from '../../../assets/gifs/cat_right.gif';
import CatWalkLeft from '../../../assets/gifs/cat_left.gif';
import CatStationary from '../../../assets/gifs/cat_station.gif';
import AngryCat from '../../../assets/gifs/angry_cat.gif';

class CatWalkingState {
    /**
     * State object for rendering the walking state for the cat
     * @param {function} setXPos used to set the XPos of the object
     * @param {number} increment the distance in which the xPos should be added to  
     */
    constructor(setXPos, increment) {
        this.increment = increment; 
        this.setXPos = setXPos;
    }

    /**
     * method used to animate the cat
     * @param {function} setCatState method used to change the state for the cat
     * @returns {Object} the sprite to be animated
     */
    animate(setCatState) {
        return null;
    }
}

export class CatWalkRightState extends CatWalkingState {
    /**
     * Cat State object used to represents when the cat is walking to the right
     * @param {function} setXPos function for setting the x position of the cat
     * @param {number} maxDistance the maximum distance the cat can move before state change, default 800
     * @param {number} increment the distance in which the xPos should be added to, default 5
     */
    constructor(setXPos, maxDistance=800, increment=5) {
        super(setXPos, increment);
        this.maxDistance = maxDistance;
        this.sprite = CatWalkRight;
    }

    /**
     * method used to animate the cat
     * @param {function} setCatState method used to change the walking state for the cat
     * @returns {Object} the sprite to be animated
     */
    animate(setCatState) {
        this.setXPos(
            (xPos) => {
                let newPos = xPos + this.increment;
                if (newPos > this.maxDistance) { 
                    newPos = this.maxDistance;
                    setCatState(new CatWalkLeftState(this.setXPos));
                }
                return newPos;
            }
        )
        return this.sprite;
    }
}

export class CatWalkLeftState extends CatWalkingState { 
    /**
     * Cat State object used to represents when the cat is walking to the left
     * @param {function} setXPos function for setting the x position of the cat
     * @param {number} minDistance the maximum distance the cat can move before state change, default 0 
     * @param {number} increment the distance in which the xPos should be added to, default 5
     */
    constructor(setXPos, minDistance=0, increment=10) {
        super(setXPos, increment);
        this.minDistance = minDistance;
        this.sprite = CatWalkLeft;
    }

    
    /**
     * method used to animate the cat
     * @param {function} setCatState method used to change the walking state for the cat
     * @returns {Object} the sprite to be animated
     */
    animate(setCatState) {
        this.setXPos(
            (xPos) => { 
                let newPos = xPos - this.increment;
                if (newPos < this.minDistance) { 
                    newPos = this.minDistance;
                    setCatState(new CatWalkRightState(this.setXPos));
                }
                return newPos;
            }
        )
        return this.sprite;
            
    }
}

export class CatPetState {
    /**
     * Cat State object used to represents when the cat is being pet
     * @param {Object} catState the previous state to restored at later time after the pet state ended
     * @param {function} setIsPet function that updated the cat pet status
     * @param {number} animatedDuration the duration of the petting animation, default: 8
     */
    constructor(catState, setIsPet,animatedDuration=8) {
        this.animatedDuration = animatedDuration;
        this.setIsPet = setIsPet;
        this.frame = 0;
        this.catState = catState;
        this.sprite = CatStationary;
        setIsPet(true);
    }
    
    /**
     * method used to animate the cat
     * @param {function} setPetState method used to change the petting state for the cat
     * @returns {Object} the sprite to be animated
     */
    animate(setCatState) {
        if (this.frame >= this.animatedDuration) {
            this.setIsPet(false);
            setCatState(this.catState);
        }
        this.frame += 1;
        return this.sprite;
    }
}

export class AngryCatState {
    constructor(catState, setShowCat, animatedDuration=8) {
        this.catState = catState;
        this.setShowCat = setShowCat;
        this.animatedDuration = animatedDuration;
        this.frame = 0;
        this.sprite = AngryCat;
    }

    animate(setCatState=()=>{}) {
        if (this.frame >= this.animatedDuration) {
            this.setShowCat(false);
            setCatState(this.catState);
        }
        this.frame += 1;
        return this.sprite;
    }
}
