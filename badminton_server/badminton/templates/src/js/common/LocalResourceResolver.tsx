import {MailView} from '../components/MailView';

const obfuscationMappings: { [cls: string]: string; }= {
	'MailView': 'ysjiUtKPV7',
}

export function getResource<T>(instance: T, arg: string): any {
	const name = (instance as any).constructor.name;
	const obf = obfuscationMappings[name] as string;
    return localStorage.getItem(arg + obf);;
}

export function setResource<T>(instance: T, arg: string, value: string): any {
	const name = (instance as any).constructor.name;
	const obf = obfuscationMappings[name] as string;
	localStorage.setItem(arg + obf, value);
}