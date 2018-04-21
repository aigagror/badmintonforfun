import * as React from "react";
import axios from 'axios';
import {Select, Option} from '../common/Select';
import {objectToFormData} from '../common/Utils';
import {Popup} from '../common/Popup';
import { xsrfCookieName, xsrfHeaderName, getMemberId, isBoardMember } from '../common/LocalResourceResolver';
import {Slider} from '../common/Slider';
import {RadioButton} from '../common/RadioButton';
axios.defaults.xsrfCookieName = xsrfCookieName();
axios.defaults.xsrfHeaderName = xsrfHeaderName();
//axios.post('/api/tournament/members/register', objectToFormData({member_id: 2})).catch((err: any) => console.log(err));
const tourney_url = '/api/tournament/';

const columnWidth = 160;
const rowHeight = 40;
const rowSpacing = 10;
const colSpacing = 50;
const lazyHack =10000000;
const svgOffset = 20;
const calcX = (col: number) => (columnWidth+colSpacing)*col + svgOffset;
const calcY = (col: number, row: number, maxCols: number): number => {
	if(col === 0) {
		return (rowHeight+rowSpacing)*row + col * ((rowHeight+rowSpacing)/2) + svgOffset;
	}

	const numBlocksCenter = Math.pow(2, col);
	const ytop = calcY(0, row*numBlocksCenter, maxCols);
	const ybot = calcY(0, (row+1)*numBlocksCenter-1, maxCols) + rowHeight;

	return (ytop + ybot - rowHeight) / 2;
}

class Matchup extends React.Component<any, any> {

	unpackMatch(matches: any) {
		const match = matches[0];
		const decide = (team: any) => {
			if (team.length == 2) {
				return team[0].first_name + ' & ' + team[1].first_name;
			} else if (team.length == 1) {
				return team[0].first_name + ' ' + team[0].last_name;
			} else {
				return 'None';
			}
		}
		const team1 = decide(match.team_A);
		const team2 = decide(match.team_B);
		return [match, team1, team2]
	}
	render() {
		var extra;
		const startingX = this.props.x;
		const startingY = this.props.y+15;
		const textStyle = {
			fill: 'white',
			stroke: 'white',
			strokeWidth: 1.5,
		}
		if (this.props.data.matches.length === 0) {
			extra = <text x={startingX} y={startingY} height={rowHeight} width={columnWidth}>
				TBA
				</text>
		}
		else if (this.props.data.endDateTime === null) {
			const [match, team1, team2] = this.unpackMatch(this.props.data.matches);
			extra = <>
				<text x={startingX} y={startingY} style={textStyle}>
				{team1}
				</text>
				<text x={startingX} y={startingY+rowHeight/2} style={textStyle}>
				{team2}
				</text>
				</>
		} else {
			const [match, team1, team2] = this.unpackMatch(this.props.data.matches);
			const convert = (num: number): string => {
				if (num < 10) {
					return "0" + num;
				}

				return "" + num;
			}
			extra = <>
				<text x={startingX} y={startingY} style={textStyle}>
				{team1}
				</text>
				<text x={startingX} y={startingY+rowHeight/2} style={textStyle}>
				{team2}
				</text>
				<text x={startingX+columnWidth-25} y={startingY} style={textStyle}>
				{this.props.data.team1_score}
				</text>
				<text x={startingX+columnWidth-25} y={startingY+rowHeight/2} style={textStyle}>
				{this.props.data.team2_score}
				</text>
				</>
		}
		const rectStyle = {
			fill: 'black',
			stroke: 'black',
			strokeWidth: 5,
		}
		return (
			<>
		  <rect
			x={this.props.x}
			y={this.props.y}
			width={columnWidth}
			height={rowHeight}
			style={rectStyle}
			className="tournament-bracket-node"
			rx={""+3}
			ry={""+3}
			onClick={()=>this.props.change(this.props.data)}
		  />
		  {extra}
		  </>
		);
	}
}

function height(matchups: any): number {
	if (matchups === null || Object.keys(matchups).length === 0) {
		return 0;
	}

	let hgt = Math.max(height(matchups.left_node), 
		height(matchups.right_node)) + 1;
	return hgt;
}

class TournamentCell extends React.Component<any, any> {

	constructor(props: any) {
		super(props);

		this.agglomerateData = this.agglomerateData.bind(this);
		this._merge = this._merge.bind(this);
	}

