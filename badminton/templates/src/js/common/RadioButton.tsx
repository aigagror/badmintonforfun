/**
 * Acts as a this wrapper around radio button so that
 * Styles, animation, and consistency is maintained
 */

import * as React from 'react';

const reverseSwirlClass = "radio-swirl-back";


class RadioButtonState {

}

// Typescript doesn't support variadic types so the props have to be any
// To forward to the standard input field
export class RadioButton extends React.Component<any, RadioButtonState> {

	private inputElem: HTMLInputElement;
	private spanElem: HTMLSpanElement;

	constructor(props: any) {
		super(props);
		this.clicked = this.clicked.bind(this);
		this.hover = this.hover.bind(this);
	}

	hover(event: any) {
		// Must remove or after :hover disappears the
		// Animation will trigger again
		// No op to remove a class that does not exist
		if (event.animationName.includes('reverse')) {
			this.spanElem.classList.remove(reverseSwirlClass);
		}
	}

	componentDidMount() {
        // Make sure that the class has the reverse if checked for the first time
        this.spanElem.addEventListener('animationend', this.hover);
        this.clicked();
    }

    componentWillUnmount() {
    	this.spanElem.removeEventListener('animationend', this.hover);
    }

	clicked() {
		if (this.inputElem.checked) {
			// We are checking it
			this.spanElem.classList.add(reverseSwirlClass);
		}
	}

	render() {
		/* Forward all props using ... to the input field since this is supposed
		 * to be a thin wrapper around it */

		return <label className="radio-container">
			<input {...this.props} type="radio" 
				onClick={this.clicked} 
				ref={(input) => this.inputElem = input}/>
			<span className="radio-checkmark" ref={(input) => this.spanElem = input}></span>
			</label>
	}
}