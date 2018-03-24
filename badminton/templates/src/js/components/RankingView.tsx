import * as React from "react";
import axios from 'axios';
import {Slider} from '../common/Slider';

const ranking_url = '/mock/ranking.json';
const ranking_not_up = '/mock/ranking_not_up.json';

class RanksTable extends React.Component<any, any> {
	render() {
		return <div>
			{
				this.props.ranks.map((rank: any, idx: number) => {
					return <div>
					{rank.name}, {rank.rank}
					</div>
				})
			}
		</div>
	}
}

export class RankingView extends React.Component<any, any> {

	constructor(props: any) {
		super(props);
		this.switch = this.switch.bind(this);

		this.state = {
			ranks: null,
			myRank: null,
			loading: true,
			regular: true,
		}
	}

	componentDidMount() {
		this.performRequest();
	}

	performRequest() {

		const regular = this.state.regular;
		var url = ranking_url;
		if (this.state.regular) {
			url = ranking_not_up
			
		}

		axios.get(url)
			.then((res) => {
				this.setState({
					ranks: res.data.ranking,
					myRank: res.data.my_rank,
					loading: false,
					regular: !regular
				})
			})
			.catch((res) => {

			})
	}

	switch(event: Event) {
		if (this.state.loading === true) {
			return;
		} else {
			this.performRequest();
		}
	}

	render() {
		if (this.state.loading === true) {
			return <p>Loading</p>
		}

		return <div>
			<Slider change={this.switch} />
			<RanksTable ranks={this.state.ranks} myRank={this.state.myRanks}/>
		</div>
	}

}