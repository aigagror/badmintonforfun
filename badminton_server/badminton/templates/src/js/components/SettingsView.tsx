import * as React from "react";
import axios from 'axios';
import { Slider } from '../common/Slider';

enum LoadingState {
    Loading,
    Loaded,
}

const reg_url = '/mock/regular_settings.json';
const member_url = '/mock/board_settings.json';

class OptionSetting extends React.Component<any, any> {

	render() {
		return <select name={this.props.data.name} defaultValue={this.props.data.value}>
		 { this.props.data.options.map((option: any, idx: number) => {
		 	return <option value={option.value} key={idx}>{option.name}</option>
		 }) 
		}
		</select>
	}
}

class BoolSetting extends React.Component<any, any> {

	render() {
		return <Slider change={() => {}} checked={this.props.data.value} />
	}
}

class StandardSettings extends React.Component<any, any> {

	constructor(props: any) {
		super(props);

		this.decideComponent = this.decideComponent.bind(this);
	}

	decideComponent(setting: any, key: any) {
		if (setting.type === "bool") {
			return <BoolSetting data={setting} key={key}/>
		} else if (setting.type === "option") {
			return <OptionSetting data={setting} key={key}/>
		}
	}

	render() {
		return <div className="grid">
		{
			this.props.data.map((setting: any, idx: number) => {
				return <div className="row" key={idx}>

				<div className="col-6">
				<h2>{setting.display_name}</h2>
				</div>

				<div className="col-6">
					{this.decideComponent(setting, idx)}
				</div>
				</div>
			})
		}
		</div>
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

		const regular = this.state.regular;

		if (this.state.regular) {
			axios.get(reg_url)
			.then((res) => {
				this.setState({
					loading: false,
					regular: !regular,
					regular_settings: <StandardSettings data={res.data}/>,
					board_settings: null
				})
			})
			.catch((res) => {

			})
		} else {

			axios.get(member_url)
				.then((res1) => {
					axios.get(reg_url)
						.then((res) => {
							this.setState({
								loading: false,
								regular: !regular,
								regular_settings: <StandardSettings data={res.data}/>,
								board_settings: <BoardSettings data={res1.data}/>
							})
						})
						.catch((res) => {

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