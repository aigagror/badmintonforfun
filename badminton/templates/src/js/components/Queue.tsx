import * as React from "react";
import axios from 'axios';
import * as ReactTooltip from 'react-tooltip';
import {Select, Option} from '../common/Select';
import {objectToFormData} from '../common/Utils';
import { xsrfCookieName, xsrfHeaderName, getMemberId, isBoardMember } from '../common/LocalResourceResolver';
axios.defaults.xsrfCookieName = xsrfCookieName();
axios.defaults.xsrfHeaderName = xsrfHeaderName();

const queueUrl = '/api/queue/';
const matchUrl = '/api/match/get/';
const courtStatuses = '/api/courts/';
const freeMemberUrl = '/api/party/free_members/';

const partyGetUrl = '/api/party/get/';

class QueuedPartyView extends React.Component<any, any> {
	render() {
		return <div className='queue-party-div'>
			{
				this.props.party.members.map((member: any, idx: number) => {
					return <div key={idx}>
					<p>{member.first_name + ' ' + member.last_name}</p>
					</div>
				})
			}
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

class CourtView extends React.Component<any, any> {
	render() {
		const name = 'court'+this.props.court.id;
		return <div className="col-6">
				<h4>{this.props.court.queue_type}</h4>
				<div className="court-style" data-tip data-event='click focus' data-for={name}></div>
				<ReactTooltip globalEventOff='click' id={name} aria-haspopup='true' >
				<h4>Start Match?</h4>
				<button>Yes</button>
				<button>No</button>
				</ ReactTooltip>
				</div>;
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

	getSelectedMemberIds() {
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

	async createParty() {
		const out = this.getSelectedMemberIds();
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
		const out = this.getSelectedMemberIds();
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
						<input type="checkbox" id={member_ident} value={member.id} className="interaction-style queue-party-input"/>
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
			<Select
				options={this.props.queueTypes} 
				name="party_picker"
				defaultValue={this.state.selectedQueue}
				onChange={(val: any) => this.setState({selectedQueue: val})}
				/>
			</div>
			<button className="interaction-style" onClick={this.createParty} >Create Party</button>
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
				console.log("You are in a game!");
			}
		} catch (err) {
			console.log(err);
		}
	}

	componentDidMount() {
		this.refreshQueue();
	}

	render() {
		if (this.state.memberState === null) {
			return <p>Loading</p>
		}
		else if (this.state.memberState === 'playing') {
			return <p>Playing</p>
		}

		return <div>
			<div className="row">
			{
				this.state.courtData.map((court: any, idx: number) => {
					return <CourtView key={idx} court={court}/>
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