import * as React from "react";
import {Slider} from "../common/Slider";
import {Popup} from "../common/Popup";
import axios from 'axios';
import { RegisterElectionView } from "./RegisterElection";

const election_url = '/mock/election_happening.json';
const election_not_url = '/mock/electionless.json';

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
			<div className="col-offset-2 col-1 row-2">
			<label className="radio-container">
			<input type="radio" name={this.props.role} id={""+this.props.person.id}
				value={this.props.person.id} className="election-check"
				defaultChecked={this.props.person.voted} />
			<span className="radio-checkmark"></span>
			</label>
			</div>

			<div className="col-8 row-2 election-label-div">
			<label htmlFor={""+this.props.person.id} className="election-label">{this.props.person.name}</label>
			</div>
			</div>

			<div className="row col-offset-2">
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
			<div className="col-offset-2 col-3">
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
		return (<div className="grid">
		<form onSubmit={this.submitVotes}>
		{
			this.state.campaigns.map((campaign: any, idx: number) => { 
				return <ElectionRole role={campaign[0]} candidates={campaign[1]} key={idx}/>
			})
		}
		<div className="row row-offset-2">
		<button type="submit" className="col-7 col-offset-2 row-2 election-submit">Submit Votes</button>
		</div>
		</form>
		{ this.state.popup !== null && this.state.popup }
		</div>);
	}
}

class ElectionDown extends React.Component<any, any> {
	message: string;
	constructor(props: any) {
		super(props);
	}

	render() {
		return (<p>{this.props.message}</p>);
	}
}

export class ElectionView extends React.Component<{}, any> {

	constructor(props: any) {
	    super(props);
	    this.state = {
	    	election: LoadingState.Loading,
	    }
	    this.performRequest = this.performRequest.bind(this);
	    this.switch = this.switch.bind(this);
	    this.componentDidMount = this.componentDidMount.bind(this);
	}

	performRequest(url: string) {
		const _this_ref = this;
		axios.get(url)
			.then(res => {
				const status = res.data.status;
				var pack;
				var up;
				var roles = null;
				if (status) {
					pack = <ElectionUp order={res.data.order} campaigns={res.data.campaigns} />;
					roles = Object.keys(res.data.campaigns).sort();
					up = true;
				} else {
					pack = <ElectionDown message={res.data.message} />;
					up = false;
				}

				_this_ref.setState({
					election_data: pack,
					roles: roles,
					election: LoadingState.Loaded,
					up: up
				})
			});
	}


	switch(event: Event) {
		if (this.state.election !== LoadingState.Loaded) {
			return;
		} else if (this.state.up) {
			this.performRequest(election_not_url);
		} else {
			this.performRequest(election_url);
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
	    	<Slider change={this.switch} checked={false}/>
    		{
    			this.state.election === LoadingState.Loading ?
    			<p> Loading </p> :
    			this.state.election_data
    		}

    		<div className="row-offset-2 col-offset-2 col-12">
    		{ this.state.roles && <RegisterElectionView roles={this.state.roles}/> }
    		</div>
    		</div>

	    	</div>);
	}
}