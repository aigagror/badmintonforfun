import * as React from 'react';

export class Option {
    public value: string;
    public display: string;

    constructor(val: string, displ: string) {
        this.value = val;
        this.display = displ;
    }
}

export interface SelectProps {
    defaultValue?: string,
    onChange: (value: string) => void,
    options: Array<Option>,
    name: string
}

interface SelectState {
    status: string
}

const selectFadeOutClassName = 'select-check-fade-out';

export interface SelectAreaProps {
    name: string;
    onChange: (event: React.FormEvent<HTMLInputElement>) => void;
    options: Option[];
}

class SelectArea extends React.Component<SelectAreaProps, {}> {
    render() {
        return <span className='select'>
        {
            this.props.options.map((option: Option, idx: number) => {
                return <>
                <input className='select-hidden' 
                    key={idx} id={this.props.name+idx} 
                    value={option.value} name={this.props.name} type='radio'
                    onChange={this.props.onChange} />
                  <label className="select-label" key={idx*-1-1} 
                      htmlFor={this.props.name+idx}>{option.display}</label>
                </>
            })
        }
        </span>
    }
}

export class Select extends React.Component<SelectProps, SelectState> {

	private selectDiv: HTMLDivElement;
    private innerDiv: HTMLDivElement;
	private inputDiv: HTMLInputElement;
	private titleSpan: HTMLSpanElement;
	private wrapper: HTMLDivElement;
    private scrollDiv: HTMLDivElement;
	private status: string;
    private interval: any;

	constructor(props: SelectProps) {
		super(props);

		this.change = this.change.bind(this);
        this.handleClickOutside = this.handleClickOutside.bind(this);
        this.lazyAnimationAdder = this.lazyAnimationAdder.bind(this);
        this._decideInitialStatus = this._decideInitialStatus.bind(this);
        const status = this._decideInitialStatus();
        this.state = {
            status: status,
        }
    }

    _decideInitialStatus() {
        if (this.props.defaultValue) {
            const value = this.props.options.find((option: Option) =>
                option.value === this.props.defaultValue);
            if (!value) {
                return "";
            } else {
                return value.display;
            }
        } else {
            return this.props.options[0].display;
        }
    }

    componentDidMount() {
        document.addEventListener('mousedown', this.handleClickOutside);
        const defaultHeight = 30;
        this.scrollDiv.style.height = defaultHeight+"px";
        this.interval = setInterval(() => {
            const movableArea = this.innerDiv.scrollTop / 
                (this.innerDiv.scrollHeight - this.innerDiv.clientHeight);
            const offset = this.innerDiv.scrollTop * (1 + movableArea) + 2;
            this.scrollDiv.style.top = ""+ offset  + "px";
        }, 20);

        const divMove = (e: any) => {
            const boundingRect = this.selectDiv.getBoundingClientRect();
            const fuzz = .2;
            const height = boundingRect.bottom - boundingRect.top;
            const bottom = boundingRect.bottom - fuzz * height;
            const top = boundingRect.top + fuzz * height;
            const adjusted = Math.max(Math.min(e.clientY, bottom), top);
            const percentage = ( adjusted - top )/ (bottom - top);
            this.innerDiv.scrollTop = percentage * (this.innerDiv.scrollHeight - this.innerDiv.clientHeight);
        }

        function mouseUp()
        {
            window.removeEventListener('mousemove', divMove, true);
        }

        function mouseDown(){
            window.addEventListener('mousemove', divMove, true);
        }

        this.scrollDiv.addEventListener('mousedown', mouseDown, false);
        window.addEventListener('mouseup', mouseUp, false);
    }

    componentWillUnmount() {
        document.removeEventListener('mousedown', this.handleClickOutside);
        clearInterval(this.interval);
    }

    /**
     * Uncheck the input if clicked outside
     * Best to leave the typing generic because typescript does _not_
     * like non-generics with dom.
     */
    handleClickOutside(event: any) {
        if (this.inputDiv && !this.wrapper.contains(event.target)) {
            this.inputDiv.checked = false;
        }
    }

    lazyAnimationAdder(event: any) {
        if (this.inputDiv.checked && !this.selectDiv.classList.contains(selectFadeOutClassName)) {
            this.selectDiv.classList.add(selectFadeOutClassName);
        }
    }

	change(event: React.FormEvent<HTMLInputElement>) {
        const target = event.target as HTMLInputElement;
		if (this.props.onChange) {
			this.props.onChange(target.value);
		}

        // Cool trick to get the label for the input
        const elem = document.querySelector('label[for="' + target.id + '"]');
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
        onChange={this.lazyAnimationAdder}
    	type='checkbox'
    	ref={(input) => this.inputDiv = input}/>

        <label className='select-label select-toggle' htmlFor={this.props.name+"-toggle"} >
        	<span ref={(input) => this.titleSpan = input} className="select-title-text">{this.state.status}</span>
    		<b className='select-arrow'></b>
        </label>

		<div className="select-div" ref={(input) => this.selectDiv = input}>
		<div className="inner-select-div" ref={(input) => this.innerDiv = input}>
        <SelectArea 
            options={this.props.options}
            name={this.props.name}
            onChange={this.change}/>
        <div className="select-scroll" ref={(input) => this.scrollDiv = input}></div>
        </div>
      </div>
      </div>
	}
}
