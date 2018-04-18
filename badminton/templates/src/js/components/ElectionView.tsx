import * as React from "react";
import {Slider} from "../common/Slider";
import {Popup} from "../common/Popup";
import axios from 'axios';
import { RegisterElectionView } from "./RegisterElection";
import { RadioButton } from '../common/RadioButton';
import { Select, Option } from "../common/Select";
import { xsrfCookieName, xsrfHeaderName, getMemberId, isBoardMember } from '../common/LocalResourceResolver';
import { EditableTextarea } from '../common/EditableTextarea';
import DatePicker from 'react-datepicker';
import {objectToFormData} from '../common/Utils';
declare var require: Function;
const moment = require('moment');

const election_url = '/api/election/get/';
const election_edit_url = '/api/election/edit/';
const campaign_url = '/api/campaign/';
const election_create_url = '/api/election/create/';
const cast_vote_url = '/api/election/vote/';
const my_vote_url = '/api/election/vote/get/'

axios.defaults.xsrfCookieName = xsrfCookieName();
axios.defaults.xsrfHeaderName = xsrfHeaderName();

enum LoadingState {
    Loading,
    Loaded,
}

function capitalize(str: string): string {
	return str.charAt(0).toUpperCase() + str.slice(1);
}

class ElectionCandidate extends React.Component<any, any> {
	person: any;
	role: string;
	constructor(props: any) {
		super(props);
		this.deleteCandidate = this.deleteCandidate.bind(this);
		this.updateCandidate = this.updateCandidate.bind(this);
		this.state = {
			pitch: this.props.person.pitch,
		}
	}

	async deleteCandidate(event: any) {
		axios.delete(campaign_url, {
		  headers: { 'Content-Type': 'text/plain' },
		  data: JSON.stringify({
		  	id: this.props.person.id,
		  	job: this.props.person.job,
		  	email: this.props.person.campaigner,
		  }),
		})
		.then((res: any) => {
			this.props.refresh()
		})
		.catch((res: any) => {
			console.log(res);
		})

		event.preventDefault();
	}

	async updateCandidate(event: any) {
		const data: any = {
			id: this.props.person.election,
			job: this.props.person.job,
			pitch: this.state.pitch,
			email: this.props.person.campaigner,
		}
		try {
			const res = await axios.post(campaign_url, objectToFormData(data));
		} catch(err) {
			console.log(err);
		}
	}

	render() {
		return (<div>
			<div className="row">
			<div className="col-1 row-2">
			<RadioButton name={this.props.role} id={this.props.person.id}
				value={this.props.person.id} defaultChecked={this.props.voted.includes(this.props.person.id)} 
				onChange={async (ev:any) => {
					if (!ev.target.checked) return;

					let data = new FormData();
					data.append('voter', ""+getMemberId());
					data.append('campaign', ev.target.value);
					try {
						const res = await axios.post(cast_vote_url, data);
					} catch (err) {
						console.log(err);
					}
				}
				} />
			</div>

			<div className="col-8 row-2 election-label-div">
			<label htmlFor={""+this.props.person.id} className="election-label">
				{this.props.person.first_name + ' ' + this.props.person.last_name}
			</label>
			</div>

			</div>

			<div className="row col-offset-1 col-12">
			<EditableTextarea 
				initValue={this.state.pitch} 
				onSave={this.updateCandidate} 
				onDelete={this.deleteCandidate}
				editableOverride={isBoardMember() || (this.props.person.id !== getMemberId())} />
			</div>
			</div>
			);
	}
}

class ElectionRole extends React.Component<any, any> {
	constructor(props: any) {
		super(props);
	}

	render() {
		return (<div>
			<div className="row">
			<div className="col-3">
			<h3>{this.props.role}</h3>
			</div>
			</div>
			{
				this.props.candidates.map((key: any, idx: any) => {
					return <ElectionCandidate 
						person={key} 
						role={this.props.role} 
						key={idx}
						refresh={this.props.refresh}
						voted={this.props.voted} />
				})
			}
			</div>
			);
	}
}

