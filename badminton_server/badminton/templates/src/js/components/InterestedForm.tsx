import * as React from "react";
import axios from 'axios';
import { Popup } from '../common/Popup';
import { GoogleAuthButton } from './GoogleAuthButton';

const email_name = "email";
const api_url = "/mock/interested.json";

export class InterestedForm extends React.Component<any, any> {

	constructor(props: any) {
	    super(props);
	    this.state = {

	    }
	    this.handleSubmit = this.handleSubmit.bind(this);
	    this.resetState = this.resetState.bind(this);
	}

	handleSubmit(response: any) {
		console.log(response);
		return;/*
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
			this.setState({
				popup: <Popup title="Sorry!" message="There was an error on our end, please check back soon"
					callback={this.resetState}/>,
			});
		});*/
	}

	resetState() {
		this.setState({
			popup: null
		});
	}


	render() {
	    return (<>
	    <div className="grid row row-offset-2">
	    	<div className="col-offset-4 col-6">
		    	<GoogleAuthButton 
		    		onSuccess={this.handleSubmit}
		    		onFailure={this.handleSubmit} 
		    	/>
		    </div>
	    </div>
	    { this.state.popup !== null && this.state.popup }
	    </>);

	    /*(<>
	    <form onSubmit={this.handleSubmit}>
	    <div className="grid row-offset-2">
	    <div className="row">
	    <div className="col-offset-4 col-2">
	    	<label className="interested-label row-2">Email</label>
	    </div>
	    <div className="col-6">
        	<input type="text" id="email" name={email_name} placeholder="netid@illinois.edu" className="interested-short-field row-2"/>
        </div>
        </div>

        <div className="row">
	    <div className="col-offset-4 col-6">
	    	<input type="submit" value="Submit!" className="interested-submit row-offset-1 row-3" />
	    </div>
        </div>
        </div>
	    </form>
	    { this.state.popup !== null && this.state.popup }
	    </>);*/
	}
}