	_merge(aggCall: any, toX: number, toY: number) {
		if (aggCall.length === 0) {
			return [];
		}
		let [othElems, [othX, othY]] = aggCall;
		const offsetX = 6;
		const midX = othX + columnWidth+offsetX;
		var midY = othY + rowHeight / 2;

		const halfX = midX + colSpacing / 2;
		const offsetY = 9;
		if (toY < midY) {
			toY += offsetY;
		} else {
			toY -= offsetY;
		}
		const lineOpts = {
			stroke: "black",
			strokeWidth: 1.5,
		}
		return [<line {...lineOpts} x1={""+midX} y1={""+midY} x2={""+halfX} y2={""+midY} />, 
			<line {...lineOpts} x1={""+halfX} y1={""+midY} x2={""+halfX} y2={""+toY} />,
			<line {...lineOpts} x1={""+halfX} y1={""+toY} x2={""+(toX-offsetX)} y2={""+toY} />,
			...othElems]
	}



	agglomerateData(data: any, row: number, col: number, maxCols: number): any {
		//elements, root
		if (data === null || Object.keys(data).length === 0) {
			return [];
		}
		let {left_node, right_node, ...rest} = data;
		const x = calcX(col);
		const y = calcY(col, row, maxCols);
		var elems = [<Matchup x={x} y={y} data={rest} change={this.props.change}/>];
		const entry = y + rowHeight / 2;

		if (data.left_node !== null) {
			const accumulated = this._merge(this.agglomerateData(data.left_node, row*2, col-1, maxCols), x, entry);
			elems = elems.concat(accumulated);
		}
		if (data.right_node !== null) {
			const accumulated = this._merge(this.agglomerateData(data.right_node, row*2+1, col-1, maxCols), x, entry);
			elems = elems.concat(accumulated);
		}
		return [elems, [x, y]];
	}


	render() {
		console.log(this.props.matches);
		const maxHeight = height(this.props.matches);
		let [elems, ...rest] = this.agglomerateData(this.props.matches, 0, maxHeight-1, maxHeight);
		return <svg width={""+window.innerWidth} height={""+window.innerHeight}>
				<g>
					{
						elems
					}
				</g>
			  </svg>
	}
}

class TournamentDown extends React.Component<any, any> {
	constructor(props: any) {
		super(props);

		this.state = {
			players: "",
			type: 'Doubles'
		}
		this.onSubmit = this.onSubmit.bind(this);
	}

	onSubmit(ev: any) {
		const data = {
			num_players: this.state.players,
			tournament_type: this.state.type,
		}
		axios.post('/api/tournament/create', objectToFormData(data))
			.then((res: any) => {
				console.log(res);
			})
			.catch((res: any) => {
				console.log(res);
			})
		ev.preventDefault();
	}

	render() {
		const opts = [
			new Option('Doubles', 'Doubles'),
			new Option('Singles', 'Singles'),
		]
		return <form onSubmit={this.onSubmit}>
		<div className="row">
		<div className="col-6">
		<input 
			type="text" 
			className="interaction-style" 
			placeholder="Number of players"
			value={this.state.players}
			onChange={(ev:any) => this.setState({players:ev.target.value})}>
			</input>
		</div>
		<div className="col-6">
		<Select 
			onChange={(val: any) => this.setState({type:val})} 
			options={opts} name="emailName" defaultValue={this.state.type}/>
		</div>
		</div>
		<button type="submit" className="interaction-style">Submit</button>
		</form>
	}
}

const convertToDicts = (matches: any) => {
	const _convertToDicts = (matches: any, idx: number): any => {
		if (idx > matches.length) {
			return null;
		}
		const lhs = _convertToDicts(matches, idx*2);
		const rhs = _convertToDicts(matches, idx*2+1);
		const node = matches[idx-1];
		return {left_node: lhs, right_node: rhs, id: node.bracket_node_id, matches: node.matches}
	}
	return _convertToDicts(matches, 1);
}

export class TournamentView extends React.Component<any, any> {

	constructor(props: any) {
		super(props);
		this.state = {
			status: null,
			matches: null,
		}
		this.refresh = this.refresh.bind(this);
		this.finishTournament = this.finishTournament.bind(this);
		this.changeMatch = this.changeMatch.bind(this);
		this.joinTournament = this.joinTournament.bind(this);
		this.leaveTournament = this.leaveTournament.bind(this);
	}

