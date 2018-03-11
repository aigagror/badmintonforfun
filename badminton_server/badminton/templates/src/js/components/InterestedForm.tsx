import * as React from "react";
import axios from 'axios';

export interface InterestedProps { 

}

interface InterestedState {
	message: string;
	title: string;
}

const email_name = "email";
const api_url = "/mock/interested.json";

export class InterestedForm extends React.Component<InterestedProps, InterestedState> {

	constructor(props: InterestedProps) {
	    super(props);
	    this.state = {
	    	message: null,
	    	title: null
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
				message: response.data.message,
				title: response.data.title
			});
		})
		.catch((error: any) => {
			console.log(error);
		});
	}

	resetState() {
		this.setState({
			message: null,
			title: null
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
	    {
	    	this.state.message !== null ?
	    		<div className="message-div">
	    			<h4>{this.state.title}</h4>
	    			<p>{this.state.message}</p>
	    			<button onClick={this.resetState}>Ok</button>
	    		</div> :
	    		<div></div>
	    }
	    </>);
	}
}