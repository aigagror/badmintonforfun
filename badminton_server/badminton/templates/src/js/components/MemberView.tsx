import * as React from 'react';
import axios from 'axios';

const url = '/mock/members.json'

class Member extends React.Component<any, any> {
	render() {
		return <a href={"/profile.html?member_id=" + this.props.id}>{this.props.name}</a>
	}
}

export class MemberView extends React.Component<any, any> {

	constructor(props: any) {
		super(props);
		this.state = {
			members: []
		}
	}

	componentDidMount() {
		axios.get(url)
			.then((res) => {
				this.setState({
					members: res.data.members
				});
			})
			.catch((res) => {
				console.log(res);
			});
	}

	render() {
		if (this.state.members.length === 0) {
			return <p>Loading</p>
		} else {
			return <ul>
				{
					this.state.members.map((member: any, idx: any) => {
						return <li key={idx}><Member name={member.name} id={member.id} key={idx}/></li>
					})
				}
			</ul>
		}
	}
}