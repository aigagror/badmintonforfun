import * as React from "react";

export interface ButtonProps { 
	text: string;
	href: string;
}

export class Button extends React.Component<ButtonProps, {}> {

	constructor(props: ButtonProps) {
	    super(props);
	    this.handleClick = this.handleClick.bind(this);
	}

	handleClick() {
	    document.location.href = this.props.href;
	}

	render() {
	    return <button onClick={this.handleClick} className="big-button faded">{this.props.text}</button>;
	}
}