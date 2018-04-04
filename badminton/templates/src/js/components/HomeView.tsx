import * as React from "react";
import axios from 'axios';
import { Slider } from '../common/Slider'
import { ProfileView } from './ProfileView'
import { Select } from '../common/Select'
import { isBoardMember } from '../common/LocalResourceResolver'
import { EditableTextarea } from '../common/EditableTextarea';

const stat_urls = "/mock/stats.json"
const announce_url = "/api/announcements/get/"

class GameView extends React.Component<any, any> {
	render() {
		return (<tr className="row-2">
			<td className="col-3 col-es-6">{this.props.my_score}</td>
			<td className="col-3 col-es-6">{this.props.their_score}</td>
			</tr>)
	}
}

class StatView extends React.Component<any, any> {

	render() {
		return (
		<div>
		<h2>Most Recent Games</h2>
		<table className="stats-table">
			<thead className="row-3">
			<tr><th className="col-3 col-es-6">Your Score</th><th className="col-3 col-es-6">My Score</th></tr>
			</thead>
			<tbody>
			{this.props.stats.games.map ((game: any, idx: number) => {
				return <GameView key={idx} my_score={game.my_score} their_score={game.their_score} />
			}) }
			</tbody>
		</table>
		</div>);
	}
}

class AnnounceCreator extends React.Component<any, any> {
	constructor(props: any) {
		super(props);

		this.state = {
			showCreator: false,
			announcementText: "",
		}

		this.sendAnnouncement = this.sendAnnouncement.bind(this);
	}

	sendAnnouncement() {
		this.props.refresh();
		this.setState({
			showCreator: false
		});
	}

	render() {
		if (!isBoardMember()) {
			return null;
		}

		if (this.state.showCreator) {
			return <div>
				<textarea onChange={(ev: any) => 
					this.setState({announcementText: ev.target.value})}
					value={this.state.announcementText}>

				</textarea>
				<button onClick={this.sendAnnouncement}>
					Submit
				</button>
				<button onClick={() => this.setState({showCreator: false})}>
					Close
				</button>
			</div>
		} else {
			return <button onClick={() => this.setState({showCreator: true})}>
						Add an announcement
					</button>
		}
	}
}

class AnnounceView extends React.Component<any, any> {

	constructor(props: any) {
		super(props);
		this.state = {
			title: null,
			body: null,
			showCreateAnnouncement: false,
		}

		this.performRequest = this.performRequest.bind(this);
	}

	performRequest() {
		axios.get(announce_url)
			.then((res) => {
				const announcements = res.data.announcements;
				if (announcements.length === 0) {
					this.setState({
						title: "No Announcements!",
						body: "More to come...",
					})
				} else {
					const announce = announcements[0];
					this.setState({
						title: res.data.title,
						body: res.data.body,
					})
				}
			})
			.catch((res) => {

			})
	}

	componentDidMount() {
		this.performRequest();
	}

	render() {
		if (this.state.title === null) {
			return <p>Loading Announcement</p>
		}
		return (
			<div className="announcement">
			<h2>Most Recent Announcment</h2>
			<h3>{this.state.title}</h3>
			<EditableTextarea initValue={this.state.body} />

			<AnnounceCreator refresh={this.performRequest}/>
			
			</div>
			);
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

		return (<div className="home-view">
			<AnnounceView stats={this.state.stats} />
			<div className="row-offset-2">
	    	<StatView stats={this.state.stats} />
	    	</div>
	    	<div className="row-offset-2">
	    	<h2>Profile</h2>
	    	<ProfileView member_id={1} />
	    	</div>
	    	</div>);
	}
}