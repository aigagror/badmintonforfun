import * as React from "react";
import {Slider} from "../common/Slider";
import {Popup} from "../common/Popup";
import axios from 'axios';
import { RegisterElectionView } from "./RegisterElection";
import { RadioButton } from '../common/RadioButton';
import { Select, Option } from "../common/Select";

const election_url = '/api/elections';
const campaign_url = '/api/campaign';

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
				value={this.props.person.id} defaultChecked={this.props.person.voted} />
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
		<div className="grid">
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

class ElectionDown extends React.Component<any, any> {
	constructor(props: any) {
		super(props);
	}

	render() {
		return (<p>{this.props.message}</p>);
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
	pitch: string;
	job: string;
	email: string;
	id: number;
	name: string;
}

class CampaignResponse {
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
	    //this.switch = this.switch.bind(this);
	    this.componentDidMount = this.componentDidMount.bind(this);
	}

	performRequest() {
		const _this_ref = this;
		const followUp = () => {
			axios.get(campaign_url)
				.then(res => {
					const casted = res.data as CampaignResponse;
					const hierarchy = convertResponseToHierarchy(casted);
					const pack = <ElectionUp order={casted.order} 
						campaigns={hierarchy} 
						roles={casted.order} />;
					_this_ref.setState({
						election_data: pack,
						election: LoadingState.Loaded,
						up: status
					})
				})
				.catch(res => {
					this.setState({
						error: res,
					});
				})
		}

		axios.get(election_url)
			.then(res => {
				const status = res.data.status;
				var pack;
				if (status === "up") {
					followUp();
				} else if (status === "down") {
					_this_ref.setState({
						election_data: <ElectionDown message={res.data.message} />,
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

/*
	switch(value: any) {
		if (this.state.election !== LoadingState.Loaded) {
			return;
		}

		if (value === 'up') {
			this.performRequest(election_url);
		} else if (value === 'down') {
			this.performRequest(election_not_url);
		} else {
			this.performRequest(election_results_url);
		}
	} */


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