class ElectionUpBoardEditable extends React.Component<any, any> {
	constructor(props: any) {
		super(props);

		let end = this.props.endDate === null ? moment() : moment(this.props.endDate);
		this.state = {
			startDate: moment(this.props.startDate),
			endDate: end,
			voted: this.props.voted,
		}
		this.deleteElection = this.deleteElection.bind(this);
	}
	async deleteElection() {
		try {
			let res = await axios({
		        method: 'DELETE',
		        url: election_edit_url,
		        data: {id: this.props.id}
		    });
			window.location.reload(true);
		} catch (err) {
			console.log(err);
		}
	}

	updateElection (attr: string) {
		return async (date: any) => {
			const setter: any = Object.assign({}, this.state);
			setter[attr] = date;
			this.setState(setter);
			const dateFormat = "YYYY-MM-DD";
			try {
				let res = await axios.post(election_edit_url,
			        objectToFormData({
			        	id: this.props.id, 
			        	startDate: setter.startDate.format(dateFormat),
			        	endDate: setter.endDate.format(dateFormat),
			        })
			    );
				window.location.reload(true);
			} catch (err) {
				console.log(err);
			}
		}
	}

	render() {
		return <div className="row">
				<h4>Members Only!</h4>
				<div className="col-4">
				<h5>Start Date</h5>
				<DatePicker
			        selected={this.state.startDate}
			        onChange={this.updateElection('startDate')}
			        className="interaction-style"
			    />
				</div>
				<div className="col-4">
				<h5>End Date</h5>
				<DatePicker
			        selected={this.state.endDate}
			        onChange={this.updateElection('endDate')}
			        className="interaction-style"
			    />
				</div>
				<div className="col-4">
					<h5>Warning: Deletes all Votes</h5>
					<button className="interaction-style" onClick={this.deleteElection}>Delete Election</button>
				</div>
			</div>
	}
}

class ElectionUp extends React.Component<any, any> {

	constructor(props: any) {
		super(props);
		const campaigns: any[] = [];
		for(let key in this.props.order) {
			let elem = this.props.order[key];
			campaigns.push([elem, this.props.campaigns[elem]]);
		}

		this.state = {
			popup: null,
			campaigns: campaigns,
		}
		this.submitVotes = this.submitVotes.bind(this);
	}

	submitVotes(event: any) {
		event.preventDefault();
		for(let key in this.props.order) {
			let elem = this.props.order[key];
			console.log("For: " + elem + " Userid: " + event.target[elem].value);
		}
		this.setState({
			popup: <Popup title="Submitted!" 
				message="Submit as many times as you want before the deadline"
				callback={()=>{
					this.setState({popup: null});
				}} />
		});
	}

	render() {
		return (<>
		<div className="grid row-offset-1">

		{isBoardMember() && <ElectionUpBoardEditable 
			refresh={this.props.refresh}
			id={this.props.id}
			startDate={this.props.startDate}
			endDate={this.props.endDate} />}

		<form onSubmit={this.submitVotes}>
		{
			this.state.campaigns.map((campaign: any, idx: number) => { 
				return <ElectionRole 
					role={campaign[0]} 
					candidates={campaign[1]} 
					key={idx} 
					refresh={this.props.refresh}
					voted={this.props.voted}/>
			})
		}
		<div className="row row-offset-2">
		<button className="interaction-style" type="submit">Submit Votes</button>
		</div>
		</form>
		{ this.state.popup !== null && this.state.popup }
		</div>
		<RegisterElectionView roles={this.props.order}/>
		</>);
	}
}

function dateNow() {
	const d = new Date();
    var month = '' + (d.getMonth() + 1);
    var day = '' + d.getDate();
    var year = d.getFullYear();

    if (month.length < 2) month = '0' + month;
    if (day.length < 2) day = '0' + day;

    return [year, month, day].join('-');
}

