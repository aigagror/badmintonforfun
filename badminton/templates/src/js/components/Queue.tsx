import * as React from "react";
import axios from 'axios';
import * as ReactTooltip from 'react-tooltip';

const queueUrl = '/api/queue/';
const matchUrl = '/api/match/get/';
const courtStatuses = '/api/courts/';
const freeMemberUrl = '/api/party/free_members/';

const partyGetUrl = '/api/party/get/';

class QueuedPartyView extends React.Component<any, any> {
	render() {
		return <div>
			<h3>Party</h3>
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
	}

	async refreshParty() {
		try {
			const free = await axios.get(freeMemberUrl);
			this.setState({
				loaded:true,
				freeMembers: free.data,
			})
		} catch (err) {
			console.log(err);
		}
	}
	componentDidMount() {
		this.refreshParty()
	}

	render() {
		if (this.props.party) {
			return <p>In a Party</p>
		} else if (!this.state.loaded) {
			return <p>Loading</p>;
		}

		return <div className="row">
			<div style={{height:'200px', overflowY:'scroll', overflowX:'hidden'}}>
			{
				this.state.freeMembers.map((member: any, idx: number) => {
					const member_ident = "member" + member.id;
					return <div className="row" key={idx}>
						<input type="checkbox" id={member_ident} className="interaction-style"/>
	    				<label htmlFor={member_ident}>{member.first_name + ' ' + member.last_name}</label>
	    				</div>
				})
			}
			</div>
			<button className="interaction-style">Create Party</button>
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
				this.setState({
					memberState: 'idle',
					queues: queueData.data.queues,
					courtData: courtData.data.courts,
					party: isParty.data.status === 'partyless' ? null : isParty,
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

			<MyPartyView party={this.state.party} />
			
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