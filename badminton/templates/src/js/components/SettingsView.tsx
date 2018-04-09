import * as React from "react";
import axios from 'axios';
import { Slider } from '../common/Slider';
import { Popup } from '../common/Popup';
import { Select, Option } from '../common/Select';
import { isBoardMember } from '../common/LocalResourceResolver';

enum LoadingState {
    Loading,
    Loaded,
}

const reg_url = '/api/settings/member/';
const member_url = '/api/settings/members/all/';
const courts_url = '/api/settings/courts/';

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
			change={(e: any) => {
				this.props.change(e.target.checked ? 1 : 0)
			}} 
			checked={this.props.data.value} />
	}
}

class TextSetting extends React.Component<any, any> {

	render() {
		return <input 
			className="interaction-style"
			type="text" 
			name={this.props.data.name} 
			onChange={(e: any) => this.props.change(e.target.value)}
			defaultValue={this.props.data.value} />
	}
}

class LongTextSetting extends React.Component<any, any> {

	render() {
		return <textarea className="interaction-style" name={this.props.data.name} 
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
			clearTimeout(this.previousTimeout);
			this.previousTimeout = null;
		}
		this.previousTimeout = setTimeout(async () => {
			let data = new FormData();
			for (let key of Object.keys( this.state.settings )) {
				data.append(key, this.state.settings[key]);
			}
			try {
				let res = await axios.post(reg_url, data);
				console.log(res);
			} catch(res) {
				console.log(res);
			}

		}, 1000)

	}

	decideComponent(setting: any, key: any) {
		const updateFunctor = (val: any) => {
			const swap = Object.assign({}, this.state.settings);
			swap[setting.name] = val;
			this.setState({settings: swap});
			this.repost();
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
		</div>
		{ this.state.popup && this.state.popup }
		</>
	}
}

class MemberSettings extends React.Component<any, any> {

	constructor(props: any) {
		super(props);
		this.deleteMember = this.deleteMember.bind(this);
		this.performRequest = this.performRequest.bind(this);
		this.state = {
			members: null,
		}
	}

	performRequest() {
		axios.get(member_url)
			.then((res) => {
				this.setState({
					members: res.data.members,
					memberTypes: res.data.memberTypes.map((role: string) => new Option(role, role)),
				});
			})
			.catch((res) => {
				console.log(res);
			})
	}

	componentDidMount() {
		this.performRequest();
	}

	deleteMember(idx: number) {
		return () => {
			const toDelete = this.state.members[idx];
			axios.delete(member_url, { 
				data: { members: [toDelete] } 
			})
			.then((res: any) => {
				console.log(res);
				this.performRequest();
			})
			.catch((res: any) => {
				console.log(res);
			})
		}
	}

	alterMember(idx: number, toRole: any) {
		const toEdit = this.state.members[idx];
		toEdit.status = toRole
		axios.post(member_url, { 
			members: [toEdit]
		})
		.then((res: any) => {
			console.log(res);
			this.performRequest();
		})
		.catch((res: any) => {
			console.log(res);
		})
	}

	render() {
		if (this.state.members === null) {
			return <p>Loading</p>
		}

		return <>
		<h3>Members</h3>
		{
			this.state.members.map((member: any, idx: number) => {
				return <div key={idx} className="row">
				<div className="col-5 col-es-12">
				<h4>{member.first_name} {member.last_name}</h4> 
				</div>
				<div className="col-4 col-es-12">
				<Select 
					options={this.state.memberTypes}
					defaultValue={member.type}
					onChange={(role: any) => {this.alterMember(idx, role)}}
					name={member.member_id} />
				</div>
				<div className="col-3 col-es-12">
				<button 
					onClick={this.deleteMember(idx)} 
					className="interaction-style">
					Delete
				</button>
				</div>
				</div>
			})
		}
		</>
	}
}

class CourtSettings extends React.Component<any, any> {

	private courts_url: string = '/api/settings/courts';

	constructor(props: any) {
		super(props);

		this.state = {
			courts: null,
		}
	}

	async componentDidMount() {
		try {
			const res = await axios.get(this.courts_url);
			this.setState({
				courts: res.data.courts,
			})
		} catch (ex) {
			console.log(ex);
		}
	}

	render() {
		if (this.state.courts === null) {
			return null;
		}

		return <div>
		<h3>Courts</h3>
		{
			this.state.courts.map((court: any, idx: number) => {
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
		<button>Add a court</button>
		</div>
	}
}

class BoardSettings extends React.Component<any, any> {

	render() {
		return <div className="grid">
			<h2>Board Member Options</h2>
			<MemberSettings />
			<CourtSettings />
			</div>
	}
}


/*

*/

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
		if (isBoardMember()) {
			axios.get(reg_url)
			.then((res) => {
				this.setState({
					loading: false,
					regular_settings: <StandardSettings data={res.data}/>,
				})
			})
			.catch((res) => {
				console.log(res);
			})
		}
		else {
			axios.get(reg_url)
			.then((res) => {
				this.setState({
					loading: false,
					regular_settings: <StandardSettings data={res.data}/>,
					board_settings: null
				})
			})
			.catch((res) => {
				console.log(res);
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
	    	{ this.state.regular_settings !== null &&
	    		this.state.regular_settings }

	    	<BoardSettings />
	    </div>
	}
}