import * as React from 'react';

export class RadioButton extends React.Component<any, any> {

	private inputElem: any;
	private spanElem: any;

	constructor(props: any) {
		super(props);
		this.clicked = this.clicked.bind(this);
	}

	clicked() {
		if (this.inputElem.checked) {
			// We are unchecking it
			console.log("Hello");
			this.spanElem.classList.add("radio-swirl-back");
			window.setTimeout(() => {
				this.spanElem.classList.remove("radio-swirl-back");
			}, 500);
		}
	}

	render() {
		return <label className="radio-container">
			<input {...this.props} type="radio" 
				onClick={this.clicked} 
				ref={(input) => this.inputElem = input}/>
			<span className="radio-checkmark" ref={(input) => this.spanElem = input}></span>
			</label>
	}
}