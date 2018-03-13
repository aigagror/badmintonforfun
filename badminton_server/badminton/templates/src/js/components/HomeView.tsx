import * as React from "react";
import axios from 'axios';
import { Slider } from '../common/Slider'
const stat_urls = "/mock/stats.json"
const member_url = "/mock/home_member.json"

class StatView extends React.Component<any, any> {

	render() {
		return (<div className="stats">
			{this.props.stats.games.map ((game: any) => {
				return <div><div>Your Score: {game.my_score}</div>
				<div>Their Score: {game.their_score}</div></div>;
			}) }
		</div>);
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
		this.switch = this.switch.bind(this)
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

	switch() {
		if (this.state.board_member) {
			this.performRequest(stat_urls);
		} else {
			this.performRequest(member_url);
		}
	}

	render() {
		return (<div className="election-view">
	    	<h2>Toggle datum</h2>
	    	<Slider change={this.switch} />
	    	{
	    		this.state.stats !== null && <StatView stats={this.state.stats} />
	    	}
	    	{
	    		this.state.board_member && <BoardView />
	    	}
	    	</div>);
	}
}