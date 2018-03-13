import * as React from "react";

export interface SliderProps { 
	change: (event: object) => any;
}

export class Slider extends React.Component<SliderProps, {}> {

	constructor(props: SliderProps) {
	    super(props);
	    this.onChange = this.onChange.bind(this);
	}

	onChange(event: object) {
	    this.props.change(event);
	}

	render() {
	    return (<label className="switch">
				  <input type="checkbox" onChange={this.onChange} />
				  <span className="slider round"></span>
				</label>);
	}
}