class ElectionDown extends React.Component<any, any> {
	constructor(props: any) {
		super(props);

		this.createElection = this.createElection.bind(this);
	}

	createElection() {
		let data = new FormData();
		data.append('startDate', dateNow());
		axios.post(election_create_url, data, {
			headers: {"Content-Type": "multipart/form-data"}
		})
		.then((res: any) => {
			this.props.refresh()
		}).catch((res: any) => {
			console.log(res);
		})
	}

	render() {
		return (<>
			<p>{this.props.message}</p> <button className="interaction-style"  onClick={this.createElection}>Create</button>
			</>);
	}
}

class ElectionResults extends React.Component<any, any> {

	constructor(props: any) {
		super(props);
	}


	render() {
		return <div>
			{
				this.props.results.map((role: any, idx: number) => {
					return <div key={idx}>
					<h4>{role.role}</h4>
					{
						role.votes.map((person: any, idx2: number) => {
							return <div key={idx2}>
								{person.name}:{person.num_votes}
							</div>;
						}
						)
					}
					</div>

				})
			}
			</div>;
	}
}

class Campaign {
	campaigner: string;
	job: string;
	election: string;
	id: number;
	pitch: string;
}

class CampaignResponse {
	status: string;
	id: string;
	endDate: string;
	date: string;
	order: string[];
	campaigns: Campaign[];
}

const convertResponseToHierarchy = (res: CampaignResponse): any => {
	console.log(res);
	const ret: any = {};
	const order = res.order;
	for (var i of order) {
		ret[i] = [];
	}

	for (var j of res.campaigns) {
		let temp = j as any;
		ret[temp.campaign.job].push(temp.campaign);
	}
	ret.order = order;
	return ret;
}

export class ElectionView extends React.Component<{}, any> {

	private switchElem: any;

	constructor(props: any) {
	    super(props);
	    this.state = {
	    	election: LoadingState.Loading,
	    	error: null,
	    }
	    this.performRequest = this.performRequest.bind(this);
	    this.componentDidMount = this.componentDidMount.bind(this);
	}

	async performRequest() {
		try {
			const res = await axios.get(election_url);

			const status = res.data.status;
			var pack;
			if (status === "up") {
				const hierarchy = convertResponseToHierarchy(res.data);
				const res2 = await axios.get(my_vote_url + getMemberId());
				const selected = res2.data.votes.filter((e: any) => e.id !== getMemberId())
									.map((e: any) => e.campaign);

				const pack = <ElectionUp order={res.data.order} 
					id={res.data.election.id}
					startDate={res.data.election.date}
					endDate={res.data.election.endDate}
					campaigns={hierarchy} 
					roles={hierarchy.order}
					voted={selected}
					refresh={this.performRequest}/>;

				this.setState({
					election_data: pack,
					election: LoadingState.Loaded,
					up: status
				})
			} else if (status === "down") {
				this.setState({
					election_data: <ElectionDown message={res.data.message || "Not Up"} 
						refresh={this.performRequest}/>,
					election: LoadingState.Loaded,
					up: status
				})
			} else {
				this.setState({
					election_data: <ElectionResults results={res.data.election_data} />,
					election: LoadingState.Loaded,
					up: status
				})
			}
		} catch (res) {
			console.log(res);
			this.setState({
				error: res,
			});
		}
	}


	componentDidMount() {
		this.performRequest();
	}

	render() {
		if (this.state.error !== null) {
			return <p> An error has occurred "{this.state.error}"</p>
		}
	    return (
	    	<div className="grid row">
	    	<div className="col-offset-2 col-8">
    		{
    			this.state.election === LoadingState.Loading ?
    			<p> Loading </p> :
    			this.state.election_data
    		}
    		</div>

	    	</div>);
	}
}