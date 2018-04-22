import * as React from "react";
import axios from 'axios';
import * as ReactTooltip from 'react-tooltip';
import {Select, Option} from '../common/Select';
import {objectToFormData} from '../common/Utils';
import { xsrfCookieName, xsrfHeaderName, getMemberId, isBoardMember } from '../common/LocalResourceResolver';
import { Popup } from '../common/Popup';
import { Slider } from '../common/Slider';
axios.defaults.xsrfCookieName = xsrfCookieName();
axios.defaults.xsrfHeaderName = xsrfHeaderName();

const queueUrl = '/api/queue/';
const matchUrl = '/api/match/current/';
const courtStatuses = '/api/courts/';
const freeMemberUrl = '/api/party/free_members/';
const partyGetUrl = '/api/party/get/';

function round(number: number, precision: number) {
  var shift = function (number: number, precision: number, reverseShift: boolean) {
    if (reverseShift) {
      precision = -precision;
    }  
    var numArray = ("" + number).split("e");
    return +(numArray[0] + "e" + (numArray[1] ? (+numArray[1] + precision) : precision));
  };
  return shift(Math.round(shift(number, precision, false)), precision, true);
}

class QueuedPartyView extends React.Component<any, any> {
	render() {
		return <div className="row">
		<div className='queue-party-div'>
			{
				this.props.party.members.map((member: any, idx: number) => {
					return <div key={idx}>
					<p>{member.first_name + ' ' + member.last_name}</p>
					</div>
				})
			}
			<h4>Average Playtime: {round(this.props.party.average_play_time, 2)} minutes</h4>
		</div>
		</div>
	}
}

class SpecificQueueView extends React.Component<any, any> {

	render() {
		return <div className="col-4">
			<h2>{this.props.type}</h2>
			{
				this.props.parties.map((party: any, idx: number) => {
					return <QueuedPartyView party={party} idx={idx} />
				})
			}
		</div>
	}
}

const getSelectedMemberIds = () => {
	const inputs = document.querySelectorAll('.queue-party-input');
	const out = [];
	for (let i = 0; i < inputs.length; ++i) {
		let input = inputs[i] as any;
		if (input.checked) {
			out.push(input.value)
		}
	}
	return out;
}

const getSelectedMemberObj = () => {
	const inputs = document.querySelectorAll('.queue-party-input');
	const out = [];
	for (let i = 0; i < inputs.length; ++i) {
		let input = inputs[i] as any;
		if (input.checked) {
			out.push({'id': input.value, 'name': input.name})
		}
	}
	return out;
}

class CourtView extends React.Component<any, any> {
	render() {
		const name = 'court'+this.props.court.id;
		const match = this.props.court.match;
		return <div className="col-6">
				<div className='row'>
				<div className="col-6">
				<h4>{this.props.court.queue_type === null ? "Free Play" : this.props.court.queue_type}</h4>
				</div> 
				{
					(this.props.court.queue_type === null && !this.props.hasParty) &&
					 (match !== null ? <div className="col-6">
					<button onClick={() => this.props.onJoin(match.match_id, match.teamA.length <= match.teamB.length ? 'A':'B')} 
					className='interaction-style'>Join Match</button>
					</div> : <div className="col-6">
					<button onClick={() => this.props.onYes(this.props.court.court_id)} className='interaction-style'>Start Match</button>
					</div>)
				}

				</div>
				{
					match !== null ?  <div className="court-style">
					{match.teamA.map((a : any, idx: number) => 
						<div className={"court-a-team team-"+(idx+1)+"-"+match.teamA.length}>{a}</div>)}
					{match.teamB.map((a : any, idx: number) => 
						<div className={"court-b-team team-"+(idx+1)+"-"+match.teamB.length}>{a}</div>)}
				</div>: 
					<div className="court-style" data-tip data-event='click focus' data-for={name}></div>
				}
				</div>
	}
}

class MyPartyView extends React.Component<any, any> {
	constructor(props: any) {
		super(props);
		this.state = {
			loaded: false
		}

		this.refreshParty = this.refreshParty.bind(this);
		this.createParty = this.createParty.bind(this);
		this.kickParty = this.kickParty.bind(this);
		this.leaveParty = this.leaveParty.bind(this);
		this.addMember = this.addMember.bind(this);
		this.refresh = this.refresh.bind(this);
	}

	refresh() {
		this.refreshParty();
		this.props.refresh();
	}

	async refreshParty() {
		try {
			const free = await axios.get(freeMemberUrl);
			this.setState({
				loaded:true,
				freeMembers: free.data,
				selectedQueue: this.props.queueTypes[0].value,
			})
		} catch (err) {
			console.log(err);
		}
	}

