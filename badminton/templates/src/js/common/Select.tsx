import * as React from 'react';

export class Select extends React.Component<any, any> {

	private selectDiv: any;
	private inputDiv: any;
	private uid: string;
	private titleSpan: any;
	private wrapper: any;
	private status: string;

	constructor(props: any) {
		super(props);

		this.change = this.change.bind(this);
        this.handleClickOutside = this.handleClickOutside.bind(this);
        var status = ""

        if (this.props.defaultValue) {

			const value = this.props.options.find((option: any) =>
				option.value === this.props.defaultValue);
			if (!value) {
				console.log("Default value not found");
			} else {
				status = value.display;
			}
		} else {
			status = this.props.options[0].display;
		}
        this.state = {
            status: status,
        }
    }

    componentDidMount() {
        document.addEventListener('mousedown', this.handleClickOutside);
    }

    componentWillUnmount() {
        document.removeEventListener('mousedown', this.handleClickOutside);
    }

    /**
     * Alert if clicked on outside of element
     */
    handleClickOutside(event: any) {
        if (this.inputDiv && !this.wrapper.contains(event.target)) {
            this.inputDiv.checked = false;
        }
    }

	change(event: any) {
		if (this.props.onChange) {
			this.props.onChange(event.target.value);
		}
        const elem = document.querySelector('label[for="' + event.target.id + '"]');
        this.setState({
            status: elem.innerHTML,
        });
		this.inputDiv.checked = false;
	}

	render() {
		return <div className="select-wrapper-div" ref={(input) => this.wrapper = input}>
		<input className='select-hidden select-check-toggle' 
    	id={this.props.name+"-toggle"} 
    	name={this.props.name}
    	type='checkbox'
    	ref={(input) => this.inputDiv = input}/>

    <label className='select-label select-toggle' htmlFor={this.props.name+"-toggle"} >
    	<span ref={(input) => this.titleSpan = input} className="select-title-text">{this.state.status}</span>
		<b className='select-arrow'></b>
    </label>

		<div className="select-div" ref={(input) => this.selectDiv = input}>

		<div className="inner-select-div">

    <span className='select'>
    	{
    		this.props.options.map((option: any, idx: number) => {
    			return <>
    			<input className='select-hidden' 
    				key={idx} id={this.props.name+idx} 
    				value={option.value} name={this.props.name} type='radio'
    				onChange={this.change} />
      			<label className="select-label" key={idx*-1-1} 
      				htmlFor={this.props.name+idx}>{option.display}</label>
    			</>
    		})
    	}
    </span>

    </div>
  </div>
  </div>
	}
}
