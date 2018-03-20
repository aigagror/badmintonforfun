import * as React from "react";
import {Slider} from "../common/Slider";
import {Popup} from "../common/Popup";
import axios from 'axios';
import { RegisterElectionView } from "./RegisterElection";
import { RadioButton } from '../common/RadioButton';
import { Select, Option } from "../common/Select";

const election_url = '/mock/election_happening.json';
const election_not_url = '/mock/electionless.json';
const election_results_url = '/mock/election_results.json';

enum LoadingState {
    Loading,
    Loaded,
}

function capitalize(str: string): string {
	return str.charAt(0).toUpperCase() + str.slice(1);
}

function format(str: string): string {
	const splitted = str.split("_");
	return splitted.map((word: string) => capitalize(word)).join(" ");
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
			<h3>{format(this.props.role)}</h3>
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
			campaigns: campaigns,
			popup: null
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

export class ElectionView extends React.Component<{}, any> {

	private switchElem: any;
	private options: object;

	constructor(props: any) {
	    super(props);
	    this.state = {
	    	election: LoadingState.Loading,
	    }
	    this.performRequest = this.performRequest.bind(this);
	    this.switch = this.switch.bind(this);
	    this.componentDidMount = this.componentDidMount.bind(this);
	    this.options = [
	    			new Option("up", "Up"),
	    			new Option("down", "Down"),
	    			new Option("results", "Results"),
	    		];
	}

	performRequest(url: string) {
		const _this_ref = this;
		axios.get(url)
			.then(res => {
				const status = res.data.status;
				var pack;
				if (status === "up") {
					pack = <ElectionUp order={res.data.order} 
						campaigns={res.data.campaigns} 
						roles={Object.keys(res.data.campaigns).sort()} />;
				} else if (status === "down") {
					pack = <ElectionDown message={res.data.message} />;
				} else {
					pack = <ElectionResults results={res.data.election_data} />;
				}

				_this_ref.setState({
					election_data: pack,
					election: LoadingState.Loaded,
					up: status
				})
			});
	}


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
	}


	componentDidMount() {
		this.performRequest(election_url);
	}

	render() {
	    return (
	    	<div className="grid row">
	    	<div className="col-offset-2 col-8">

	    	<h2>Toggle Election Happening</h2>
	    	<Select onChange={this.switch} 
	    		options={this.options as Option[]} 
	    		defaultValue="up" 
	    		name="electionState" />
    		{
    			this.state.election === LoadingState.Loading ?
    			<p> Loading </p> :
    			this.state.election_data
    		}
    		</div>

	    	</div>);
	}
}