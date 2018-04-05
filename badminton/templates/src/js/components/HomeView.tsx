import * as React from "react";
import axios from 'axios';
import { Slider } from '../common/Slider'
import { ProfileView } from './ProfileView'
import { Select } from '../common/Select'
import { isBoardMember } from '../common/LocalResourceResolver'
import { EditableTextarea } from '../common/EditableTextarea';

declare var require: Function;

const DjangoCSRFToken: any = require('django-react-csrftoken').default;

console.log(DjangoCSRFToken);

const stat_urls = "/mock/stats.json"
const announce_url = "/api/announcements/get/";
const announce_create_url = "/api/announcements/create/";

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";

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
		this.initState = this.initState.bind(this);
		this.state = this.initState();

		this.sendAnnouncement = this.sendAnnouncement.bind(this);
	}

	initState() {
		return JSON.parse(JSON.stringify({
			showCreator: false,
			announcementText: "",
			titleText: "",
		}))
	}

	sendAnnouncement(ev: any) {
		var params = new FormData();
		params.append('title', this.state.titleText);
		params.append('entry', this.state.titleText);
		axios.post(announce_create_url, params)
		.then((res: any) => {
			this.setState(this.initState());
			this.props.refresh();
		})
		.catch((res: any) => {
			console.log(res);
		})
		ev.preventDefault()
	}

	render() {
		if (!isBoardMember()) {
			return null;
		}

		if (this.state.showCreator) {
			return <div className="row-offset-1">

				<form onSubmit={this.sendAnnouncement}>

				<input placeholder="Title" type="text" onChange={(ev: any) => {
					this.setState({titleText:ev.target.value})
				}} value={this.state.titleText} />

				<textarea placeholder="Body" className="row-offset-1" onChange={(ev: any) => 
					this.setState({announcementText: ev.target.value})}
					value={this.state.announcementText}>

				</textarea>
				<div className="row">
				<button type="submit" className="">
					Submit
				</button>
				<button onClick={() => this.setState({showCreator: false})} className="">
					Close
				</button>
				</div>
				</form>
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
			announcements: null,
		}

		this.performRequest = this.performRequest.bind(this);
	}

	performRequest() {
		axios.get(announce_url)
			.then((res) => {
				const announcements = res.data.announcements;
				if (announcements.length === 0) {
					const fake = [{
						title: "No Announcements!",
						body: "More to come...",
					}]
					this.setState({
						announcements: fake,
					})
				} else {
					const announce = announcements[0];
					console.log(announce);
					this.setState({
						announcements: announcements,
					})
				}
			})
			.catch((res) => {
				console.log(res);
			})
	}

	componentDidMount() {
		this.performRequest();
	}

	render() {
		if (this.state.announcements === null) {
			return <p>Loading Announcement</p>
		}
		return (
			<div className="announcement">
			<h2>Recent Announcements</h2>
			{
				this.state.announcements.map((announce: any, idx: number) => {
					return <div key={idx}>
						<h3>{announce.title}</h3>
						<EditableTextarea initValue={announce.entry} />
					</div>
				})
			}

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