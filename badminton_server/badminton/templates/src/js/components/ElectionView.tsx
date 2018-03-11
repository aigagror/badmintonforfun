import * as React from "react";
import {Slider} from "./Slider";
import axios from 'axios';

enum LoadingState {
    Loading,
    Loaded,
}

abstract class HigherOrderComponent {
	constructor() {
		this.render = this.render.bind(this);
	}

	abstract render(): any;
}

class ElectionCandidate extends HigherOrderComponent {
	person: any;
	role: string;
	constructor(person: any, role: string) {
		super();
		this.person = person;
		this.role = role;
	}

	render() {
		return (<div>
			<p>Name: {this.person.name}</p>
			<p>Pitch: {this.person.pitch}</p>
			{this.person.voted ? 
				<input type="radio" name={this.role} value={this.person.id} checked /> :
				<input type="radio" name={this.role} value={this.person.id} />
			}
			</div>
			);
	}
}

class ElectionRole extends HigherOrderComponent {
	role: string;
	candidates: ElectionCandidate[];
	selected: any;
	constructor(name: string, candidates: any) {
		super();
		this.role = name;
		this.candidates = [];
		for (let i in candidates) {
			let candidate = candidates[i];
			const obj = new ElectionCandidate(candidate, this.role);
			this.candidates.push(obj);
		}
		this.selected = null;
	}

	render() {
		return (<div>
			<h3>{this.role}</h3>
			{
				this.candidates.map((key, idx) => {
					return key.render();
				})
			}
			</div>
			);
	}
}

class ElectionUp extends HigherOrderComponent {
	candidates: any;
	order: string[];
	campaigns: any;

	constructor(data: any) {
		super();
		this.order = data.order;
		this.campaigns = [];
		for(let key in this.order) {
			let elem = this.order[key];
			this.campaigns.push(new ElectionRole(elem, data.campaigns[elem]));
		}
		this.submitVotes = this.submitVotes.bind(this);
	}

	up() {
		return true;
	}

	submitVotes(event: any) {
		event.preventDefault();
		for(let key in this.order) {
			let elem = this.order[key];
			console.log("For: " + elem + " Userid: " + event.target[elem].value);
		}
	}

	render() {
		return (<form onSubmit={this.submitVotes}>{
			this.campaigns.map((campaign: any, idx: number) => { 
				return campaign.render() 
			})
		}<button type="submit">Submit Votes</button>
		</form>);
	}
}

class ElectionDown extends HigherOrderComponent {
	message: string;
	constructor(data: any) {
		super();
		this.message = data.message;
	}

	up() {
		return false;
	}

	render() {
		return (<p>{this.message}</p>);
	}
}

type ElectionData = ElectionUp | ElectionDown;

interface ElectionState {
	election: LoadingState;
	election_data?: ElectionData;
}

export interface ElectionProps { 
}

const election_url = '/mock/election_happening.json';
const election_not_url = '/mock/electionless.json'



export class ElectionView extends React.Component<any, any> {

	constructor(props: ElectionProps) {
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
				if (status) {
					pack = new ElectionUp(res.data);
				} else {
					pack = new ElectionDown(res.data);
				}
				_this_ref.setState({
					election_data: pack,
					election: LoadingState.Loaded
				})
			});
	}


	switch(event: Event) {
		if (this.state.election !== LoadingState.Loaded) {
			return;
		} else if (this.state.election_data.up()) {
			this.performRequest(election_not_url);
		} else {
			this.performRequest(election_url);
		}
	}


	componentDidMount() {
		this.performRequest(election_url);
	}

	render() {
	    return (<div className="election-view">
	    	<h2>Toggle datum</h2>
	    	<Slider change={this.switch} />
    		{
    			this.state.election === LoadingState.Loading ?
    			<p> Loading </p> :
    			this.state.election_data.render()
    		}
	    	</div>);
	}
}