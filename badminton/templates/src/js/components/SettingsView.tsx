import * as React from "react";
import axios from 'axios';
import { Slider } from '../common/Slider';
import { Popup } from '../common/Popup';
import { Select, Option } from '../common/Select';

enum LoadingState {
    Loading,
    Loaded,
}

const reg_url = '/api/settings/member/';
const member_url = '/mock/board_settings.json';

class OptionSetting extends React.Component<any, any> {

	render() {
		const options = this.props.data.options.map((option: any, idx: number) =>
		 	new Option(option.value, option.name));
		return <Select 
		name={this.props.data.name} 
		defaultValue={this.props.data.value}
		onChange={this.props.change}
		options={options} />
	}
}

class BoolSetting extends React.Component<any, any> {

	render() {
		return <Slider 
			change={(e: any) => this.props.change(e.target.value === "on" ? true: false)} 
			checked={this.props.data.value} />
	}
}

class TextSetting extends React.Component<any, any> {

	render() {
		return <input 
			type="text" 
			name={this.props.data.name} 
			onChange={(e: any) => this.props.change(e.target.value)}
			defaultValue={this.props.data.value} />
	}
}

class LongTextSetting extends React.Component<any, any> {

	render() {
		return <textarea name={this.props.data.name} 
			onChange={(e: any) => this.props.change(e.target.value)} 
			defaultValue={this.props.data.value} />
	}
}

class StandardSettings extends React.Component<any, any> {

	private previousTimeout: any;

	constructor(props: any) {
		super(props);

		this.decideComponent = this.decideComponent.bind(this);
		const params: any = {
		};
		for (let setting of this.props.data) {
			params[setting.name] = setting.value
		}

		this.state = {
			popup: null,
			settings: params
		}
		this.previousTimeout = null;
		this.repost = this.repost.bind(this);
	}

	repost() {
		if (this.previousTimeout !== null) {
			clearInterval(this.previousTimeout);
			this.previousTimeout = null;
		}
		let data = new FormData();
		for (let key of Object.keys( this.state.settings )) {
			data.append(key, this.state.settings[key]);
		}

		axios.post(reg_url, data)
			.then((res: any) => {
				console.log(res);
				this.setState({
					popup: <Popup title="Saved" message="Your data has been saved" callback={() => 
						this.setState({popup:null})} />
				})
			})
			.catch((res: any) => {
				console.log(res);
			})
	}

	decideComponent(setting: any, key: any) {
		const updateFunctor = (val: any) => {
			const swap = Object.assign({}, this.state.settings);
			swap[setting.name] = val;
			this.setState({settings: swap});
		}
		if (setting.type === "bool") {
			return <BoolSetting data={setting} key={key} 
				change={updateFunctor}/>
		} else if (setting.type === "option") {
			return <OptionSetting data={setting} key={key} change={updateFunctor}/>
		} else if (setting.type === "text") {
			return <TextSetting data={setting} key={key} change={updateFunctor} />
		} else if (setting.type === "long_text") {
			return <LongTextSetting data={setting} key={key} change={updateFunctor} />
		}
	}



	render() {
		return <>
		<div className="grid">
		{
			this.props.data.map((setting: any, idx: number) => {
				return <div className="row" key={idx}>

				<div className="col-6 col-es-12">
				<h2>{setting.display_name}</h2>
				</div>

				<div className="col-6 col-es-12">
					{this.decideComponent(setting, idx)}
				</div>
				</div>
			})
		}
		<button onClick={this.repost}>Save</button>
		</div>
		{ this.state.popup && this.state.popup }
		</>
	}
}

class BoardSettings extends React.Component<any, any> {

	constructor(props: any) {
		super(props);
		this.deleteMember = this.deleteMember.bind(this);
		this.deleteCourt = this.deleteCourt.bind(this);
		this.state = {
			data: null,
		}
	}

	componentDidMount() {
		axios.get(member_url)
			.then((res) => {
				this.setState({
					data: res.data,
					memberTypes: res.data.memberTypes.map((role: string) => new Option(role, role)),
					courtTypes: res.data.courtTypes.map((role: string) => new Option(role, role))
				});
			})
			.catch((res) => {

			})
	}

	deleteMember() {

	}

	deleteCourt() {

	}

	render() {
		if (this.state.data === null) {
			return <div>
			<h3>Board Member only Views</h3>
			<p>Loading</p>
			</div>
		}

		return <div className="grid">
		<h2>Board Member Options</h2>
		<h3>Members</h3>
		{
			this.state.data.members.map((member: any, idx: number) => {
				return <div key={idx} className="row">
				<div className="col-5 col-es-12">
				<h4>{member.name}</h4> 
				</div>
				<div className="col-4 col-es-12">
				<Select 
					options={this.state.memberTypes}
					defaultValue={member.type}
					onChange={(i: any) => {console.log(i)}}
					name={member.id} />
				</div>
				<div className="col-3 col-es-12">
				<button>Delete</button>
				</div>
				</div>
			})
		}
		<h3>Courts</h3>
		{
			this.state.data.courts.map((court: any, idx: number) => {
				return <div key={idx} className="row">
				<div className="col-5 col-es-12">
				<h4>{court.name}</h4> 
				</div>
				<div className="col-4 col-es-12">
				<Select 
					options={this.state.courtTypes}
					defaultValue={court.type}
					onChange={(i: any) => {console.log(i)}}
					name={"courts" + idx} />
				</div>
				<div className="col-3 col-es-12">
				<button>Delete</button>
				</div>
				</div>
			})
		}
		</div>
	}
}

export class SettingsView extends React.Component<any, any> {

	constructor(props: any) {
		super(props);
		this.switch = this.switch.bind(this);
		this.performRequest = this.performRequest.bind(this);
		
		this.state = {
			regular_settings: null,
			board_settings: null,
			loading: true,
		}
	}

	performRequest() {
		axios.get(reg_url)
		.then((res) => {
			this.setState({
				loading: false,
				regular_settings: <StandardSettings data={res.data}/>,
				board_settings: null
			})
		})
		.catch((res) => {

		})
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
	    	{ this.state.regular_settings !== null &&
	    		this.state.regular_settings }

	    	{ this.state.board_settings !== null &&
	    		this.state.board_settings }
	    </div>
	}
}