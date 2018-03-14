import * as React from "react";
import axios from 'axios';
import { Slider } from '../common/Slider'

const stat_urls = "/mock/stats.json"

class GameView extends React.Component<any, any> {
	render() {
		return (<tr className="row-2">
			<td className="col-3">{this.props.my_score}</td>
			<td className="col-3">{this.props.their_score}</td>
			</tr>)
	}
}

class StatView extends React.Component<any, any> {

	render() {
		return (<table className="stats-table">
			<thead className="row-3">
			<tr><th className="col-3">Your Score</th><th className="col-3">My Score</th></tr>
			</thead>
			<tbody>
			{this.props.stats.games.map ((game: any, idx: number) => {
				return <GameView key={idx} my_score={game.my_score} their_score={game.their_score} />
			}) }
			</tbody>
		</table>);
	}
}

class BoardView extends React.Component<any, any> {

	render() {
		return <p>BoardView</p>;
	}
}

export class HomeView extends React.Component<{}, any> {
	constructor(props: any) {
		super(props);
		this.state = {
			stats: null,
			board_member: false
		}
		this.performRequest = this.performRequest.bind(this)
	}

	componentDidMount() {
		this.performRequest(stat_urls);
	}

	performRequest(url: string) {
		axios.get(url)
			.then((res) => {
				this.setState({
					stats: res.data.stat_data,
					board_member: res.data.board_member
				});
			})
			.catch((res) => {

			})
	}

	render() {
		if (this.state.stats === null) {
			return null
		}
		return (<div className="election-view">
	    	<StatView stats={this.state.stats} />
	    	</div>);
	}
}