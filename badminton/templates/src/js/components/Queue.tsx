import * as React from "react";
import axios from 'axios';

const queueUrl = '/api/queue/';

class PartyView extends React.Component<any, any> {
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
		return <div>
			<h2>{this.props.type}</h2>
			{
				this.props.parties.map((party: any, idx: number) => {
					return <PartyView party={party} idx={idx} />
				})
			}
		</div>
	}
}

export class Queue extends React.Component<any, any> {

	constructor(props: any) {
		super(props);
		this.state = {
			data: null,
		}
		this.refreshQueue = this.refreshQueue.bind(this);
	}

	async refreshQueue() {
		try {
			const queueData = await axios.get(queueUrl);
			this.setState({
				data: queueData.data,
			})
		} catch (err) {
			console.log(err);
		}
	}

	componentDidMount() {
		this.refreshQueue();
	}

	render() {
		if (this.state.data === null) {
			return <p>Loading</p>
		}
		return <div>
			{
				this.state.data.queues.map((queue: any, idx: number) => {
					return <SpecificQueueView parties={queue.parties} type={queue.type} key={idx} />
				})
			}
		</div>
	}
}