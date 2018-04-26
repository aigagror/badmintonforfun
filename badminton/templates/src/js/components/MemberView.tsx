import * as React from 'react';
import axios from 'axios';

const url = '/api/members/all/';

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
				const sorted = res.data.members.sort((a: any, b: any) => {
					const cmp = a.first_name.localeCompare(b.first_name);
					if (cmp === 0) {
						return a.last_name.localeCompare(b.last_name);
					}
					return cmp;
				})
				this.setState({
					members: sorted
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
			return <ul className="member-list">
				{
					this.state.members.map((member: any, idx: any) => {
						return <li key={idx}><Member name={member.first_name + ' ' + member.last_name} 
							id={member.id} key={idx}/></li>
					})
				}
			</ul>
		}
	}
}