import * as React from "react";
import axios from 'axios';
import {Slider} from '../common/Slider';
import { getMemberId } from '../common/LocalResourceResolver'

const ranking_url = '/api/members/top_players';

class RanksTable extends React.Component<any, any> {
	render() {
		return <table className="stats-table row-offset-1">
			<thead className="row-3">
			<tr><th className="col-3 col-es-6">Rank</th>
				<th className="col-3 col-es-6">Name</th></tr>
			</thead>
			<tbody>
			{
				this.props.ranks.map((rank: any, idx: number) => {
					return (<tr key={idx} className={(getMemberId() === rank.id ? "my-rank " : "")+"row-2"}>
						<td className="col-3 col-es-6">{idx+1}</td>
						<td className="col-3 col-es-6">{rank.first_name} {rank.last_name}</td>
						</tr>);
				})
			}
			</tbody>
		</table>
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

	performRequest() {

		const regular = this.state.regular;
		var url = ranking_url;

		axios.get(url)
			.then((res) => {
				this.setState({
					ranks: res.data,
					loading: false,
				})
			})
			.catch((res) => {

			})
	}

	render() {
		if (this.state.loading === true) {
			return <p>Loading</p>
		}

		return <RanksTable ranks={this.state.ranks} myRank={this.state.myRanks}/>
	}

}