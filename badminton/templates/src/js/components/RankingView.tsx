import * as React from "react";
import axios from 'axios';
import {Slider} from '../common/Slider';
import { getMemberId } from '../common/LocalResourceResolver'

const ranking_url = '/api/rankings/winratio/';
const ranking_level = '/api/rankings/level/';

class RanksTableWL extends React.Component<any, any> {
	render() {
		return <div>
		<h4>{this.props.title}</h4>
		<table className="stats-table row-offset-1">
			<thead className="row-3">
			<tr>
				<th className="col-3 col-es-6">Rank</th>
				<th className="col-3 col-es-6">Name</th>
				<th className="col-3 col-es-6">Wins</th>
				<th className="col-3 col-es-6">Total</th>
			</tr>
			</thead>
			<tbody>
			{
				this.props.ranks.map((rank: any, idx: number) => {
					return (<tr key={idx} className={(getMemberId() === rank.id ? "my-rank " : "")+"row-2"}>
						<td className="col-3 col-es-6">{idx+1}</td>
						<td className="col-3 col-es-6">{rank.first_name} {rank.last_name}</td>
						<td className="col-3 col-es-6">{rank.wins}</td>
						<td className="col-3 col-es-6">{rank.total_games}</td>
						</tr>);
				})
			}
			</tbody>
		</table>
		</div>
	}
}

class RanksTableLevel extends React.Component<any, any> {
	render() {
		return <div>
		<h4>{this.props.title}</h4>
		<table className="stats-table row-offset-1">
			<thead className="row-3">
			<tr><th className="col-3 col-es-6">Rank</th>
				<th className="col-3 col-es-6">Name</th>
				<th className="col-3 col-es-6">Level</th>
			</tr>
			</thead>
			<tbody>
			{
				this.props.ranks.map((rank: any, idx: number) => {
					return (<tr key={idx} className={(getMemberId() === rank.id ? "my-rank " : "")+"row-2"}>
						<td className="col-3 col-es-6">{idx+1}</td>
						<td className="col-3 col-es-6">{rank.first_name} {rank.last_name}</td>
						<td className="col-3 col-es-6">{rank.level}</td>
						</tr>);
				})
			}
			</tbody>
		</table>
		</div>
	}
}

export class RankingView extends React.Component<any, any> {

	constructor(props: any) {
		super(props);

		this.state = {
			ranks: null,
			loading: true,
		}
	}

	componentDidMount() {
		this.performRequest();
	}

	async performRequest() {

		const regular = this.state.regular;
		var url = ranking_url;
		try {
			const [res, level] = [await axios.get(url), await axios.get(ranking_level)];
			this.setState({
				ranks: res.data.rankings,
				level: level.data.rankings,
				loading: false,
			})
		} catch (err) {
			console.log(err);
		}
	}

	render() {
		if (this.state.loading === true) {
			return <p>Loading</p>
		}
		console.log(this.state.ranks)
		console.log(this.state.level)

		return <>
		<RanksTableWL ranks={this.state.ranks} myRank={this.state.myRanks} title="Rankings by Win/Loss"/>
		<RanksTableLevel ranks={this.state.level} myRank={this.state.myRanks} title="Rankings by Level"/>
		</>
	}

}