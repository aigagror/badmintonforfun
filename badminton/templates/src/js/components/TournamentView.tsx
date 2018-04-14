import * as React from "react";
import axios from 'axios';
import {Select, Option} from '../common/Select';
import {objectToFormData} from '../common/Utils';
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


	render() {

		var extra;
		const opts = {
			stroke: "white",
			fill: "white",
			fontFamily: "Arial",
			fontSize: "16px",
			cursor: "pointer",
		}
		const startingX = this.props.x;
		const startingY = this.props.y+15;
		if (this.props.data.state === "undecided") {
			extra = <text style={opts} x={startingX} y={startingY} height={rowHeight} width={columnWidth}>
				TBA
				</text>
		}
		else if (this.props.data.state === "decided") {
			extra = <>
				<text style={opts} x={startingX} y={startingY}>
				{this.props.data.team1}
				</text>
				<text style={opts} x={startingX} y={startingY+rowHeight/2}>
				{this.props.data.team2}
				</text>
				</>
		} else {
			const convert = (num: number): string => {
				if (num < 10) {
					return "0" + num;
				}

				return "" + num;
			}
			extra = <>
				<text style={opts} x={startingX} y={startingY}>
				{this.props.data.team1}
				</text>
				<text style={opts} x={startingX} y={startingY+rowHeight/2}>
				{this.props.data.team2}
				</text>
				<text style={opts} x={startingX+columnWidth-25} y={startingY}>
				{this.props.data.team1_score}
				</text>
				<text style={opts} x={startingX+columnWidth-25} y={startingY+rowHeight/2}>
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
			rx={""+3}
			ry={""+3}
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
		var elems = [<Matchup x={x} y={y} data={rest}/>];
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

export class TournamentView extends React.Component<any, any> {

	constructor(props: any) {
		super(props);
		this.state = {
			status: null,
			matches: null,
		}
		this.refresh = this.refresh.bind(this);
		this.finishTournament = this.finishTournament.bind(this);
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
			const res = await axios.get(tourney_url)
			const data = res.data;
			if (data.status === "down") {
				this.setState({
					status: data.status,
					matches: res.data,
				})			}
			else {
				this.setState({
					status: data.status,
					matches: data.tournament.bracket_nodes,
					id: data.tournament.tournament_id,
				})
			}
		} catch (err) {
			console.log(err)
		}
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
			<TournamentCell matches={this.state.matches} />
			<button onClick={this.finishTournament} className="interaction-style">Finish</button>
			</div>);
	}
}