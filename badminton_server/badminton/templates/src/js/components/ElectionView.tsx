import * as React from "react";
import {Slider} from "./Slider";
import axios from 'axios';
import {HigherOrderComponent} from '../common/ComponentSubclasses';

const election_url = '/mock/election_happening.json';
const election_not_url = '/mock/electionless.json';

enum LoadingState {
    Loading,
    Loaded,
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
	constructor(name: string, candidates: any) {
		super();
		this.role = name;
		this.candidates = [];
		for (let i in candidates) {
			let candidate = candidates[i];
			const obj = new ElectionCandidate(candidate, this.role);
			this.candidates.push(obj);
		}
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

abstract class ElectionData extends HigherOrderComponent {
	constructor() {
		super();
	}

	abstract up(): boolean;
}

class ElectionUp extends ElectionData {
	order: string[];
	campaigns: ElectionRole[];

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
			this.campaigns.map((campaign: ElectionRole, idx: number) => { 
				return campaign.render() 
			})
		}<button type="submit">Submit Votes</button>
		</form>);
	}
}

class ElectionDown extends ElectionData {
	message: string;
	constructor(message: string) {
		super();
		this.message = message;
	}

	up() {
		return false;
	}

	render() {
		return (<p>{this.message}</p>);
	}
}

interface ElectionState {
	election: LoadingState;
	election_data?: ElectionData;
}

export class ElectionView extends React.Component<{}, ElectionState> {

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
				if (status) {
					pack = new ElectionUp(res.data);
				} else {
					pack = new ElectionDown(res.data.message);
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