	async createParty() {
		const out = getSelectedMemberIds();
		const joined = out.join(',')
		const queue = this.state.selectedQueue;
		try {
			const data = await axios.post('/api/party/create', objectToFormData({queue_id: queue, member_ids: joined}));
			this.refresh();
		} catch (err) {
			console.log(err);
		}
	}

	async kickParty(member_id: any) {
		try {
			const res = await axios.post('/api/party/remove_member/', objectToFormData({member_id: member_id}));
			console.log(res);
			this.refresh();
		} catch(err) {
			console.log(err);
		}
	}

	async leaveParty() {
		try {
			const res = await axios.post('api/party/leave/');
			console.log(res);
			this.refresh();
		} catch (err) {
			console.log(err);
		}
	}


	addMember() {
		const out = getSelectedMemberIds();
		const requests = out.map((member_id: any) => {
			axios.post('/api/party/add_member/', objectToFormData({'member_id': member_id}));
		})
		axios.all(requests).then(() => {
			this.refresh();
		});
	}

	componentDidMount() {
		this.refreshParty()
	}

	render() {
		
		if (!this.state.loaded) {
			return <p>Loading</p>;
		} 
		const members = <div style={{height:'200px', overflowY:'scroll', overflowX:'hidden'}}> {
		this.state.freeMembers.map((member: any, idx: number) => {
					const member_ident = "member" + member.id;
					return <div className="row" key={idx}>
						<input type="checkbox" id={member_ident} value={member.id} name={member.first_name + ' ' + member.last_name} className="interaction-style queue-party-input"/>
	    				<label htmlFor={member_ident}>{member.first_name + ' ' + member.last_name}</label>
	    				</div>
				}) } </div>

		if (this.props.party) {
			return <div>
			<h4>Current Party</h4>
			{
				this.props.party.members.map((member: any, idx: number) => {
					return <div key={idx} className="row">
					<div className="col-6">
					<h4>{member.name}</h4>
					</div>
					<div className="col-6">
					<button onClick={() => this.kickParty(member.id)} className="interaction-style">Kick</button>
					</div>
					</div>
				})
			}
			<button className="interaction-style" onClick={this.leaveParty}>Leave</button>
			{
				members
			}
			<button className="interaction-style" onClick={this.addMember}>Add</button>
			</div>
		}

		return <div className="row">
			{
				members
			}
			<div className="row-offset-1">
			<div className="row">
			<div className="col-6">
			<Select
				options={this.props.queueTypes} 
				name="party_picker"
				defaultValue={this.state.selectedQueue}
				onChange={(val: any) => this.setState({selectedQueue: val})}
				/>
			</div>
			<div className="col-6">
			<button className="interaction-style" onClick={this.createParty} >Create Party</button>
			</div>
			</div>
			</div>
			</div>

	}
}

export class Queue extends React.Component<any, any> {

	constructor(props: any) {
		super(props);
		this.state = {
			memberState: null,
			queues: null,
		}
		this.refreshQueue = this.refreshQueue.bind(this);
		this.startMatch = this.startMatch.bind(this);
		this.finishMatch = this.finishMatch.bind(this);
		this.leaveMatch = this.leaveMatch.bind(this);
		this.joinMatch = this.joinMatch.bind(this);
	}

	async refreshQueue() {
		try {
			const res = await axios.get(matchUrl);
			if (res.data.status === 'idle') {
				const [queueData, courtData, isParty] = [await axios.get(queueUrl), 
					await axios.get(courtStatuses),
					await axios.get(partyGetUrl)];
				const queues = queueData.data.queues;
				const queueTypes = queues.map((queue: any) => new Option(queue.id, queue.type))
				this.setState({
					memberState: 'idle',
					queues: queueData.data.queues,
					queueTypes: queueTypes,
					courtData: courtData.data.courts,
					party: isParty.data.status === 'partyless' ? null : isParty.data,
				})
			} else {
				const match = await axios.get('/api/match/current/');
				const matchData = match.data.match;
				this.setState({
					memberState: 'playing',
					matchId: matchData.match_id,
					teamA: matchData.teamA,
					teamB: matchData.teamB,
					aScore: matchData.scoreA,
					bScore: matchData.scoreB,
				})
			}
		} catch (err) {
			console.log(err);
		}
	}

	componentDidMount() {
		this.refreshQueue();
	}

