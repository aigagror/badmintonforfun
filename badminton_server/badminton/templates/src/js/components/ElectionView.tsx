import * as React from "react";
import {Slider} from "../common/Slider";
import axios from 'axios';
import { HigherOrderComponent } from '../common/ComponentSubclasses';

const election_url = '/mock/election_happening.json';
const election_not_url = '/mock/electionless.json';

enum LoadingState {
    Loading,
    Loaded,
}

class ElectionCandidate extends React.Component<any, any> {
	person: any;
	role: string;
	constructor(props: any) {
		super(props);
	}

	render() {
		return (<div>
			<p>Name: {this.props.person.name}</p>
			<p>Pitch: {this.props.person.pitch}</p>
			<input type="radio" name={this.props.role} value={this.props.person.id} defaultChecked={this.props.person.voted} />
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
			<h3>{this.props.role}</h3>
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
		}
		this.submitVotes = this.submitVotes.bind(this);
	}

	submitVotes(event: any) {
		event.preventDefault();
		for(let key in this.props.order) {
			let elem = this.props.order[key];
			console.log("For: " + elem + " Userid: " + event.target[elem].value);
		}
	}

	render() {
		return (<form onSubmit={this.submitVotes}>{
			this.state.campaigns.map((campaign: any, idx: number) => { 
				return <ElectionRole role={campaign[0]} candidates={campaign[1]} key={idx}/>
			})
		}<button type="submit">Submit Votes</button>
		</form>);
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
				if (status) {
					pack = <ElectionUp order={res.data.order} campaigns={res.data.campaigns} />;
					up = true;
				} else {
					pack = <ElectionDown message={res.data.message} />;
					up = false;
				}
				_this_ref.setState({
					election_data: pack,
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
	    return (<div className="election-view">
	    	<h2>Toggle datum</h2>
	    	<Slider change={this.switch} />
    		{
    			this.state.election === LoadingState.Loading ?
    			<p> Loading </p> :
    			this.state.election_data
    		}
	    	</div>);
	}
}