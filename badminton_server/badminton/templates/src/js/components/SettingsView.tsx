import * as React from "react";
import axios from 'axios';
import { Slider } from '../common/Slider';

enum LoadingState {
    Loading,
    Loaded,
}

const reg_url = '/mock/regular_settings.json';
const member_url = '/mock/board_settings.json';

class StandardSettings extends React.Component<any, any> {

	render() {
		return <p>Standard</p>
	}
}

class BoardSettings extends React.Component<any, any> {

	render() {
		return <p>Board</p>
	}
}

export class SettingsView extends React.Component<any, any> {

	constructor(props: any) {
		super(props);
		this.switch = this.switch.bind(this);

		this.state = {
			regular_settings: null,
			board_settings: null,
			loading: true,
			regular: true,
		}
	}

	performRequest() {

		//... Regular Stuff
		const regular = this.state.regular;

		//... Board Stuff
		if(this.state.regular) {
			axios.get(reg_url)
			.then((res) => {
				this.setState({
					loading: false,
					regular: !regular,
					regular_settings: <StandardSettings />
				})
			})
			.catch((res) => {

			})
		} else {
			axios.get(reg_url)
			.then((res) => {
				this.setState({
					loading: false,
					regular: !regular,
					regular_settings: <StandardSettings />
				})
			})
			.catch((res) => {

			})

			axios.get(member_url)
				.then((res) => {
					this.setState({
						loading: false,
						regular: !regular,
						board_settings: <BoardSettings />
					})
				})
				.catch((res) => {
					
				})
		}

	}

	componentDidMount() {
		this.performRequest();
	}

	switch(event: Event) {
		if (this.state.loading === true) {
			return;
		} else {
			this.performRequest();
		}
	}

	render() {
		return <div className="election-view">
	    	<h2>Toggle Board View</h2>
	    	<Slider change={this.switch} />

	    	{ this.state.regular_settings !== null &&
	    		this.state.regular_settings }

	    	{ this.state.board_settings !== null &&
	    		this.state.board_settings }
	    </div>
	}
}