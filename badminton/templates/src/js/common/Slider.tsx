import * as React from "react";

export interface SliderProps { 
	change: (event: object) => any;
	checked?: boolean;
}

export class Slider extends React.Component<SliderProps, {}> {

	private selected: boolean;
	private inputElem: any;

	constructor(props: SliderProps) {
	    super(props);
	    this.onChange = this.onChange.bind(this);
	    // Since checked is optional, use a double !!
	    // To get a boolean value
	    this.selected = !!this.props.checked;
	}

	componentDidMount() {
		if (this.selected) {
	    	this.inputElem.checked = true;
	    }
	}

	onChange(event: object) {
		this.selected = !this.selected;
	    this.props.change(event);
	}

	render() {
	    return (<label className="switch">
				  <input type="checkbox" 
				  	onChange={this.onChange}
				  	ref={(input) => this.inputElem = input}/>
				  <span className="slider round"></span>
				</label>);
	}
}