	startMatch(court_id: number) {
		const sel = getSelectedMemberObj();
		if (sel.length === 0) {
			this.setState({
				popup:  <Popup title="One Member" message="Please pick at least one member" callback={() => this.setState({popup: null})} />
			})
			return;
		}

		const callback = async (left: any, right: any) => {
			try {
				const res = await axios.post('/api/match/create/', JSON.stringify({
					court_id: court_id,
					score_A: 0, 
					score_B: 0, 
					a_players: left, 
					b_players: right,
				}));
				console.log(res.data);
				this.setState({
					popup: null
				})
				this.refreshQueue();
			} catch (err) {
				console.log(err);
			}
		}
		const left = sel.map((e: any) => e.id);
		const right: any[] = [];
		const deleteArr = (arr: any[], elem: any) => {
			const idx = arr.findIndex((i: any) => i === elem);
			if (idx != -1) {
				arr.splice(idx, 1);
			}
		}
		const onSwap = (id: any, event: any) => {
			if (event.target.checked) {
				deleteArr(left, id);
				right.push(id);
			} else {
				deleteArr(right, id);
				left.push(id);
			}
		}

		const popup = <Popup title="Pick Sides - One Per side" callback={() => callback(left, right)}>
			<div className="row">
				<div className="col-6">Me</div>
				<div className="col-6"><Slider change={(val: any) => onSwap(getMemberId(), val)}/></div>
			</div>
			{
				sel.map((person: any, idx: number) => {
					return <div className="row">
						<div className="col-6">{person.name}</div>
						<div className="col-6"><Slider change={(val: any) => onSwap(person.id, val)}/></div>
					</div>
				})
			}
		</Popup>
		this.setState({
				popup: popup
		})
	}

	async finishMatch() {
		try {
			const res = await axios.post('/api/match/finish/', objectToFormData({
				scoreA: this.state.aScore,
				scoreB: this.state.bScore,
			}));
			this.refreshQueue();
			console.log(res);
		} catch (err) {
			console.log(err);
		}
	}

	async leaveMatch() {
		try {
			const res = await axios.post('/api/match/leave/', objectToFormData({
				match_id: this.state.matchId,
			}));
			this.refreshQueue();
			console.log(res);
		} catch (err) {
			console.log(err);
		}
	}

	async joinMatch(match_id: any, team: any) {
		try {
			const res = await axios.post('/api/match/join/', objectToFormData({
				match_id: match_id,
				team: team,
			}));
			this.refreshQueue();
			console.log(res);
		} catch (err) {
			console.log(err);
		}
	}

	render() {
		if (this.state.memberState === null) {
			return <p>Loading</p>
		}
		else if (this.state.memberState === 'playing') {
			return <div className="col-12">
				{this.state.popup && this.state.popup}
				<h4>Team A: {this.state.teamA.map((a : any) => a.name).join(',') + " "}
				 vs Team B: {this.state.teamB.map((a : any) => a.name).join(',')} </h4>
				<div className="court-style">
					{this.state.teamA.map((a : any, idx: number) => 
						<div className={"court-a-team a-team-"+(idx+1)+"-"+this.state.teamA.length}>{a.name}</div>)}
					{this.state.teamB.map((a : any, idx: number) => 
						<div className={"court-b-team b-team-"+(idx+1)+"-"+this.state.teamB.length}>{a.name}</div>)}
				</div>
				<div className="col-5">
				<input value={this.state.aScore} className='interaction-style' onChange={(ev: any) => this.setState({aScore: ev.target.value})}></input> 
				</div>
				<div className="col-2">
				to
				</div>
				<div className="col-5">
				<input value={this.state.bScore} className='interaction-style' onChange={(ev: any) => this.setState({bScore: ev.target.value})}></input> 
				</div>

				<div className="row">
				<div className="col-6">
				<button className='interaction-style' onClick={this.finishMatch}>Finish Match</button>
				</div>
				<div className="col-6">
				<button className='interaction-style' onClick={this.leaveMatch}>Leave Match</button>
				</div>
				</div>
				</div>
		}

		return <div>
			<div className="row">
			{this.state.popup && this.state.popup}
			{
				this.state.courtData.map((court: any, idx: number) => {
					return <CourtView key={idx} court={court} hasParty={this.state.party!==null} 
						onYes={this.startMatch}
						onJoin={this.joinMatch} />
				})

			}
			</div>

			<MyPartyView 
				party={this.state.party} 
				queueTypes={this.state.queueTypes}
				refresh={this.refreshQueue} />
			
			<div className="row">
			{
				this.state.queues.map((queue: any, idx: number) => {
					return <SpecificQueueView parties={queue.parties} type={queue.type} key={idx} />
				})
			}
			</div>
		</div>
	}
}