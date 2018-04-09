/**
 * Contains a popup view that need only to be rendered
 * To work. Appears in the middle of the screen and darkens
 * The body.
 */

import * as React from 'react';

const popupDisabledClass = "popup-disabled";
const popupScreenFadeClass = 'popup-screen-fade';
const popupFadeClass = 'popup-fade';

export class PopupProps {
	/* Method to call after closing */
	callback: () => void;
	title: string;
	message: string;
}

class PopupState {

}

export class Popup extends React.Component<PopupProps, PopupState> {

	private wrapperDiv: HTMLDivElement;
	private screenDiv: HTMLDivElement;

	constructor(props: PopupProps) {
		super(props);
		this.close = this.close.bind(this);
	}

	componentDidMount() {
		/* Programatically create a div to overlay everything and animate it in 
			Also force the body not to scroll */

		this.screenDiv = document.createElement('div');
		this.screenDiv.className = 'popup-screen';
		const body = document.querySelector('body');
		body.appendChild(this.screenDiv);
		body.classList.add(popupDisabledClass);
	}

	componentWillUnmount() {
		/* Remove the programatic div and let the body scroll */
		const body = document.querySelector('body');
		body.removeChild(this.screenDiv);
		body.classList.remove(popupDisabledClass);
	}

	close() {
		/* Animate everything in */
		
		this.wrapperDiv.classList.add(popupFadeClass);
		this.screenDiv.classList.add(popupScreenFadeClass);

		/* Cool so we can seperate concerns */
		const refCounter = {count: 0}
		const callback = () => {
			if (refCounter.count == 1) {
				this.props.callback();
			} else {
				refCounter.count += 1;
			}
		}
		/* 
		 * Since there are two animations going on we want to wait
		 * for both of them to end. So we use a reference counter
		 * in the form of a bound object.
		 */
		this.wrapperDiv.addEventListener('animationend', callback)
		this.screenDiv.addEventListener('animationend', callback)
	}

	render() {
		return (
			<div className="popup-div" ref={(input) => this.wrapperDiv = input}>
				<div className="grid row">
				<div className="row-1">
				<div className="col-11 popup-title-div">
					<h4 className="popup-title">{this.props.title}</h4>
				</div>
				</div>
				<div className="row-1">
				<div className="col-offset-1 col-11">
					<p className="popup-message">{this.props.message}</p>
				</div>
				</div>
				<div className="row-offset-10">
				<div className="col-offset-es-9 col-es-5 row-offset-es-9 col-offset-9 row-offset-11">
					<button className="popup-button interaction-style row-2" onClick={this.close}>✔</button>
				</div>
				</div>
				</div>
			</div>)
	}
}