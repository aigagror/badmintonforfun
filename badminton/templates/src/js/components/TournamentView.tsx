import * as React from "react";
import axios from 'axios';

const tourney_url = '/mock/tournament.json';

class TournamentCell extends React.Component<any, any> {

	render(): any {
		const matches = this.props.matches;
		var render;
		if (matches.state === "undecided") {
			render = (<div className="tournament-card">
					<h4>{matches.title}</h4>
					<p>TBA</p>
					</div>);
		} else if (matches.state === "decided") {
			render = (<div className="tournament-card">
					<h4>{matches.title}</h4>
					<h5>{matches.team1}</h5>
					<h5>{matches.team2}</h5>
					</div>);
		} else {
			render = (<div className="tournament-card">
					<h4>{matches.title}</h4>
					<h5>{matches.team1} Score: {matches.team1_score}</h5>
					<h5>{matches.team2} Score: {matches.team2_score}</h5>
					</div>);
		}
		
		return <div className="grid">
			<div className="row">
				{render}
			</div>

			<div className="row">
			<div className="col-6 tournament-row">
			{matches.feeder_lhs !== null && 
				<TournamentCell matches={matches.feeder_lhs} />}
			</div>
			<div className="col-6 tournament-row">
			{matches.feeder_rhs !== null && 
				<TournamentCell matches={matches.feeder_rhs} />}
			</div>
			</div>
		</div>
	}
}

export class TournamentView extends React.Component<any, any> {

	constructor(props: any) {
		super(props);
		this.state = {
			matches: null,
		}
	}

	componentDidMount() {
		axios.get(tourney_url)
			.then((res) => {
				this.setState({
					matches: res.data.matches,
				})
			})
			.catch((res) => {

			})
	}
	render() {
		if (this.state.matches === null) {
			return null;
		}

		return (<TournamentCell matches={this.state.matches} />);
	}
}