import * as React from "react";

export class InterestedForm extends React.Component<any, any> {

	render() {
	    return (<>
	    <div className="grid row row-offset-2">
	    	<div className="col-offset-4 col-6">
		    	<button className="interaction-style" onClick={() => {window.location.href = '/login'}}>Register</button>
		    </div>
	    </div>
	    { this.state.popup !== null && this.state.popup }
	    </>);
	}
}