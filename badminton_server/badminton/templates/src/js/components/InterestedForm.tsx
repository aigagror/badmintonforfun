import * as React from "react";
import axios from 'axios';
import { Popup } from '../common/Popup';

export interface InterestedProps { 

}

const email_name = "email";
const api_url = "/mock/interested.json";

export class InterestedForm extends React.Component<InterestedProps, any> {

	constructor(props: InterestedProps) {
	    super(props);
	    this.state = {

	    }
	    this.handleSubmit = this.handleSubmit.bind(this);
	    this.resetState = this.resetState.bind(this);
	}

	handleSubmit(event: any) {
		event.preventDefault();
		axios.get(api_url, {
			params: {
			  email: event.target[email_name].value
			}
		})
		.then((response: any) => {
			this.setState({
				popup: <Popup title={response.data.title} message={response.data.message} 
					callback={this.resetState}/>,
			});
		})
		.catch((error: any) => {
			console.log(error);
		});
	}

	resetState() {
		this.setState({
			popup: null
		});
	}


	render() {
	    return (<>
	    <form onSubmit={this.handleSubmit}>
	    <div className="col-center-4">
	    	<label>Email:
        	<input type="text" id="email" name={email_name} placeholder="netid@illinois.edu"/>
        	</label>
        </div>

        <div className="col-center-4">
	    	<input type="submit" value="Submit" className="big-button" />
        </div>
	    </form>
	    { this.state.popup !== null && this.state.popup }
	    </>);
	}
}