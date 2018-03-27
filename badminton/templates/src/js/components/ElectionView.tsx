import * as React from "react";
import {Slider} from "../common/Slider";
import {Popup} from "../common/Popup";
import axios from 'axios';
import { RegisterElectionView } from "./RegisterElection";
import { RadioButton } from '../common/RadioButton';
import { Select, Option } from "../common/Select";

const election_url = '/api/election/';
const campaign_url = '/api/campaign/';
const election_create_url = '/api/election/create/';

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
	}

	render() {
		return (<div>
			<div className="row">
			<div className="col-1 row-2">
			<RadioButton name={this.props.role} id={""+this.props.person.id}
				value={this.props.person.id} defaultChecked={this.props.person.name} />
			</div>

			<div className="col-8 row-2 election-label-div">
			<label htmlFor={""+this.props.person.id} className="election-label">{this.props.person.name}</label>
			</div>
			</div>

			<div className="row col-offset-1 col-10">
			<p>Pitch: {this.props.person.pitch}</p>
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
					return <ElectionCandidate person={key} role={this.props.role} key={idx}/>
				})
			}
			</div>
			);
	}
}

type ElectionData = ElectionUp | ElectionDown;

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

		this.deleteElection = this.deleteElection.bind(this);
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

	deleteElection() {
		console.log(this.props.id);
		axios.delete(election_url, {
		  headers: { 'Content-Type': 'text/plain' },
		  data: JSON.stringify({id: this.props.id,}),
		})
		.then((res: any) => {
			this.props.refresh();
			console.log("delete");
		})
		.catch((res: any) => {
			console.log(res);
		})

	}

	render() {
		return (<>
		<div className="grid">
		<button onClick={this.deleteElection}>Delete Election</button>
		<form onSubmit={this.submitVotes}>
		{
			this.state.campaigns.map((campaign: any, idx: number) => { 
				return <ElectionRole role={campaign[0]} candidates={campaign[1]} key={idx}/>
			})
		}
		<div className="row row-offset-2">
		<button type="submit">Submit Votes</button>
		</div>
		</form>
		{ this.state.popup !== null && this.state.popup }
		</div>
		<RegisterElectionView roles={this.props.roles}/>
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
			<p>{this.props.message}</p> <button onClick={this.createElection}>Create</button>
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
	const ret: any = {};
	for (var i of res.order) {
		ret[i] = [];
	}

	for (var campaigner of res.campaigns) {
		ret[campaigner.job].push(campaigner);
	}
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

	performRequest() {
		const _this_ref = this;

		axios.get(election_url)
			.then(res => {
				const status = res.data.status;
				var pack;
				if (status === "up") {
					const hierarchy = convertResponseToHierarchy(res.data);
					const pack = <ElectionUp order={res.data.order} 
						id={res.data.id}
						campaigns={hierarchy} 
						roles={res.data.order} 
						refresh={this.performRequest}/>;

					_this_ref.setState({
						election_data: pack,
						election: LoadingState.Loaded,
						up: status
					})
				} else if (status === "down") {
					_this_ref.setState({
						election_data: <ElectionDown message={res.data.message || "Not Up"} refresh={this.performRequest}/>,
						election: LoadingState.Loaded,
						up: status
					})
				} else {
					_this_ref.setState({
						election_data: <ElectionResults results={res.data.election_data} />,
						election: LoadingState.Loaded,
						up: status
					})
				}
			})
			.catch(res => {
				this.setState({
					error: res,
				});
			});
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