	async finishTournament() {
		try {
			const data = {
				tournament_id: this.state.id,
			}
			const res = await axios.post(tourney_url + 'finish/', objectToFormData(data));
			console.log(res);
			this.refresh();
		} catch (err) {
			console.log(err);
		}
	}

	async refresh() {
		try {
			const [res] = [await axios.get(tourney_url)];
			const data = res.data;
			if (data.status === "down") {
				this.setState({
					status: data.status,
					matches: res.data,
				})
			}
			else {
				const members = await axios.get('/api/tournament/members/get/');
				const brackets = convertToDicts(data.tournament.bracket_nodes);
				this.setState({
					status: data.status,
					matches: brackets,
					members: members.data.tournament_members,
					id: data.tournament.tournament_id,
				})
			}
		} catch (err) {
			console.log(err)
		}
	}

	async joinTournament() {
		try {
			const res = await axios.post('/api/tournament/members/register', objectToFormData({member_id: getMemberId()}));
			console.log(res);
			this.refresh();
		} catch (err) {
			console.log(err);
		}
	}

	async leaveTournament() {
		try {
			const res = await axios.post('/api/tournament/members/unregister', objectToFormData({member_id: getMemberId()}));
			console.log(res);
			this.refresh();
		} catch (err) {
			console.log(err);
		}
	}

	changeMatch(matchObj: any) {
		const reset = () => this.setState({popup: null})
		var popup = null;
		console.log(matchObj.matches);
		if (matchObj.matches.length === 0) {
			// Unassigned case
			const team: any = {teamA: new Set(), teamB: new Set()}
			const callback = async () => {
				try {
					const data = {
						bracket_node_id: matchObj.id,
						team_A: Array.from(team.teamA).join(','),
						team_B: Array.from(team.teamB).join(','),
					}
					const res = await axios.post('/api/tournament/add/match/', objectToFormData(data));
					console.log(res);
				} finally {
					reset();
					this.refresh();
				}
			}
			popup = <Popup title="Assign Teams" callback={callback}>
			<div style={{height: "100%", overflowY: "scroll"}} >
			<div className="row">
			<div className="col-9">
			Member
			</div>

			<div className="col-1">
			</div>
			<div className="col-1">
			A
			</div>
			<div className="col-1">
			B
			</div>
			</div>
			{
				this.state.members.map((member: any, idx: number) => {
					return <div className="row" key={idx}>
						<div className="col-9">
						{member.first_name} {member.last_name}
						</div>

						<div className="col-1">
						<RadioButton defaultChecked={true} name={"" + idx} 
							onChange={(ev: any) => {
								if (!ev.target.checked) return;
								team.teamA.delete(member.member_id);
								team.teamB.delete(member.member_id);
							}}/>
						</div>
						<div className="col-1">
						<RadioButton defaultChecked={false} name={"" + idx} onChange={(ev: any) => {
								if (!ev.target.checked) return;
								team.teamA.add(member.member_id);
								team.teamB.delete(member.member_id);
							}}/>
						</div>
						<div className="col-1">
						<RadioButton defaultChecked={false} name={"" + idx} onChange={(ev: any) => {
								if (!ev.target.checked) return;
								team.teamA.delete(member.member_id);
								team.teamB.add(member.member_id);
						}}/>
						</div>
						</div>
				})
			}
			</div>
			</Popup>
		} 

		this.setState({popup:popup});
	}

	componentDidMount() {
		this.refresh();
	}
	render() {
		if (this.state.status === null) {
			return null;
		}
		if (this.state.status === "down") {
			return <TournamentDown refresh={this.refresh}/>
		}
		return (
			<div className="tournament-div">
			{this.state.popup && this.state.popup}
			<TournamentCell matches={this.state.matches} change={this.changeMatch} />
			<div className="row">
			<div className="col-6">
			<button onClick={this.finishTournament} className="interaction-style">Finish</button>
			</div>

			{
				this.state.members.find((e: any) => e.member_id == getMemberId() ) === undefined ? 
				<div className="col-6">
			<button onClick={this.joinTournament} className="interaction-style">Join</button>
			</div> : <div className="col-6">
			<button onClick={this.leaveTournament} className="interaction-style">Leave</button>
			</div>
			}
			</div>
			</div>);
	}
}