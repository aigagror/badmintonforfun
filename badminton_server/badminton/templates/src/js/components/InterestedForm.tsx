import * as React from "react";

export interface InterestedProps { 

}

export class InterestedForm extends React.Component<InterestedProps, {}> {

	constructor(props: InterestedProps) {
	    super(props);
	    this.handleSubmit = this.handleSubmit.bind(this);
	}

	handleSubmit() {
		console.log("Submitted!");
		return false;
	}


	render() {
	    return <form onSubmit={this.handleSubmit} className="big-button">
	    <div className="col-center-4">
	    	<label>Email:
        	<input type="text" id="email" name="email" placeholder="netid@illinois.edu"/>
        	</label>
        </div>

        <div className="col-center-4">
	    	<input type="submit" value="Submit" className="big-button" />
        </div>
	    </form>;
	}
}