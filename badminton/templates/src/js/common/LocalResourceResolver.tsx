/**
 * This class serves as a resource resolver for classes.
 * This manages local storage so none of the classes conflict
 * The classes only need to make sure that their resources are unique
 * in of themselves.
 */

import {MailView} from '../components/MailView';
declare var require: Function;
var Cookies: any = require("universal-cookie");

/**
 * Mappings from imported classes to random strings.
 */
const obfuscationMappings: { [cls: string]: string; }= {
	'MailView': 'ysjiUtKPV7',
}

/**
 * Generates key pattern from an instance and an arg
 * arg being the requested key
 */
function _generateKey<T>(instance: T, arg: string) {
	const name = (instance as any).constructor.name as string;
	const obf = obfuscationMappings[name] as string;
	return name + obf;
}

/**
 * Returns a string given the class and the key <arg>
 */
export function getResource<T>(instance: T, arg: string): string {
	const key = _generateKey(instance, arg);
    return localStorage.getItem(key);;
}

/**
 * Sets the requested key <arg> of class <instance> to <value>
 */
export function setResource<T>(instance: T, arg: string, value: string): void {
	const key = _generateKey(instance, arg);
	localStorage.setItem(key, value);
}

const cookies = new Cookies();

export function isBoardMember(): boolean {
	const ret = cookies.get('is_board_member');
	return ret == 'true';
}

export function getMemberId(): number {
	const ret = cookies.get('member_id');
	return parseInt(ret);
}

export function xsrfCookieName(): string {
	return "csrftoken";
}

export function xsrfHeaderName(): string {
	return "X-CSRFToken";
}