import * as React from "react";
import axios from 'axios';
import { Slider } from '../common/Slider'
import { ProfileView } from './ProfileView'
import { Select } from '../common/Select'
import { isBoardMember, xsrfCookieName, xsrfHeaderName, getMemberId } from '../common/LocalResourceResolver'
import { EditableTextarea } from '../common/EditableTextarea';
import { objectToFormData } from '../common/Utils';
import DatePicker from 'react-datepicker';

axios.defaults.xsrfCookieName = xsrfCookieName();
axios.defaults.xsrfHeaderName = xsrfHeaderName();

declare var require: Function;
const moment = require('moment');
const BigCalendar = require('react-big-calendar');
BigCalendar.momentLocalizer(moment); // or globalizeLocalizer

const stat_urls = "/api/match/all_matches_from_member/"
const announce_url = "/api/announcements/get/";
const announce_create_url = "/api/announcements/create/";
const announce_edit_url = "/api/announcements/edit/";
const announce_delete_url = "/api/announcements/delete/";

class GameView extends React.Component<any, any> {
	render() {
		return (<tr className="row-2">
			<td className="col-3 col-es-6">{this.props.myScore}</td>
			<td className="col-3 col-es-6">{this.props.theirScore}</td>
			<td className="col-3 col-es-6">{this.props.playtime}</td>
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
			<tr>
			<th className="col-3 col-es-6">Your Score</th>
			<th className="col-3 col-es-6">My Score</th>
			<th className="col-3 col-es-6">Play Time</th>
			</tr>
			</thead>
			<tbody>
			{this.props.stats.map ((game: any, idx: number) => {
				let playTime = "ongoing";
				const match = game.match;
				if (match.endDateTime !== null) {
					const start = (new Date(match.startDateTime)).getTime();
					const end = (new Date(match.endDateTime)).getTime();
					const diff = (end - start) / 1000;
					playTime = Math.floor((diff / 60)) + ":" + (diff % 60);
				}
				const isTeamA = game.team_A.find((e: any) => e.id === getMemberId()) !== undefined;
				let my_score = match.scoreB, their_score = match.scoreA;
				if (isTeamA) {
					my_score = match.scoreA;
					their_score = match.scoreB;
				}
				return <GameView key={idx} myScore={my_score} theirScore={their_score} playtime={playTime}/>
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

		this.state = {
			boardMember: isBoardMember(),
		}

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
		const params = {
			title: this.state.titleText,
			entry: this.state.annoucementText,
		}
		axios.post(announce_create_url, objectToFormData(params))
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
		if (!this.state.boardMember) {
			return null;
		}

		if (this.state.showCreator) {
			return <div className="row-offset-1">
				<h4>Send Anouncement</h4>
				<form onSubmit={this.sendAnnouncement}>

				<div className="row">
				<h4>Members only! Add a practice</h4>
				<div className="col-8">
				<input className="interaction-style" 
					placeholder="Title" 
					type="text" 
					onChange={(ev: any) => {
						this.setState({titleText:ev.target.value})
					}} 
					value={this.state.titleText} />
				</div>
				</div>

				<div className="row">
				<div className="col-12">
				<textarea placeholder="Body" className="row-offset-1 interaction-style" onChange={(ev: any) => 
					this.setState({announcementText: ev.target.value})}
					value={this.state.announcementText}>
				</textarea>
				</div>
				</div>

				<div className="row row-offset-1">
				<div className="col-6">
				<button type="submit" className="interaction-style">
					Submit
				</button>
				</div>
				<div className="col-6">
				<button onClick={() => this.setState({showCreator: false})} className="interaction-style">
					Close
				</button>
				</div>
				</div>
				</form>
			</div>
		} else {
			return <button onClick={() => this.setState({showCreator: true})} className="interaction-style">
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
			boardMember: isBoardMember(),
		}

		this.performRequest = this.performRequest.bind(this);
		this.performUpdate = this.performUpdate.bind(this);
		this.deleteAnnouncement = this.deleteAnnouncement.bind(this);
	}

	async performRequest() {
		try {
			const res = await axios.get(announce_url);
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
				this.setState({
					announcements: announcements,
				})
			}
		} catch (err) {
			console.log(err);
		}
	}

	componentDidMount() {
		this.performRequest();
	}

	performUpdate(idx: number) {
		return async (text:string) => {
					const announce = this.state.announcements[idx];
					const data = new FormData();
					data.append('title', announce.title);
					data.append('entry', text);
					data.append('id', announce.id);
					try {
						await axios.post(announce_edit_url, data);
						this.performRequest();
					} catch (res) {
						console.log(res);
					}
				}
	}

	deleteAnnouncement(idx: number) {
		return async () => {
			try {
				await axios.post(announce_delete_url,
			         objectToFormData({id: idx}));
			    this.performRequest();
			} catch (err) {
				console.log(err);
			}
		}
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
						<EditableTextarea 
							initValue={announce.entry}
							onSave={this.performUpdate(idx)}
							onDelete={this.deleteAnnouncement(announce.id)}
							editableOverride={!this.state.boardMember} />
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
			board_member: false,
			sched: [],
			addDate: moment(),
			numCourts: "",
		}
		this.performRequest = this.performRequest.bind(this)
		this.sendSchedule = this.sendSchedule.bind(this);
	}

	componentDidMount() {
		this.performRequest(stat_urls);
	}

	performRequest(url: string) {
		const req1 = axios.get(url + "?id=" + getMemberId())
		const req2 = axios.get('/api/settings/schedule/get')
		axios.all([req1, req2]).then(axios.spread((res: any, res2: any) => {
			const events = res2.data.schedule.map((ev: any) => {
				    return {
				    	'title': ev.number_of_courts + ' courts',
	    				'allDay': true,
					    start: moment(ev.date),
					    end: moment(ev.date),
					}
				})
			this.setState({
				stats: res.data,
				sched: events,
				board_member: res.data.board_member
			})
		})).catch((res: any) => {
			console.log(res);
		})

	}

	async sendSchedule(ev: any) {
		const dateFormat = "YYYY-MM-DD";
		try {
			const body = {
				schedule: {
					date: this.state.addDate.format(dateFormat), 
					number_of_courts: this.state.numCourts
				}
			}
			const data = await axios.post('/api/settings/schedule/edit', {
				schedule: [{
					date: this.state.addDate.format(dateFormat), 
					number_of_courts: this.state.numCourts
				}]
			})
			this.setState({
				date: moment(),
				number_of_courts: "",
			})
			this.performRequest(stat_urls);
		} catch (err) {
			console.log(err);
		}
	}

	render() {
		if (this.state.stats === null) {
			return null
		}
		/*<div className="row-offset-2">
		<BigCalendar
		      events={this.state.sched}
		      views={["month"]}
			  step={60}
			  showMultiDayTimes
			  startAccessor="start"
      		  endAccessor="end"
		    />
		    {isBoardMember() &&
		    <div className="row row-offset-1">
		    <div className="col-4">
		    <DatePicker
		        selected={this.state.addDate}
		        onChange={(date: any) => this.setState({addDate:date})}
		        className="interaction-style"
		    />
		    <div className="col-4">
		    <input 
		    	className="interaction-style" 
		    	value={this.state.numCourts}
		    	onChange={(ev: any) => this.setState({numCourts:ev.target.value})} 
		    	placeholder="Num Courts"/>
		    </div>

		    <div className="col-4">
		    <button 
		    	type="submit" 
		    	className="interaction-style" 
		    	onClick={this.sendSchedule} 
		    	>Submit</button>
		    </div>
		    </div>
		    </div>}*/

		return (<div className="home-view">
			<AnnounceView stats={this.state.stats} />

			<div className="row-offset-2">
	    	<StatView stats={this.state.stats} />
	    	</div>

	    	<div className="row-offset-2">
	    	<h2>Profile</h2>
	    	<ProfileView member_id={getMemberId()} />
	    	</div>
	    	</div>);
	}
}