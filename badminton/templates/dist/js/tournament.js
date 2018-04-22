/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, {
/******/ 				configurable: false,
/******/ 				enumerable: true,
/******/ 				get: getter
/******/ 			});
/******/ 		}
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 498);
/******/ })
/************************************************************************/
/******/ ({

/***/ 1:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var bind = __webpack_require__(7);
var isBuffer = __webpack_require__(14);

/*global toString:true*/

// utils is a library of generic helper functions non-specific to axios

var toString = Object.prototype.toString;

/**
 * Determine if a value is an Array
 *
 * @param {Object} val The value to test
 * @returns {boolean} True if value is an Array, otherwise false
 */
function isArray(val) {
  return toString.call(val) === '[object Array]';
}

/**
 * Determine if a value is an ArrayBuffer
 *
 * @param {Object} val The value to test
 * @returns {boolean} True if value is an ArrayBuffer, otherwise false
 */
function isArrayBuffer(val) {
  return toString.call(val) === '[object ArrayBuffer]';
}

/**
 * Determine if a value is a FormData
 *
 * @param {Object} val The value to test
 * @returns {boolean} True if value is an FormData, otherwise false
 */
function isFormData(val) {
  return (typeof FormData !== 'undefined') && (val instanceof FormData);
}

/**
 * Determine if a value is a view on an ArrayBuffer
 *
 * @param {Object} val The value to test
 * @returns {boolean} True if value is a view on an ArrayBuffer, otherwise false
 */
function isArrayBufferView(val) {
  var result;
  if ((typeof ArrayBuffer !== 'undefined') && (ArrayBuffer.isView)) {
    result = ArrayBuffer.isView(val);
  } else {
    result = (val) && (val.buffer) && (val.buffer instanceof ArrayBuffer);
  }
  return result;
}

/**
 * Determine if a value is a String
 *
 * @param {Object} val The value to test
 * @returns {boolean} True if value is a String, otherwise false
 */
function isString(val) {
  return typeof val === 'string';
}

/**
 * Determine if a value is a Number
 *
 * @param {Object} val The value to test
 * @returns {boolean} True if value is a Number, otherwise false
 */
function isNumber(val) {
  return typeof val === 'number';
}

/**
 * Determine if a value is undefined
 *
 * @param {Object} val The value to test
 * @returns {boolean} True if the value is undefined, otherwise false
 */
function isUndefined(val) {
  return typeof val === 'undefined';
}

/**
 * Determine if a value is an Object
 *
 * @param {Object} val The value to test
 * @returns {boolean} True if value is an Object, otherwise false
 */
function isObject(val) {
  return val !== null && typeof val === 'object';
}

/**
 * Determine if a value is a Date
 *
 * @param {Object} val The value to test
 * @returns {boolean} True if value is a Date, otherwise false
 */
function isDate(val) {
  return toString.call(val) === '[object Date]';
}

/**
 * Determine if a value is a File
 *
 * @param {Object} val The value to test
 * @returns {boolean} True if value is a File, otherwise false
 */
function isFile(val) {
  return toString.call(val) === '[object File]';
}

/**
 * Determine if a value is a Blob
 *
 * @param {Object} val The value to test
 * @returns {boolean} True if value is a Blob, otherwise false
 */
function isBlob(val) {
  return toString.call(val) === '[object Blob]';
}

/**
 * Determine if a value is a Function
 *
 * @param {Object} val The value to test
 * @returns {boolean} True if value is a Function, otherwise false
 */
function isFunction(val) {
  return toString.call(val) === '[object Function]';
}

/**
 * Determine if a value is a Stream
 *
 * @param {Object} val The value to test
 * @returns {boolean} True if value is a Stream, otherwise false
 */
function isStream(val) {
  return isObject(val) && isFunction(val.pipe);
}

/**
 * Determine if a value is a URLSearchParams object
 *
 * @param {Object} val The value to test
 * @returns {boolean} True if value is a URLSearchParams object, otherwise false
 */
function isURLSearchParams(val) {
  return typeof URLSearchParams !== 'undefined' && val instanceof URLSearchParams;
}

/**
 * Trim excess whitespace off the beginning and end of a string
 *
 * @param {String} str The String to trim
 * @returns {String} The String freed of excess whitespace
 */
function trim(str) {
  return str.replace(/^\s*/, '').replace(/\s*$/, '');
}

/**
 * Determine if we're running in a standard browser environment
 *
 * This allows axios to run in a web worker, and react-native.
 * Both environments support XMLHttpRequest, but not fully standard globals.
 *
 * web workers:
 *  typeof window -> undefined
 *  typeof document -> undefined
 *
 * react-native:
 *  navigator.product -> 'ReactNative'
 */
function isStandardBrowserEnv() {
  if (typeof navigator !== 'undefined' && navigator.product === 'ReactNative') {
    return false;
  }
  return (
    typeof window !== 'undefined' &&
    typeof document !== 'undefined'
  );
}

/**
 * Iterate over an Array or an Object invoking a function for each item.
 *
 * If `obj` is an Array callback will be called passing
 * the value, index, and complete array for each item.
 *
 * If 'obj' is an Object callback will be called passing
 * the value, key, and complete object for each property.
 *
 * @param {Object|Array} obj The object to iterate
 * @param {Function} fn The callback to invoke for each item
 */
function forEach(obj, fn) {
  // Don't bother if no value provided
  if (obj === null || typeof obj === 'undefined') {
    return;
  }

  // Force an array if not already something iterable
  if (typeof obj !== 'object') {
    /*eslint no-param-reassign:0*/
    obj = [obj];
  }

  if (isArray(obj)) {
    // Iterate over array values
    for (var i = 0, l = obj.length; i < l; i++) {
      fn.call(null, obj[i], i, obj);
    }
  } else {
    // Iterate over object keys
    for (var key in obj) {
      if (Object.prototype.hasOwnProperty.call(obj, key)) {
        fn.call(null, obj[key], key, obj);
      }
    }
  }
}

/**
 * Accepts varargs expecting each argument to be an object, then
 * immutably merges the properties of each object and returns result.
 *
 * When multiple objects contain the same key the later object in
 * the arguments list will take precedence.
 *
 * Example:
 *
 * ```js
 * var result = merge({foo: 123}, {foo: 456});
 * console.log(result.foo); // outputs 456
 * ```
 *
 * @param {Object} obj1 Object to merge
 * @returns {Object} Result of all merge properties
 */
function merge(/* obj1, obj2, obj3, ... */) {
  var result = {};
  function assignValue(val, key) {
    if (typeof result[key] === 'object' && typeof val === 'object') {
      result[key] = merge(result[key], val);
    } else {
      result[key] = val;
    }
  }

  for (var i = 0, l = arguments.length; i < l; i++) {
    forEach(arguments[i], assignValue);
  }
  return result;
}

/**
 * Extends object a by mutably adding to it the properties of object b.
 *
 * @param {Object} a The object to be extended
 * @param {Object} b The object to copy properties from
 * @param {Object} thisArg The object to bind function to
 * @return {Object} The resulting value of object a
 */
function extend(a, b, thisArg) {
  forEach(b, function assignValue(val, key) {
    if (thisArg && typeof val === 'function') {
      a[key] = bind(val, thisArg);
    } else {
      a[key] = val;
    }
  });
  return a;
}

module.exports = {
  isArray: isArray,
  isArrayBuffer: isArrayBuffer,
  isBuffer: isBuffer,
  isFormData: isFormData,
  isArrayBufferView: isArrayBufferView,
  isString: isString,
  isNumber: isNumber,
  isObject: isObject,
  isUndefined: isUndefined,
  isDate: isDate,
  isFile: isFile,
  isBlob: isBlob,
  isFunction: isFunction,
  isStream: isStream,
  isURLSearchParams: isURLSearchParams,
  isStandardBrowserEnv: isStandardBrowserEnv,
  forEach: forEach,
  merge: merge,
  extend: extend,
  trim: trim
};


/***/ }),

/***/ 10:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


module.exports = function isCancel(value) {
  return !!(value && value.__CANCEL__);
};


/***/ }),

/***/ 11:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


/**
 * A `Cancel` is an object that is thrown when an operation is canceled.
 *
 * @class
 * @param {string=} message The message.
 */
function Cancel(message) {
  this.message = message;
}

Cancel.prototype.toString = function toString() {
  return 'Cancel' + (this.message ? ': ' + this.message : '');
};

Cancel.prototype.__CANCEL__ = true;

module.exports = Cancel;


/***/ }),

/***/ 12:
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(13);

/***/ }),

/***/ 13:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var utils = __webpack_require__(1);
var bind = __webpack_require__(7);
var Axios = __webpack_require__(15);
var defaults = __webpack_require__(4);

/**
 * Create an instance of Axios
 *
 * @param {Object} defaultConfig The default config for the instance
 * @return {Axios} A new instance of Axios
 */
function createInstance(defaultConfig) {
  var context = new Axios(defaultConfig);
  var instance = bind(Axios.prototype.request, context);

  // Copy axios.prototype to instance
  utils.extend(instance, Axios.prototype, context);

  // Copy context to instance
  utils.extend(instance, context);

  return instance;
}

// Create the default instance to be exported
var axios = createInstance(defaults);

// Expose Axios class to allow class inheritance
axios.Axios = Axios;

// Factory for creating new instances
axios.create = function create(instanceConfig) {
  return createInstance(utils.merge(defaults, instanceConfig));
};

// Expose Cancel & CancelToken
axios.Cancel = __webpack_require__(11);
axios.CancelToken = __webpack_require__(29);
axios.isCancel = __webpack_require__(10);

// Expose all/spread
axios.all = function all(promises) {
  return Promise.all(promises);
};
axios.spread = __webpack_require__(30);

module.exports = axios;

// Allow use of default import syntax in TypeScript
module.exports.default = axios;


/***/ }),

/***/ 14:
/***/ (function(module, exports) {

/*!
 * Determine if an object is a Buffer
 *
 * @author   Feross Aboukhadijeh <https://feross.org>
 * @license  MIT
 */

// The _isBuffer check is for Safari 5-7 support, because it's missing
// Object.prototype.constructor. Remove this eventually
module.exports = function (obj) {
  return obj != null && (isBuffer(obj) || isSlowBuffer(obj) || !!obj._isBuffer)
}

function isBuffer (obj) {
  return !!obj.constructor && typeof obj.constructor.isBuffer === 'function' && obj.constructor.isBuffer(obj)
}

// For Node v0.10 support. Remove this eventually.
function isSlowBuffer (obj) {
  return typeof obj.readFloatLE === 'function' && typeof obj.slice === 'function' && isBuffer(obj.slice(0, 0))
}


/***/ }),

/***/ 15:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var defaults = __webpack_require__(4);
var utils = __webpack_require__(1);
var InterceptorManager = __webpack_require__(24);
var dispatchRequest = __webpack_require__(25);

/**
 * Create a new instance of Axios
 *
 * @param {Object} instanceConfig The default config for the instance
 */
function Axios(instanceConfig) {
  this.defaults = instanceConfig;
  this.interceptors = {
    request: new InterceptorManager(),
    response: new InterceptorManager()
  };
}

/**
 * Dispatch a request
 *
 * @param {Object} config The config specific for this request (merged with this.defaults)
 */
Axios.prototype.request = function request(config) {
  /*eslint no-param-reassign:0*/
  // Allow for axios('example/url'[, config]) a la fetch API
  if (typeof config === 'string') {
    config = utils.merge({
      url: arguments[0]
    }, arguments[1]);
  }

  config = utils.merge(defaults, {method: 'get'}, this.defaults, config);
  config.method = config.method.toLowerCase();

  // Hook up interceptors middleware
  var chain = [dispatchRequest, undefined];
  var promise = Promise.resolve(config);

  this.interceptors.request.forEach(function unshiftRequestInterceptors(interceptor) {
    chain.unshift(interceptor.fulfilled, interceptor.rejected);
  });

  this.interceptors.response.forEach(function pushResponseInterceptors(interceptor) {
    chain.push(interceptor.fulfilled, interceptor.rejected);
  });

  while (chain.length) {
    promise = promise.then(chain.shift(), chain.shift());
  }

  return promise;
};

// Provide aliases for supported request methods
utils.forEach(['delete', 'get', 'head', 'options'], function forEachMethodNoData(method) {
  /*eslint func-names:0*/
  Axios.prototype[method] = function(url, config) {
    return this.request(utils.merge(config || {}, {
      method: method,
      url: url
    }));
  };
});

utils.forEach(['post', 'put', 'patch'], function forEachMethodWithData(method) {
  /*eslint func-names:0*/
  Axios.prototype[method] = function(url, data, config) {
    return this.request(utils.merge(config || {}, {
      method: method,
      url: url,
      data: data
    }));
  };
});

module.exports = Axios;


/***/ }),

/***/ 16:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var utils = __webpack_require__(1);

module.exports = function normalizeHeaderName(headers, normalizedName) {
  utils.forEach(headers, function processHeader(value, name) {
    if (name !== normalizedName && name.toUpperCase() === normalizedName.toUpperCase()) {
      headers[normalizedName] = value;
      delete headers[name];
    }
  });
};


/***/ }),

/***/ 17:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var createError = __webpack_require__(9);

/**
 * Resolve or reject a Promise based on response status.
 *
 * @param {Function} resolve A function that resolves the promise.
 * @param {Function} reject A function that rejects the promise.
 * @param {object} response The response.
 */
module.exports = function settle(resolve, reject, response) {
  var validateStatus = response.config.validateStatus;
  // Note: status is not exposed by XDomainRequest
  if (!response.status || !validateStatus || validateStatus(response.status)) {
    resolve(response);
  } else {
    reject(createError(
      'Request failed with status code ' + response.status,
      response.config,
      null,
      response.request,
      response
    ));
  }
};


/***/ }),

/***/ 18:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


/**
 * Update an Error with the specified config, error code, and response.
 *
 * @param {Error} error The error to update.
 * @param {Object} config The config.
 * @param {string} [code] The error code (for example, 'ECONNABORTED').
 * @param {Object} [request] The request.
 * @param {Object} [response] The response.
 * @returns {Error} The error.
 */
module.exports = function enhanceError(error, config, code, request, response) {
  error.config = config;
  if (code) {
    error.code = code;
  }
  error.request = request;
  error.response = response;
  return error;
};


/***/ }),

/***/ 19:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var utils = __webpack_require__(1);

function encode(val) {
  return encodeURIComponent(val).
    replace(/%40/gi, '@').
    replace(/%3A/gi, ':').
    replace(/%24/g, '$').
    replace(/%2C/gi, ',').
    replace(/%20/g, '+').
    replace(/%5B/gi, '[').
    replace(/%5D/gi, ']');
}

/**
 * Build a URL by appending params to the end
 *
 * @param {string} url The base of the url (e.g., http://www.google.com)
 * @param {object} [params] The params to be appended
 * @returns {string} The formatted url
 */
module.exports = function buildURL(url, params, paramsSerializer) {
  /*eslint no-param-reassign:0*/
  if (!params) {
    return url;
  }

  var serializedParams;
  if (paramsSerializer) {
    serializedParams = paramsSerializer(params);
  } else if (utils.isURLSearchParams(params)) {
    serializedParams = params.toString();
  } else {
    var parts = [];

    utils.forEach(params, function serialize(val, key) {
      if (val === null || typeof val === 'undefined') {
        return;
      }

      if (utils.isArray(val)) {
        key = key + '[]';
      } else {
        val = [val];
      }

      utils.forEach(val, function parseValue(v) {
        if (utils.isDate(v)) {
          v = v.toISOString();
        } else if (utils.isObject(v)) {
          v = JSON.stringify(v);
        }
        parts.push(encode(key) + '=' + encode(v));
      });
    });

    serializedParams = parts.join('&');
  }

  if (serializedParams) {
    url += (url.indexOf('?') === -1 ? '?' : '&') + serializedParams;
  }

  return url;
};


/***/ }),

/***/ 2:
/***/ (function(module, exports) {

module.exports = React;

/***/ }),

/***/ 20:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var utils = __webpack_require__(1);

// Headers whose duplicates are ignored by node
// c.f. https://nodejs.org/api/http.html#http_message_headers
var ignoreDuplicateOf = [
  'age', 'authorization', 'content-length', 'content-type', 'etag',
  'expires', 'from', 'host', 'if-modified-since', 'if-unmodified-since',
  'last-modified', 'location', 'max-forwards', 'proxy-authorization',
  'referer', 'retry-after', 'user-agent'
];

/**
 * Parse headers into an object
 *
 * ```
 * Date: Wed, 27 Aug 2014 08:58:49 GMT
 * Content-Type: application/json
 * Connection: keep-alive
 * Transfer-Encoding: chunked
 * ```
 *
 * @param {String} headers Headers needing to be parsed
 * @returns {Object} Headers parsed into an object
 */
module.exports = function parseHeaders(headers) {
  var parsed = {};
  var key;
  var val;
  var i;

  if (!headers) { return parsed; }

  utils.forEach(headers.split('\n'), function parser(line) {
    i = line.indexOf(':');
    key = utils.trim(line.substr(0, i)).toLowerCase();
    val = utils.trim(line.substr(i + 1));

    if (key) {
      if (parsed[key] && ignoreDuplicateOf.indexOf(key) >= 0) {
        return;
      }
      if (key === 'set-cookie') {
        parsed[key] = (parsed[key] ? parsed[key] : []).concat([val]);
      } else {
        parsed[key] = parsed[key] ? parsed[key] + ', ' + val : val;
      }
    }
  });

  return parsed;
};


/***/ }),

/***/ 21:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var utils = __webpack_require__(1);

module.exports = (
  utils.isStandardBrowserEnv() ?

  // Standard browser envs have full support of the APIs needed to test
  // whether the request URL is of the same origin as current location.
  (function standardBrowserEnv() {
    var msie = /(msie|trident)/i.test(navigator.userAgent);
    var urlParsingNode = document.createElement('a');
    var originURL;

    /**
    * Parse a URL to discover it's components
    *
    * @param {String} url The URL to be parsed
    * @returns {Object}
    */
    function resolveURL(url) {
      var href = url;

      if (msie) {
        // IE needs attribute set twice to normalize properties
        urlParsingNode.setAttribute('href', href);
        href = urlParsingNode.href;
      }

      urlParsingNode.setAttribute('href', href);

      // urlParsingNode provides the UrlUtils interface - http://url.spec.whatwg.org/#urlutils
      return {
        href: urlParsingNode.href,
        protocol: urlParsingNode.protocol ? urlParsingNode.protocol.replace(/:$/, '') : '',
        host: urlParsingNode.host,
        search: urlParsingNode.search ? urlParsingNode.search.replace(/^\?/, '') : '',
        hash: urlParsingNode.hash ? urlParsingNode.hash.replace(/^#/, '') : '',
        hostname: urlParsingNode.hostname,
        port: urlParsingNode.port,
        pathname: (urlParsingNode.pathname.charAt(0) === '/') ?
                  urlParsingNode.pathname :
                  '/' + urlParsingNode.pathname
      };
    }

    originURL = resolveURL(window.location.href);

    /**
    * Determine if a URL shares the same origin as the current location
    *
    * @param {String} requestURL The URL to test
    * @returns {boolean} True if URL shares the same origin, otherwise false
    */
    return function isURLSameOrigin(requestURL) {
      var parsed = (utils.isString(requestURL)) ? resolveURL(requestURL) : requestURL;
      return (parsed.protocol === originURL.protocol &&
            parsed.host === originURL.host);
    };
  })() :

  // Non standard browser envs (web workers, react-native) lack needed support.
  (function nonStandardBrowserEnv() {
    return function isURLSameOrigin() {
      return true;
    };
  })()
);


/***/ }),

/***/ 213:
/***/ (function(module, exports, __webpack_require__) {

"use strict";

/**
 * Acts as a this wrapper around radio button so that
 * Styles, animation, and consistency is maintained
 */
var __extends = (this && this.__extends) || (function () {
    var extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
var __assign = (this && this.__assign) || Object.assign || function(t) {
    for (var s, i = 1, n = arguments.length; i < n; i++) {
        s = arguments[i];
        for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
            t[p] = s[p];
    }
    return t;
};
Object.defineProperty(exports, "__esModule", { value: true });
var React = __webpack_require__(2);
var reverseSwirlClass = "radio-swirl-back";
var RadioButtonState = /** @class */ (function () {
    function RadioButtonState() {
    }
    return RadioButtonState;
}());
// Typescript doesn't support variadic types so the props have to be any
// To forward to the standard input field
var RadioButton = /** @class */ (function (_super) {
    __extends(RadioButton, _super);
    function RadioButton(props) {
        var _this = _super.call(this, props) || this;
        _this.clicked = _this.clicked.bind(_this);
        _this.hover = _this.hover.bind(_this);
        return _this;
    }
    RadioButton.prototype.hover = function (event) {
        // Must remove or after :hover disappears the
        // Animation will trigger again
        // No op to remove a class that does not exist
        if (event.animationName.includes('reverse')) {
            this.spanElem.classList.remove(reverseSwirlClass);
        }
    };
    RadioButton.prototype.componentDidMount = function () {
        // Make sure that the class has the reverse if checked for the first time
        this.spanElem.addEventListener('animationend', this.hover);
        this.clicked();
    };
    RadioButton.prototype.componentWillUnmount = function () {
        this.spanElem.removeEventListener('animationend', this.hover);
    };
    RadioButton.prototype.clicked = function () {
        if (this.inputElem.checked) {
            // We are checking it
            this.spanElem.classList.add(reverseSwirlClass);
        }
    };
    RadioButton.prototype.render = function () {
        /* Forward all props using ... to the input field since this is supposed
         * to be a thin wrapper around it */
        var _this = this;
        return React.createElement("label", { className: "radio-container" },
            React.createElement("input", __assign({}, this.props, { type: "radio", onClick: this.clicked, ref: function (input) { return _this.inputElem = input; } })),
            React.createElement("span", { className: "radio-checkmark", ref: function (input) { return _this.spanElem = input; } }));
    };
    return RadioButton;
}(React.Component));
exports.RadioButton = RadioButton;


/***/ }),

/***/ 22:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


// btoa polyfill for IE<10 courtesy https://github.com/davidchambers/Base64.js

var chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';

function E() {
  this.message = 'String contains an invalid character';
}
E.prototype = new Error;
E.prototype.code = 5;
E.prototype.name = 'InvalidCharacterError';

function btoa(input) {
  var str = String(input);
  var output = '';
  for (
    // initialize result and counter
    var block, charCode, idx = 0, map = chars;
    // if the next str index does not exist:
    //   change the mapping table to "="
    //   check if d has no fractional digits
    str.charAt(idx | 0) || (map = '=', idx % 1);
    // "8 - idx % 1 * 8" generates the sequence 2, 4, 6, 8
    output += map.charAt(63 & block >> 8 - idx % 1 * 8)
  ) {
    charCode = str.charCodeAt(idx += 3 / 4);
    if (charCode > 0xFF) {
      throw new E();
    }
    block = block << 8 | charCode;
  }
  return output;
}

module.exports = btoa;


/***/ }),

/***/ 23:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var utils = __webpack_require__(1);

module.exports = (
  utils.isStandardBrowserEnv() ?

  // Standard browser envs support document.cookie
  (function standardBrowserEnv() {
    return {
      write: function write(name, value, expires, path, domain, secure) {
        var cookie = [];
        cookie.push(name + '=' + encodeURIComponent(value));

        if (utils.isNumber(expires)) {
          cookie.push('expires=' + new Date(expires).toGMTString());
        }

        if (utils.isString(path)) {
          cookie.push('path=' + path);
        }

        if (utils.isString(domain)) {
          cookie.push('domain=' + domain);
        }

        if (secure === true) {
          cookie.push('secure');
        }

        document.cookie = cookie.join('; ');
      },

      read: function read(name) {
        var match = document.cookie.match(new RegExp('(^|;\\s*)(' + name + ')=([^;]*)'));
        return (match ? decodeURIComponent(match[3]) : null);
      },

      remove: function remove(name) {
        this.write(name, '', Date.now() - 86400000);
      }
    };
  })() :

  // Non standard browser env (web workers, react-native) lack needed support.
  (function nonStandardBrowserEnv() {
    return {
      write: function write() {},
      read: function read() { return null; },
      remove: function remove() {}
    };
  })()
);


/***/ }),

/***/ 24:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var utils = __webpack_require__(1);

function InterceptorManager() {
  this.handlers = [];
}

/**
 * Add a new interceptor to the stack
 *
 * @param {Function} fulfilled The function to handle `then` for a `Promise`
 * @param {Function} rejected The function to handle `reject` for a `Promise`
 *
 * @return {Number} An ID used to remove interceptor later
 */
InterceptorManager.prototype.use = function use(fulfilled, rejected) {
  this.handlers.push({
    fulfilled: fulfilled,
    rejected: rejected
  });
  return this.handlers.length - 1;
};

/**
 * Remove an interceptor from the stack
 *
 * @param {Number} id The ID that was returned by `use`
 */
InterceptorManager.prototype.eject = function eject(id) {
  if (this.handlers[id]) {
    this.handlers[id] = null;
  }
};

/**
 * Iterate over all the registered interceptors
 *
 * This method is particularly useful for skipping over any
 * interceptors that may have become `null` calling `eject`.
 *
 * @param {Function} fn The function to call for each interceptor
 */
InterceptorManager.prototype.forEach = function forEach(fn) {
  utils.forEach(this.handlers, function forEachHandler(h) {
    if (h !== null) {
      fn(h);
    }
  });
};

module.exports = InterceptorManager;


/***/ }),

/***/ 25:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var utils = __webpack_require__(1);
var transformData = __webpack_require__(26);
var isCancel = __webpack_require__(10);
var defaults = __webpack_require__(4);
var isAbsoluteURL = __webpack_require__(27);
var combineURLs = __webpack_require__(28);

/**
 * Throws a `Cancel` if cancellation has been requested.
 */
function throwIfCancellationRequested(config) {
  if (config.cancelToken) {
    config.cancelToken.throwIfRequested();
  }
}

/**
 * Dispatch a request to the server using the configured adapter.
 *
 * @param {object} config The config that is to be used for the request
 * @returns {Promise} The Promise to be fulfilled
 */
module.exports = function dispatchRequest(config) {
  throwIfCancellationRequested(config);

  // Support baseURL config
  if (config.baseURL && !isAbsoluteURL(config.url)) {
    config.url = combineURLs(config.baseURL, config.url);
  }

  // Ensure headers exist
  config.headers = config.headers || {};

  // Transform request data
  config.data = transformData(
    config.data,
    config.headers,
    config.transformRequest
  );

  // Flatten headers
  config.headers = utils.merge(
    config.headers.common || {},
    config.headers[config.method] || {},
    config.headers || {}
  );

  utils.forEach(
    ['delete', 'get', 'head', 'post', 'put', 'patch', 'common'],
    function cleanHeaderConfig(method) {
      delete config.headers[method];
    }
  );

  var adapter = config.adapter || defaults.adapter;

  return adapter(config).then(function onAdapterResolution(response) {
    throwIfCancellationRequested(config);

    // Transform response data
    response.data = transformData(
      response.data,
      response.headers,
      config.transformResponse
    );

    return response;
  }, function onAdapterRejection(reason) {
    if (!isCancel(reason)) {
      throwIfCancellationRequested(config);

      // Transform response data
      if (reason && reason.response) {
        reason.response.data = transformData(
          reason.response.data,
          reason.response.headers,
          config.transformResponse
        );
      }
    }

    return Promise.reject(reason);
  });
};


/***/ }),

/***/ 26:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var utils = __webpack_require__(1);

/**
 * Transform the data for a request or a response
 *
 * @param {Object|String} data The data to be transformed
 * @param {Array} headers The headers for the request or response
 * @param {Array|Function} fns A single function or Array of functions
 * @returns {*} The resulting transformed data
 */
module.exports = function transformData(data, headers, fns) {
  /*eslint no-param-reassign:0*/
  utils.forEach(fns, function transform(fn) {
    data = fn(data, headers);
  });

  return data;
};


/***/ }),

/***/ 27:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


/**
 * Determines whether the specified URL is absolute
 *
 * @param {string} url The URL to test
 * @returns {boolean} True if the specified URL is absolute, otherwise false
 */
module.exports = function isAbsoluteURL(url) {
  // A URL is considered absolute if it begins with "<scheme>://" or "//" (protocol-relative URL).
  // RFC 3986 defines scheme name as a sequence of characters beginning with a letter and followed
  // by any combination of letters, digits, plus, period, or hyphen.
  return /^([a-z][a-z\d\+\-\.]*:)?\/\//i.test(url);
};


/***/ }),

/***/ 28:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


/**
 * Creates a new URL by combining the specified URLs
 *
 * @param {string} baseURL The base URL
 * @param {string} relativeURL The relative URL
 * @returns {string} The combined URL
 */
module.exports = function combineURLs(baseURL, relativeURL) {
  return relativeURL
    ? baseURL.replace(/\/+$/, '') + '/' + relativeURL.replace(/^\/+/, '')
    : baseURL;
};


/***/ }),

/***/ 29:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var Cancel = __webpack_require__(11);

/**
 * A `CancelToken` is an object that can be used to request cancellation of an operation.
 *
 * @class
 * @param {Function} executor The executor function.
 */
function CancelToken(executor) {
  if (typeof executor !== 'function') {
    throw new TypeError('executor must be a function.');
  }

  var resolvePromise;
  this.promise = new Promise(function promiseExecutor(resolve) {
    resolvePromise = resolve;
  });

  var token = this;
  executor(function cancel(message) {
    if (token.reason) {
      // Cancellation has already been requested
      return;
    }

    token.reason = new Cancel(message);
    resolvePromise(token.reason);
  });
}

/**
 * Throws a `Cancel` if cancellation has been requested.
 */
CancelToken.prototype.throwIfRequested = function throwIfRequested() {
  if (this.reason) {
    throw this.reason;
  }
};

/**
 * Returns an object that contains a new `CancelToken` and a function that, when called,
 * cancels the `CancelToken`.
 */
CancelToken.source = function source() {
  var cancel;
  var token = new CancelToken(function executor(c) {
    cancel = c;
  });
  return {
    token: token,
    cancel: cancel
  };
};

module.exports = CancelToken;


/***/ }),

/***/ 3:
/***/ (function(module, exports) {

// shim for using process in browser
var process = module.exports = {};

// cached from whatever global is present so that test runners that stub it
// don't break things.  But we need to wrap it in a try catch in case it is
// wrapped in strict mode code which doesn't define any globals.  It's inside a
// function because try/catches deoptimize in certain engines.

var cachedSetTimeout;
var cachedClearTimeout;

function defaultSetTimout() {
    throw new Error('setTimeout has not been defined');
}
function defaultClearTimeout () {
    throw new Error('clearTimeout has not been defined');
}
(function () {
    try {
        if (typeof setTimeout === 'function') {
            cachedSetTimeout = setTimeout;
        } else {
            cachedSetTimeout = defaultSetTimout;
        }
    } catch (e) {
        cachedSetTimeout = defaultSetTimout;
    }
    try {
        if (typeof clearTimeout === 'function') {
            cachedClearTimeout = clearTimeout;
        } else {
            cachedClearTimeout = defaultClearTimeout;
        }
    } catch (e) {
        cachedClearTimeout = defaultClearTimeout;
    }
} ())
function runTimeout(fun) {
    if (cachedSetTimeout === setTimeout) {
        //normal enviroments in sane situations
        return setTimeout(fun, 0);
    }
    // if setTimeout wasn't available but was latter defined
    if ((cachedSetTimeout === defaultSetTimout || !cachedSetTimeout) && setTimeout) {
        cachedSetTimeout = setTimeout;
        return setTimeout(fun, 0);
    }
    try {
        // when when somebody has screwed with setTimeout but no I.E. maddness
        return cachedSetTimeout(fun, 0);
    } catch(e){
        try {
            // When we are in I.E. but the script has been evaled so I.E. doesn't trust the global object when called normally
            return cachedSetTimeout.call(null, fun, 0);
        } catch(e){
            // same as above but when it's a version of I.E. that must have the global object for 'this', hopfully our context correct otherwise it will throw a global error
            return cachedSetTimeout.call(this, fun, 0);
        }
    }


}
function runClearTimeout(marker) {
    if (cachedClearTimeout === clearTimeout) {
        //normal enviroments in sane situations
        return clearTimeout(marker);
    }
    // if clearTimeout wasn't available but was latter defined
    if ((cachedClearTimeout === defaultClearTimeout || !cachedClearTimeout) && clearTimeout) {
        cachedClearTimeout = clearTimeout;
        return clearTimeout(marker);
    }
    try {
        // when when somebody has screwed with setTimeout but no I.E. maddness
        return cachedClearTimeout(marker);
    } catch (e){
        try {
            // When we are in I.E. but the script has been evaled so I.E. doesn't  trust the global object when called normally
            return cachedClearTimeout.call(null, marker);
        } catch (e){
            // same as above but when it's a version of I.E. that must have the global object for 'this', hopfully our context correct otherwise it will throw a global error.
            // Some versions of I.E. have different rules for clearTimeout vs setTimeout
            return cachedClearTimeout.call(this, marker);
        }
    }



}
var queue = [];
var draining = false;
var currentQueue;
var queueIndex = -1;

function cleanUpNextTick() {
    if (!draining || !currentQueue) {
        return;
    }
    draining = false;
    if (currentQueue.length) {
        queue = currentQueue.concat(queue);
    } else {
        queueIndex = -1;
    }
    if (queue.length) {
        drainQueue();
    }
}

function drainQueue() {
    if (draining) {
        return;
    }
    var timeout = runTimeout(cleanUpNextTick);
    draining = true;

    var len = queue.length;
    while(len) {
        currentQueue = queue;
        queue = [];
        while (++queueIndex < len) {
            if (currentQueue) {
                currentQueue[queueIndex].run();
            }
        }
        queueIndex = -1;
        len = queue.length;
    }
    currentQueue = null;
    draining = false;
    runClearTimeout(timeout);
}

process.nextTick = function (fun) {
    var args = new Array(arguments.length - 1);
    if (arguments.length > 1) {
        for (var i = 1; i < arguments.length; i++) {
            args[i - 1] = arguments[i];
        }
    }
    queue.push(new Item(fun, args));
    if (queue.length === 1 && !draining) {
        runTimeout(drainQueue);
    }
};

// v8 likes predictible objects
function Item(fun, array) {
    this.fun = fun;
    this.array = array;
}
Item.prototype.run = function () {
    this.fun.apply(null, this.array);
};
process.title = 'browser';
process.browser = true;
process.env = {};
process.argv = [];
process.version = ''; // empty string to avoid regexp issues
process.versions = {};

function noop() {}

process.on = noop;
process.addListener = noop;
process.once = noop;
process.off = noop;
process.removeListener = noop;
process.removeAllListeners = noop;
process.emit = noop;
process.prependListener = noop;
process.prependOnceListener = noop;

process.listeners = function (name) { return [] }

process.binding = function (name) {
    throw new Error('process.binding is not supported');
};

process.cwd = function () { return '/' };
process.chdir = function (dir) {
    throw new Error('process.chdir is not supported');
};
process.umask = function() { return 0; };


/***/ }),

/***/ 30:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


/**
 * Syntactic sugar for invoking a function and expanding an array for arguments.
 *
 * Common use case would be to use `Function.prototype.apply`.
 *
 *  ```js
 *  function f(x, y, z) {}
 *  var args = [1, 2, 3];
 *  f.apply(null, args);
 *  ```
 *
 * With `spread` this example can be re-written.
 *
 *  ```js
 *  spread(function(x, y, z) {})([1, 2, 3]);
 *  ```
 *
 * @param {Function} callback
 * @returns {Function}
 */
module.exports = function spread(callback) {
  return function wrap(arr) {
    return callback.apply(null, arr);
  };
};


/***/ }),

/***/ 31:
/***/ (function(module, exports, __webpack_require__) {

"use strict";
/*
object-assign
(c) Sindre Sorhus
@license MIT
*/


/* eslint-disable no-unused-vars */
var getOwnPropertySymbols = Object.getOwnPropertySymbols;
var hasOwnProperty = Object.prototype.hasOwnProperty;
var propIsEnumerable = Object.prototype.propertyIsEnumerable;

function toObject(val) {
	if (val === null || val === undefined) {
		throw new TypeError('Object.assign cannot be called with null or undefined');
	}

	return Object(val);
}

function shouldUseNative() {
	try {
		if (!Object.assign) {
			return false;
		}

		// Detect buggy property enumeration order in older V8 versions.

		// https://bugs.chromium.org/p/v8/issues/detail?id=4118
		var test1 = new String('abc');  // eslint-disable-line no-new-wrappers
		test1[5] = 'de';
		if (Object.getOwnPropertyNames(test1)[0] === '5') {
			return false;
		}

		// https://bugs.chromium.org/p/v8/issues/detail?id=3056
		var test2 = {};
		for (var i = 0; i < 10; i++) {
			test2['_' + String.fromCharCode(i)] = i;
		}
		var order2 = Object.getOwnPropertyNames(test2).map(function (n) {
			return test2[n];
		});
		if (order2.join('') !== '0123456789') {
			return false;
		}

		// https://bugs.chromium.org/p/v8/issues/detail?id=3056
		var test3 = {};
		'abcdefghijklmnopqrst'.split('').forEach(function (letter) {
			test3[letter] = letter;
		});
		if (Object.keys(Object.assign({}, test3)).join('') !==
				'abcdefghijklmnopqrst') {
			return false;
		}

		return true;
	} catch (err) {
		// We don't expect any of the above to throw, but better to be safe.
		return false;
	}
}

module.exports = shouldUseNative() ? Object.assign : function (target, source) {
	var from;
	var to = toObject(target);
	var symbols;

	for (var s = 1; s < arguments.length; s++) {
		from = Object(arguments[s]);

		for (var key in from) {
			if (hasOwnProperty.call(from, key)) {
				to[key] = from[key];
			}
		}

		if (getOwnPropertySymbols) {
			symbols = getOwnPropertySymbols(from);
			for (var i = 0; i < symbols.length; i++) {
				if (propIsEnumerable.call(from, symbols[i])) {
					to[symbols[i]] = from[symbols[i]];
				}
			}
		}
	}

	return to;
};


/***/ }),

/***/ 33:
/***/ (function(module, exports, __webpack_require__) {

"use strict";

/**
 * This class serves as a resource resolver for classes.
 * This manages local storage so none of the classes conflict
 * The classes only need to make sure that their resources are unique
 * in of themselves.
 */
Object.defineProperty(exports, "__esModule", { value: true });
var Cookies = __webpack_require__(37);
/**
 * Mappings from imported classes to random strings.
 */
var obfuscationMappings = {
    'MailView': 'ysjiUtKPV7',
};
/**
 * Generates key pattern from an instance and an arg
 * arg being the requested key
 */
function _generateKey(instance, arg) {
    var name = instance.constructor.name;
    var obf = obfuscationMappings[name];
    return name + obf;
}
/**
 * Returns a string given the class and the key <arg>
 */
function getResource(instance, arg) {
    var key = _generateKey(instance, arg);
    return localStorage.getItem(key);
    ;
}
exports.getResource = getResource;
/**
 * Sets the requested key <arg> of class <instance> to <value>
 */
function setResource(instance, arg, value) {
    var key = _generateKey(instance, arg);
    localStorage.setItem(key, value);
}
exports.setResource = setResource;
var cookies = new Cookies();
function isBoardMember() {
    var ret = cookies.get('is_board_member');
    return ret == 'true';
}
exports.isBoardMember = isBoardMember;
function getMemberId() {
    var ret = cookies.get('member_id');
    return parseInt(ret);
}
exports.getMemberId = getMemberId;
function xsrfCookieName() {
    return "csrftoken";
}
exports.xsrfCookieName = xsrfCookieName;
function xsrfHeaderName() {
    return "X-CSRFToken";
}
exports.xsrfHeaderName = xsrfHeaderName;


/***/ }),

/***/ 37:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});

var _Cookies = __webpack_require__(38);

var _Cookies2 = _interopRequireDefault(_Cookies);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

exports.default = _Cookies2.default;
module.exports = exports['default'];

/***/ }),

/***/ 38:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});

var _typeof = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; };

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _cookie = __webpack_require__(39);

var _cookie2 = _interopRequireDefault(_cookie);

var _objectAssign = __webpack_require__(31);

var _objectAssign2 = _interopRequireDefault(_objectAssign);

var _utils = __webpack_require__(40);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var Cookies = function () {
  function Cookies(cookies, hooks) {
    _classCallCheck(this, Cookies);

    this.cookies = parseCookies(cookies);
    this.hooks = hooks;
    this.HAS_DOCUMENT_COOKIE = (0, _utils.hasDocumentCookie)();
  }

  _createClass(Cookies, [{
    key: '_updateBrowserValues',
    value: function _updateBrowserValues() {
      if (!this.HAS_DOCUMENT_COOKIE) {
        return;
      }

      this.cookies = _cookie2.default.parse(document.cookie);
    }
  }, {
    key: 'get',
    value: function get(name) {
      var options = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {};

      this._updateBrowserValues();
      return readCookie(this.cookies[name], options);
    }
  }, {
    key: 'getAll',
    value: function getAll() {
      var options = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};

      this._updateBrowserValues();
      var result = {};

      for (var name in this.cookies) {
        result[name] = readCookie(this.cookies[name], options);
      }

      return result;
    }
  }, {
    key: 'set',
    value: function set(name, value, options) {
      if ((typeof value === 'undefined' ? 'undefined' : _typeof(value)) === 'object') {
        value = JSON.stringify(value);
      }

      if (this.hooks && this.hooks.onSet) {
        this.hooks.onSet(name, value, options);
      }

      this.cookies[name] = value;

      if (this.HAS_DOCUMENT_COOKIE) {
        document.cookie = _cookie2.default.serialize(name, value, options);
      }
    }
  }, {
    key: 'remove',
    value: function remove(name, options) {
      var finalOptions = options = (0, _objectAssign2.default)({}, options, {
        expires: new Date(1970, 1, 1, 0, 0, 1),
        maxAge: 0
      });

      if (this.hooks && this.hooks.onRemove) {
        this.hooks.onRemove(name, finalOptions);
      }

      delete this.cookies[name];

      if (this.HAS_DOCUMENT_COOKIE) {
        document.cookie = _cookie2.default.serialize(name, '', finalOptions);
      }
    }
  }]);

  return Cookies;
}();

exports.default = Cookies;


function parseCookies(cookies) {
  if (typeof cookies === 'string') {
    return _cookie2.default.parse(cookies);
  } else if ((typeof cookies === 'undefined' ? 'undefined' : _typeof(cookies)) === 'object' && cookies !== null) {
    return cookies;
  } else {
    return {};
  }
}

function isParsingCookie(value, doNotParse) {
  if (typeof doNotParse === 'undefined') {
    // We guess if the cookie start with { or [, it has been serialized
    doNotParse = !value || value[0] !== '{' && value[0] !== '[' && value[0] !== '"';
  }

  return !doNotParse;
}

function readCookie(value) {
  var options = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {};

  if (isParsingCookie(value, options.doNotParse)) {
    try {
      return JSON.parse(value);
    } catch (e) {
      // At least we tried
    }
  }

  return value;
}
module.exports = exports['default'];

/***/ }),

/***/ 39:
/***/ (function(module, exports, __webpack_require__) {

"use strict";
/*!
 * cookie
 * Copyright(c) 2012-2014 Roman Shtylman
 * Copyright(c) 2015 Douglas Christopher Wilson
 * MIT Licensed
 */



/**
 * Module exports.
 * @public
 */

exports.parse = parse;
exports.serialize = serialize;

/**
 * Module variables.
 * @private
 */

var decode = decodeURIComponent;
var encode = encodeURIComponent;
var pairSplitRegExp = /; */;

/**
 * RegExp to match field-content in RFC 7230 sec 3.2
 *
 * field-content = field-vchar [ 1*( SP / HTAB ) field-vchar ]
 * field-vchar   = VCHAR / obs-text
 * obs-text      = %x80-FF
 */

var fieldContentRegExp = /^[\u0009\u0020-\u007e\u0080-\u00ff]+$/;

/**
 * Parse a cookie header.
 *
 * Parse the given cookie header string into an object
 * The object has the various cookies as keys(names) => values
 *
 * @param {string} str
 * @param {object} [options]
 * @return {object}
 * @public
 */

function parse(str, options) {
  if (typeof str !== 'string') {
    throw new TypeError('argument str must be a string');
  }

  var obj = {}
  var opt = options || {};
  var pairs = str.split(pairSplitRegExp);
  var dec = opt.decode || decode;

  for (var i = 0; i < pairs.length; i++) {
    var pair = pairs[i];
    var eq_idx = pair.indexOf('=');

    // skip things that don't look like key=value
    if (eq_idx < 0) {
      continue;
    }

    var key = pair.substr(0, eq_idx).trim()
    var val = pair.substr(++eq_idx, pair.length).trim();

    // quoted values
    if ('"' == val[0]) {
      val = val.slice(1, -1);
    }

    // only assign once
    if (undefined == obj[key]) {
      obj[key] = tryDecode(val, dec);
    }
  }

  return obj;
}

/**
 * Serialize data into a cookie header.
 *
 * Serialize the a name value pair into a cookie string suitable for
 * http headers. An optional options object specified cookie parameters.
 *
 * serialize('foo', 'bar', { httpOnly: true })
 *   => "foo=bar; httpOnly"
 *
 * @param {string} name
 * @param {string} val
 * @param {object} [options]
 * @return {string}
 * @public
 */

function serialize(name, val, options) {
  var opt = options || {};
  var enc = opt.encode || encode;

  if (typeof enc !== 'function') {
    throw new TypeError('option encode is invalid');
  }

  if (!fieldContentRegExp.test(name)) {
    throw new TypeError('argument name is invalid');
  }

  var value = enc(val);

  if (value && !fieldContentRegExp.test(value)) {
    throw new TypeError('argument val is invalid');
  }

  var str = name + '=' + value;

  if (null != opt.maxAge) {
    var maxAge = opt.maxAge - 0;
    if (isNaN(maxAge)) throw new Error('maxAge should be a Number');
    str += '; Max-Age=' + Math.floor(maxAge);
  }

  if (opt.domain) {
    if (!fieldContentRegExp.test(opt.domain)) {
      throw new TypeError('option domain is invalid');
    }

    str += '; Domain=' + opt.domain;
  }

  if (opt.path) {
    if (!fieldContentRegExp.test(opt.path)) {
      throw new TypeError('option path is invalid');
    }

    str += '; Path=' + opt.path;
  }

  if (opt.expires) {
    if (typeof opt.expires.toUTCString !== 'function') {
      throw new TypeError('option expires is invalid');
    }

    str += '; Expires=' + opt.expires.toUTCString();
  }

  if (opt.httpOnly) {
    str += '; HttpOnly';
  }

  if (opt.secure) {
    str += '; Secure';
  }

  if (opt.sameSite) {
    var sameSite = typeof opt.sameSite === 'string'
      ? opt.sameSite.toLowerCase() : opt.sameSite;

    switch (sameSite) {
      case true:
        str += '; SameSite=Strict';
        break;
      case 'lax':
        str += '; SameSite=Lax';
        break;
      case 'strict':
        str += '; SameSite=Strict';
        break;
      default:
        throw new TypeError('option sameSite is invalid');
    }
  }

  return str;
}

/**
 * Try decoding a string using a decoding function.
 *
 * @param {string} str
 * @param {function} decode
 * @private
 */

function tryDecode(str, decode) {
  try {
    return decode(str);
  } catch (e) {
    return str;
  }
}


/***/ }),

/***/ 4:
/***/ (function(module, exports, __webpack_require__) {

"use strict";
/* WEBPACK VAR INJECTION */(function(process) {

var utils = __webpack_require__(1);
var normalizeHeaderName = __webpack_require__(16);

var DEFAULT_CONTENT_TYPE = {
  'Content-Type': 'application/x-www-form-urlencoded'
};

function setContentTypeIfUnset(headers, value) {
  if (!utils.isUndefined(headers) && utils.isUndefined(headers['Content-Type'])) {
    headers['Content-Type'] = value;
  }
}

function getDefaultAdapter() {
  var adapter;
  if (typeof XMLHttpRequest !== 'undefined') {
    // For browsers use XHR adapter
    adapter = __webpack_require__(8);
  } else if (typeof process !== 'undefined') {
    // For node use HTTP adapter
    adapter = __webpack_require__(8);
  }
  return adapter;
}

var defaults = {
  adapter: getDefaultAdapter(),

  transformRequest: [function transformRequest(data, headers) {
    normalizeHeaderName(headers, 'Content-Type');
    if (utils.isFormData(data) ||
      utils.isArrayBuffer(data) ||
      utils.isBuffer(data) ||
      utils.isStream(data) ||
      utils.isFile(data) ||
      utils.isBlob(data)
    ) {
      return data;
    }
    if (utils.isArrayBufferView(data)) {
      return data.buffer;
    }
    if (utils.isURLSearchParams(data)) {
      setContentTypeIfUnset(headers, 'application/x-www-form-urlencoded;charset=utf-8');
      return data.toString();
    }
    if (utils.isObject(data)) {
      setContentTypeIfUnset(headers, 'application/json;charset=utf-8');
      return JSON.stringify(data);
    }
    return data;
  }],

  transformResponse: [function transformResponse(data) {
    /*eslint no-param-reassign:0*/
    if (typeof data === 'string') {
      try {
        data = JSON.parse(data);
      } catch (e) { /* Ignore */ }
    }
    return data;
  }],

  /**
   * A timeout in milliseconds to abort a request. If set to 0 (default) a
   * timeout is not created.
   */
  timeout: 0,

  xsrfCookieName: 'XSRF-TOKEN',
  xsrfHeaderName: 'X-XSRF-TOKEN',

  maxContentLength: -1,

  validateStatus: function validateStatus(status) {
    return status >= 200 && status < 300;
  }
};

defaults.headers = {
  common: {
    'Accept': 'application/json, text/plain, */*'
  }
};

utils.forEach(['delete', 'get', 'head'], function forEachMethodNoData(method) {
  defaults.headers[method] = {};
});

utils.forEach(['post', 'put', 'patch'], function forEachMethodWithData(method) {
  defaults.headers[method] = utils.merge(DEFAULT_CONTENT_TYPE);
});

module.exports = defaults;

/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(3)))

/***/ }),

/***/ 40:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});

var _typeof = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; };

exports.hasDocumentCookie = hasDocumentCookie;
exports.cleanCookies = cleanCookies;
// Can we get/set cookies on document.cookie?

function hasDocumentCookie() {
  return (typeof document === 'undefined' ? 'undefined' : _typeof(document)) === 'object' && typeof document.cookie === 'string';
}

//backwards compatibility
var HAS_DOCUMENT_COOKIE = exports.HAS_DOCUMENT_COOKIE = hasDocumentCookie();

function cleanCookies() {
  document.cookie.split(';').forEach(function (c) {
    document.cookie = c.replace(/^ +/, '').replace(/=.*/, '=;expires=' + new Date().toUTCString() + ';path=/');
  });
}

/***/ }),

/***/ 44:
/***/ (function(module, exports, __webpack_require__) {

"use strict";

Object.defineProperty(exports, "__esModule", { value: true });
function objectToFormData(obj) {
    var data = new FormData();
    for (var _i = 0, _a = Object.keys(obj); _i < _a.length; _i++) {
        var key = _a[_i];
        var serial = obj[key];
        if (typeof serial === 'object') {
            serial = JSON.stringify(obj[key]);
        }
        data.append(key, serial);
    }
    return data;
}
exports.objectToFormData = objectToFormData;


/***/ }),

/***/ 49:
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __extends = (this && this.__extends) || (function () {
    var extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
var React = __webpack_require__(2);
var Option = /** @class */ (function () {
    function Option(val, displ) {
        this.value = val;
        this.display = displ;
    }
    return Option;
}());
exports.Option = Option;
var selectFadeOutClassName = 'select-check-fade-out';
var SelectArea = /** @class */ (function (_super) {
    __extends(SelectArea, _super);
    function SelectArea() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SelectArea.prototype.render = function () {
        var _this = this;
        return React.createElement("span", { className: 'select' }, this.props.options.map(function (option, idx) {
            return React.createElement(React.Fragment, null,
                React.createElement("input", { className: 'select-hidden', key: idx, id: _this.props.name + idx, value: option.value, name: _this.props.name, type: 'radio', onChange: function (target) { return _this.props.change(option.value, _this.props.name + idx); } }),
                React.createElement("label", { className: "select-label", key: idx * -1 - 1, htmlFor: _this.props.name + idx }, option.display));
        }));
    };
    return SelectArea;
}(React.Component));
var Select = /** @class */ (function (_super) {
    __extends(Select, _super);
    function Select(props) {
        var _this = _super.call(this, props) || this;
        _this.change = _this.change.bind(_this);
        _this.handleClickOutside = _this.handleClickOutside.bind(_this);
        _this.lazyAnimationAdder = _this.lazyAnimationAdder.bind(_this);
        _this._decideInitialStatus = _this._decideInitialStatus.bind(_this);
        _this._scrollCondition = _this._scrollCondition.bind(_this);
        _this.documentResizeUpdate = _this.documentResizeUpdate.bind(_this);
        var status = _this._decideInitialStatus();
        var value = _this.props.defaultValue !== undefined ? _this.props.defaultValue : _this.props.options[0].value;
        _this.state = {
            status: status,
            width: document.documentElement.clientWidth,
            value: value,
        };
        _this.scrollDiv = null;
        return _this;
    }
    Select.prototype._scrollCondition = function () {
        return this.state.width < 500 || this.props.override;
    };
    Select.prototype._decideInitialStatus = function () {
        var _this = this;
        if (this.props.defaultValue !== undefined) {
            var value = this.props.options.find(function (option) {
                return option.value === _this.props.defaultValue;
            });
            if (value === undefined) {
                return this.props.options[0].display;
            }
            else {
                return value.display;
            }
        }
        else {
            return this.props.options[0].display;
        }
    };
    Select.prototype.documentResizeUpdate = function () {
        this.setState({
            width: document.documentElement.clientWidth
        });
    };
    Select.prototype.componentDidMount = function () {
        var _this = this;
        if (this._scrollCondition()) {
            return;
        }
        document.documentElement.addEventListener('resize', this.documentResizeUpdate);
        document.addEventListener('mousedown', this.handleClickOutside);
        var defaultHeight = 30;
        this.scrollDiv.style.height = defaultHeight + "px";
        this.interval = setInterval(function () {
            var movableArea = _this.innerDiv.scrollTop /
                (_this.innerDiv.scrollHeight - _this.innerDiv.clientHeight);
            var offset = _this.innerDiv.scrollTop * (1 + movableArea) + 2;
            _this.scrollDiv.style.top = "" + offset + "px";
        }, 20);
        var divMove = function (e) {
            var boundingRect = _this.selectDiv.getBoundingClientRect();
            var fuzz = .2;
            var height = boundingRect.bottom - boundingRect.top;
            var bottom = boundingRect.bottom - fuzz * height;
            var top = boundingRect.top + fuzz * height;
            var adjusted = Math.max(Math.min(e.clientY, bottom), top);
            var percentage = (adjusted - top) / (bottom - top);
            _this.innerDiv.scrollTop = percentage * (_this.innerDiv.scrollHeight - _this.innerDiv.clientHeight);
        };
        function mouseUp() {
            window.removeEventListener('mousemove', divMove, true);
        }
        function mouseDown() {
            window.addEventListener('mousemove', divMove, true);
        }
        this.scrollDiv.addEventListener('mousedown', mouseDown, false);
        window.addEventListener('mouseup', mouseUp, false);
    };
    Select.prototype.componentWillUnmount = function () {
        if (this._scrollCondition()) {
            return;
        }
        document.removeEventListener('mousedown', this.handleClickOutside);
        document.documentElement.removeEventListener('resize', this.documentResizeUpdate);
        clearInterval(this.interval);
    };
    /**
     * Uncheck the input if clicked outside
     * Best to leave the typing generic because typescript does _not_
     * like non-generics with dom.
     */
    Select.prototype.handleClickOutside = function (event) {
        if (this._scrollCondition()) {
            return;
        }
        if (this.inputDiv && !this.wrapper.contains(event.target)) {
            this.inputDiv.checked = false;
        }
    };
    Select.prototype.lazyAnimationAdder = function (event) {
        if (this._scrollCondition()) {
            return;
        }
        if (this.inputDiv.checked && !this.selectDiv.classList.contains(selectFadeOutClassName)) {
            this.selectDiv.classList.add(selectFadeOutClassName);
        }
    };
    Select.prototype.change = function (value, id) {
        if (this.props.onChange) {
            this.props.onChange(value);
        }
        this.setState({
            value: value,
        });
        if (this._scrollCondition()) {
            return;
        }
        else {
            // Cool trick to get the label for the input
            var elem = document.querySelector('label[for="' + id + '"]');
            this.setState({
                status: elem.innerHTML,
            });
            this.inputDiv.checked = false;
        }
    };
    Select.prototype.render = function () {
        var _this = this;
        if (this._scrollCondition()) {
            return React.createElement("select", { className: "interaction-style", value: this.state.value, onChange: function (ev) { return _this.change(ev.target.value, null); } }, this.props.options.map(function (option, idx) {
                return React.createElement(React.Fragment, null,
                    React.createElement("option", { value: option.value }, option.display));
            }));
        }
        return React.createElement("div", { className: "select-wrapper-div", ref: function (input) { return _this.wrapper = input; } },
            React.createElement("input", { className: 'select-hidden select-check-toggle', id: this.props.name + "-toggle", name: this.props.name, onChange: this.lazyAnimationAdder, type: 'checkbox', ref: function (input) { return _this.inputDiv = input; } }),
            React.createElement("label", { className: 'select-label select-toggle', htmlFor: this.props.name + "-toggle" },
                React.createElement("span", { ref: function (input) { return _this.titleSpan = input; }, className: "select-title-text" }, this.state.status),
                React.createElement("b", { className: 'select-arrow' })),
            React.createElement("div", { className: "select-div", ref: function (input) { return _this.selectDiv = input; } },
                React.createElement("div", { className: "inner-select-div", ref: function (input) { return _this.innerDiv = input; } },
                    React.createElement(SelectArea, { options: this.props.options, name: this.props.name, change: this.change }),
                    React.createElement("div", { className: "select-scroll", ref: function (input) { return _this.scrollDiv = input; } }))));
    };
    return Select;
}(React.Component));
exports.Select = Select;


/***/ }),

/***/ 498:
/***/ (function(module, exports, __webpack_require__) {

"use strict";

Object.defineProperty(exports, "__esModule", { value: true });
var React = __webpack_require__(2);
var ReactDOM = __webpack_require__(5);
var TournamentView_1 = __webpack_require__(499);
ReactDOM.render(React.createElement(TournamentView_1.TournamentView, null), document.querySelector("tournament-view"));


/***/ }),

/***/ 499:
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __extends = (this && this.__extends) || (function () {
    var extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
var __assign = (this && this.__assign) || Object.assign || function(t) {
    for (var s, i = 1, n = arguments.length; i < n; i++) {
        s = arguments[i];
        for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
            t[p] = s[p];
    }
    return t;
};
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = y[op[0] & 2 ? "return" : op[0] ? "throw" : "next"]) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [0, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
var __rest = (this && this.__rest) || function (s, e) {
    var t = {};
    for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p) && e.indexOf(p) < 0)
        t[p] = s[p];
    if (s != null && typeof Object.getOwnPropertySymbols === "function")
        for (var i = 0, p = Object.getOwnPropertySymbols(s); i < p.length; i++) if (e.indexOf(p[i]) < 0)
            t[p[i]] = s[p[i]];
    return t;
};
Object.defineProperty(exports, "__esModule", { value: true });
var React = __webpack_require__(2);
var axios_1 = __webpack_require__(12);
var Select_1 = __webpack_require__(49);
var Utils_1 = __webpack_require__(44);
var Popup_1 = __webpack_require__(50);
var LocalResourceResolver_1 = __webpack_require__(33);
var RadioButton_1 = __webpack_require__(213);
axios_1.default.defaults.xsrfCookieName = LocalResourceResolver_1.xsrfCookieName();
axios_1.default.defaults.xsrfHeaderName = LocalResourceResolver_1.xsrfHeaderName();
//axios.post('/api/tournament/members/register', objectToFormData({member_id: 2})).catch((err: any) => console.log(err));
var tourney_url = '/api/tournament/';
var columnWidth = 160;
var rowHeight = 40;
var rowSpacing = 10;
var colSpacing = 50;
var lazyHack = 10000000;
var svgOffset = 20;
var calcX = function (col) { return (columnWidth + colSpacing) * col + svgOffset; };
var calcY = function (col, row, maxCols) {
    if (col === 0) {
        return (rowHeight + rowSpacing) * row + col * ((rowHeight + rowSpacing) / 2) + svgOffset;
    }
    var numBlocksCenter = Math.pow(2, col);
    var ytop = calcY(0, row * numBlocksCenter, maxCols);
    var ybot = calcY(0, (row + 1) * numBlocksCenter - 1, maxCols) + rowHeight;
    return (ytop + ybot - rowHeight) / 2;
};
var Matchup = /** @class */ (function (_super) {
    __extends(Matchup, _super);
    function Matchup() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Matchup.prototype.unpackMatch = function (matches) {
        var match = matches[0];
        var decide = function (team) {
            if (team.length == 2) {
                return team[0].first_name + ' & ' + team[1].first_name;
            }
            else if (team.length == 1) {
                return team[0].first_name + ' ' + team[0].last_name;
            }
            else {
                return 'None';
            }
        };
        var team1 = decide(match.team_A);
        var team2 = decide(match.team_B);
        return [match, team1, team2];
    };
    Matchup.prototype.render = function () {
        var _this = this;
        var extra;
        var startingX = this.props.x;
        var startingY = this.props.y + 15;
        var textStyle = {
            fill: 'white',
            stroke: 'white',
            strokeWidth: 1.5,
        };
        if (this.props.data.matches.length === 0) {
            extra = React.createElement("text", { x: startingX, y: startingY, height: rowHeight, width: columnWidth }, "TBA");
        }
        else if (this.props.data.endDateTime === null) {
            var _a = this.unpackMatch(this.props.data.matches), match = _a[0], team1 = _a[1], team2 = _a[2];
            extra = React.createElement(React.Fragment, null,
                React.createElement("text", { x: startingX, y: startingY, style: textStyle }, team1),
                React.createElement("text", { x: startingX, y: startingY + rowHeight / 2, style: textStyle }, team2));
        }
        else {
            var _b = this.unpackMatch(this.props.data.matches), match = _b[0], team1 = _b[1], team2 = _b[2];
            var convert = function (num) {
                if (num < 10) {
                    return "0" + num;
                }
                return "" + num;
            };
            extra = React.createElement(React.Fragment, null,
                React.createElement("text", { x: startingX, y: startingY, style: textStyle }, team1),
                React.createElement("text", { x: startingX, y: startingY + rowHeight / 2, style: textStyle }, team2),
                React.createElement("text", { x: startingX + columnWidth - 25, y: startingY, style: textStyle }, match.scoreA),
                React.createElement("text", { x: startingX + columnWidth - 25, y: startingY + rowHeight / 2, style: textStyle }, match.scoreB));
        }
        var rectStyle = {
            fill: 'black',
            stroke: 'black',
            strokeWidth: 5,
        };
        return (React.createElement(React.Fragment, null,
            React.createElement("rect", { x: this.props.x, y: this.props.y, width: columnWidth, height: rowHeight, style: rectStyle, className: "tournament-bracket-node", rx: "" + 3, ry: "" + 3, onClick: function () { return _this.props.change(_this.props.data); } }),
            extra));
    };
    return Matchup;
}(React.Component));
function height(matchups) {
    if (matchups === null || Object.keys(matchups).length === 0) {
        return 0;
    }
    var hgt = Math.max(height(matchups.left_node), height(matchups.right_node)) + 1;
    return hgt;
}
var TournamentCell = /** @class */ (function (_super) {
    __extends(TournamentCell, _super);
    function TournamentCell(props) {
        var _this = _super.call(this, props) || this;
        _this.agglomerateData = _this.agglomerateData.bind(_this);
        _this._merge = _this._merge.bind(_this);
        return _this;
    }
    TournamentCell.prototype._merge = function (aggCall, toX, toY) {
        if (aggCall.length === 0) {
            return [];
        }
        var othElems = aggCall[0], _a = aggCall[1], othX = _a[0], othY = _a[1];
        var offsetX = 6;
        var midX = othX + columnWidth + offsetX;
        var midY = othY + rowHeight / 2;
        var halfX = midX + colSpacing / 2;
        var offsetY = 9;
        if (toY < midY) {
            toY += offsetY;
        }
        else {
            toY -= offsetY;
        }
        var lineOpts = {
            stroke: "black",
            strokeWidth: 1.5,
        };
        return [React.createElement("line", __assign({}, lineOpts, { x1: "" + midX, y1: "" + midY, x2: "" + halfX, y2: "" + midY })),
            React.createElement("line", __assign({}, lineOpts, { x1: "" + halfX, y1: "" + midY, x2: "" + halfX, y2: "" + toY })),
            React.createElement("line", __assign({}, lineOpts, { x1: "" + halfX, y1: "" + toY, x2: "" + (toX - offsetX), y2: "" + toY }))].concat(othElems);
    };
    TournamentCell.prototype.agglomerateData = function (data, row, col, maxCols) {
        //elements, root
        if (data === null || Object.keys(data).length === 0) {
            return [];
        }
        var left_node = data.left_node, right_node = data.right_node, rest = __rest(data, ["left_node", "right_node"]);
        var x = calcX(col);
        var y = calcY(col, row, maxCols);
        var elems = [React.createElement(Matchup, { x: x, y: y, data: rest, change: this.props.change })];
        var entry = y + rowHeight / 2;
        if (data.left_node !== null) {
            var accumulated = this._merge(this.agglomerateData(data.left_node, row * 2, col - 1, maxCols), x, entry);
            elems = elems.concat(accumulated);
        }
        if (data.right_node !== null) {
            var accumulated = this._merge(this.agglomerateData(data.right_node, row * 2 + 1, col - 1, maxCols), x, entry);
            elems = elems.concat(accumulated);
        }
        return [elems, [x, y]];
    };
    TournamentCell.prototype.render = function () {
        console.log(this.props.matches);
        var maxHeight = height(this.props.matches);
        var _a = this.agglomerateData(this.props.matches, 0, maxHeight - 1, maxHeight), elems = _a[0], rest = _a.slice(1);
        return React.createElement("svg", { width: "" + window.innerWidth, height: "" + window.innerHeight },
            React.createElement("g", null, elems));
    };
    return TournamentCell;
}(React.Component));
var TournamentDown = /** @class */ (function (_super) {
    __extends(TournamentDown, _super);
    function TournamentDown(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            players: "",
            type: 'Doubles'
        };
        _this.onSubmit = _this.onSubmit.bind(_this);
        return _this;
    }
    TournamentDown.prototype.onSubmit = function (ev) {
        var data = {
            num_players: this.state.players,
            tournament_type: this.state.type,
        };
        axios_1.default.post('/api/tournament/create', Utils_1.objectToFormData(data))
            .then(function (res) {
            console.log(res);
        })
            .catch(function (res) {
            console.log(res);
        });
        ev.preventDefault();
    };
    TournamentDown.prototype.render = function () {
        var _this = this;
        var opts = [
            new Select_1.Option('Doubles', 'Doubles'),
            new Select_1.Option('Singles', 'Singles'),
        ];
        return React.createElement("form", { onSubmit: this.onSubmit },
            React.createElement("div", { className: "row" },
                React.createElement("div", { className: "col-6" },
                    React.createElement("input", { type: "text", className: "interaction-style", placeholder: "Number of players", value: this.state.players, onChange: function (ev) { return _this.setState({ players: ev.target.value }); } })),
                React.createElement("div", { className: "col-6" },
                    React.createElement(Select_1.Select, { onChange: function (val) { return _this.setState({ type: val }); }, options: opts, name: "emailName", defaultValue: this.state.type }))),
            React.createElement("button", { type: "submit", className: "interaction-style" }, "Submit"));
    };
    return TournamentDown;
}(React.Component));
var convertToDicts = function (matches) {
    var _convertToDicts = function (matches, idx) {
        if (idx > matches.length) {
            return null;
        }
        var lhs = _convertToDicts(matches, idx * 2);
        var rhs = _convertToDicts(matches, idx * 2 + 1);
        var node = matches[idx - 1];
        return { left_node: lhs, right_node: rhs, id: node.bracket_node_id, matches: node.matches };
    };
    return _convertToDicts(matches, 1);
};
var TournamentView = /** @class */ (function (_super) {
    __extends(TournamentView, _super);
    function TournamentView(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            status: null,
            matches: null,
        };
        _this.refresh = _this.refresh.bind(_this);
        _this.finishTournament = _this.finishTournament.bind(_this);
        _this.changeMatch = _this.changeMatch.bind(_this);
        _this.joinTournament = _this.joinTournament.bind(_this);
        _this.leaveTournament = _this.leaveTournament.bind(_this);
        return _this;
    }
    TournamentView.prototype.finishTournament = function () {
        return __awaiter(this, void 0, void 0, function () {
            var data, res, err_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        _a.trys.push([0, 2, , 3]);
                        data = {
                            tournament_id: this.state.id,
                        };
                        return [4 /*yield*/, axios_1.default.post(tourney_url + 'finish/', Utils_1.objectToFormData(data))];
                    case 1:
                        res = _a.sent();
                        console.log(res);
                        this.refresh();
                        return [3 /*break*/, 3];
                    case 2:
                        err_1 = _a.sent();
                        console.log(err_1);
                        return [3 /*break*/, 3];
                    case 3: return [2 /*return*/];
                }
            });
        });
    };
    TournamentView.prototype.refresh = function () {
        return __awaiter(this, void 0, void 0, function () {
            var res, data, members, brackets, err_2;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        _a.trys.push([0, 5, , 6]);
                        return [4 /*yield*/, axios_1.default.get(tourney_url)];
                    case 1:
                        res = [_a.sent()][0];
                        data = res.data;
                        if (!(data.status === "down")) return [3 /*break*/, 2];
                        this.setState({
                            status: data.status,
                            matches: res.data,
                        });
                        return [3 /*break*/, 4];
                    case 2: return [4 /*yield*/, axios_1.default.get('/api/tournament/members/get/')];
                    case 3:
                        members = _a.sent();
                        brackets = convertToDicts(data.tournament.bracket_nodes);
                        this.setState({
                            status: data.status,
                            matches: brackets,
                            members: members.data.tournament_members,
                            id: data.tournament.tournament_id,
                        });
                        _a.label = 4;
                    case 4: return [3 /*break*/, 6];
                    case 5:
                        err_2 = _a.sent();
                        console.log(err_2);
                        return [3 /*break*/, 6];
                    case 6: return [2 /*return*/];
                }
            });
        });
    };
    TournamentView.prototype.joinTournament = function () {
        return __awaiter(this, void 0, void 0, function () {
            var res, err_3;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        _a.trys.push([0, 2, , 3]);
                        return [4 /*yield*/, axios_1.default.post('/api/tournament/members/register', Utils_1.objectToFormData({ member_id: LocalResourceResolver_1.getMemberId() }))];
                    case 1:
                        res = _a.sent();
                        console.log(res);
                        this.refresh();
                        return [3 /*break*/, 3];
                    case 2:
                        err_3 = _a.sent();
                        console.log(err_3);
                        return [3 /*break*/, 3];
                    case 3: return [2 /*return*/];
                }
            });
        });
    };
    TournamentView.prototype.leaveTournament = function () {
        return __awaiter(this, void 0, void 0, function () {
            var res, err_4;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        _a.trys.push([0, 2, , 3]);
                        return [4 /*yield*/, axios_1.default.post('/api/tournament/members/unregister', Utils_1.objectToFormData({ member_id: LocalResourceResolver_1.getMemberId() }))];
                    case 1:
                        res = _a.sent();
                        console.log(res);
                        this.refresh();
                        return [3 /*break*/, 3];
                    case 2:
                        err_4 = _a.sent();
                        console.log(err_4);
                        return [3 /*break*/, 3];
                    case 3: return [2 /*return*/];
                }
            });
        });
    };
    TournamentView.prototype.changeMatch = function (matchObj) {
        var _this = this;
        var reset = function () { return _this.setState({ popup: null }); };
        var popup = null;
        console.log(matchObj.matches);
        if (matchObj.matches.length === 0) {
            // Unassigned case
            var team_1 = { teamA: new Set(), teamB: new Set() };
            var callback = function () { return __awaiter(_this, void 0, void 0, function () {
                var _a, team_A, team_B, data, res;
                return __generator(this, function (_b) {
                    switch (_b.label) {
                        case 0:
                            _b.trys.push([0, , 2, 3]);
                            _a = [team_1.teamA, team_1.teamB].map(function (e) { return Array.from(e); }), team_A = _a[0], team_B = _a[1];
                            if (team_A.length === 0 || team_A.length > 2
                                || team_B.length === 0 || team_B.length > 2) {
                                return [2 /*return*/];
                            }
                            data = {
                                bracket_node_id: matchObj.id,
                                team_A: team_A.join(','),
                                team_B: team_B.join(','),
                            };
                            return [4 /*yield*/, axios_1.default.post('/api/tournament/add/match/', Utils_1.objectToFormData(data))];
                        case 1:
                            res = _b.sent();
                            console.log(res);
                            return [3 /*break*/, 3];
                        case 2:
                            reset();
                            this.refresh();
                            return [7 /*endfinally*/];
                        case 3: return [2 /*return*/];
                    }
                });
            }); };
            popup = React.createElement(Popup_1.Popup, { title: "Assign Teams", callback: callback },
                React.createElement("div", { style: { height: "100%", overflowY: "scroll" } },
                    React.createElement("div", { className: "row" },
                        React.createElement("div", { className: "col-9" }, "Member"),
                        React.createElement("div", { className: "col-1" }),
                        React.createElement("div", { className: "col-1" }, "A"),
                        React.createElement("div", { className: "col-1" }, "B")),
                    this.state.members.map(function (member, idx) {
                        return React.createElement("div", { className: "row", key: idx },
                            React.createElement("div", { className: "col-9" },
                                member.first_name,
                                " ",
                                member.last_name),
                            React.createElement("div", { className: "col-1" },
                                React.createElement(RadioButton_1.RadioButton, { defaultChecked: true, name: "" + idx, onChange: function (ev) {
                                        if (!ev.target.checked)
                                            return;
                                        team_1.teamA.delete(member.member_id);
                                        team_1.teamB.delete(member.member_id);
                                    } })),
                            React.createElement("div", { className: "col-1" },
                                React.createElement(RadioButton_1.RadioButton, { defaultChecked: false, name: "" + idx, onChange: function (ev) {
                                        if (!ev.target.checked)
                                            return;
                                        team_1.teamA.add(member.member_id);
                                        team_1.teamB.delete(member.member_id);
                                    } })),
                            React.createElement("div", { className: "col-1" },
                                React.createElement(RadioButton_1.RadioButton, { defaultChecked: false, name: "" + idx, onChange: function (ev) {
                                        if (!ev.target.checked)
                                            return;
                                        team_1.teamA.delete(member.member_id);
                                        team_1.teamB.add(member.member_id);
                                    } })));
                    })));
        }
        else if (matchObj.matches[0].endDateTime === null) {
            var match_1 = matchObj.matches[0];
            var teamA = "Team A: " + match_1.team_A.map(function (e) { return e.first_name; }).join(',');
            var teamB = "Team B: " + match_1.team_B.map(function (e) { return e.first_name; }).join(',');
            var score_1 = { aScore: 0, bScore: 0 };
            var onFinish = function () { return __awaiter(_this, void 0, void 0, function () {
                var data, res, err_5;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            _a.trys.push([0, 2, 3, 4]);
                            console.log(score_1);
                            data = { match_id: match_1.match_id, scoreA: score_1.aScore, scoreB: score_1.bScore };
                            return [4 /*yield*/, axios_1.default.post('/api/match/finish/', Utils_1.objectToFormData(data))];
                        case 1:
                            res = _a.sent();
                            console.log(res);
                            return [3 /*break*/, 4];
                        case 2:
                            err_5 = _a.sent();
                            console.log(err_5);
                            return [3 /*break*/, 4];
                        case 3:
                            reset();
                            this.refresh();
                            return [7 /*endfinally*/];
                        case 4: return [2 /*return*/];
                    }
                });
            }); };
            popup = React.createElement(Popup_1.Popup, { title: "Finish Match", callback: onFinish },
                React.createElement("div", { className: "row" },
                    React.createElement("div", { className: "col-6" }, "Team"),
                    React.createElement("div", { className: "col-6" }, "Score")),
                React.createElement("div", { className: "row" },
                    React.createElement("div", { className: "col-6" }, teamA),
                    React.createElement("div", { className: "col-6" },
                        React.createElement("input", { className: "interaction-style", onChange: function (e) { score_1.aScore = e.target.value; } }))),
                React.createElement("div", { className: "row" },
                    React.createElement("div", { className: "col-6" }, teamB),
                    React.createElement("div", { className: "col-6" },
                        React.createElement("input", { className: "interaction-style", onChange: function (e) { score_1.bScore = e.target.value; } }))));
        }
        this.setState({ popup: popup });
    };
    TournamentView.prototype.componentDidMount = function () {
        this.refresh();
    };
    TournamentView.prototype.render = function () {
        if (this.state.status === null) {
            return null;
        }
        if (this.state.status === "down") {
            return React.createElement(TournamentDown, { refresh: this.refresh });
        }
        return (React.createElement("div", { className: "tournament-div" },
            this.state.popup && this.state.popup,
            React.createElement(TournamentCell, { matches: this.state.matches, change: this.changeMatch }),
            React.createElement("div", { className: "row" },
                React.createElement("div", { className: "col-6" },
                    React.createElement("button", { onClick: this.finishTournament, className: "interaction-style" }, "Finish")),
                this.state.members.find(function (e) { return e.member_id == LocalResourceResolver_1.getMemberId(); }) === undefined ?
                    React.createElement("div", { className: "col-6" },
                        React.createElement("button", { onClick: this.joinTournament, className: "interaction-style" }, "Join")) : React.createElement("div", { className: "col-6" },
                    React.createElement("button", { onClick: this.leaveTournament, className: "interaction-style" }, "Leave")))));
    };
    return TournamentView;
}(React.Component));
exports.TournamentView = TournamentView;


/***/ }),

/***/ 5:
/***/ (function(module, exports) {

module.exports = ReactDOM;

/***/ }),

/***/ 50:
/***/ (function(module, exports, __webpack_require__) {

"use strict";

/**
 * Contains a popup view that need only to be rendered
 * To work. Appears in the middle of the screen and darkens
 * The body.
 */
var __extends = (this && this.__extends) || (function () {
    var extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
var React = __webpack_require__(2);
var popupDisabledClass = "popup-disabled";
var popupScreenFadeClass = 'popup-screen-fade';
var popupFadeClass = 'popup-fade';
var PopupProps = /** @class */ (function () {
    function PopupProps() {
    }
    return PopupProps;
}());
exports.PopupProps = PopupProps;
var PopupState = /** @class */ (function () {
    function PopupState() {
    }
    return PopupState;
}());
var Popup = /** @class */ (function (_super) {
    __extends(Popup, _super);
    function Popup(props) {
        var _this = _super.call(this, props) || this;
        _this.close = _this.close.bind(_this);
        return _this;
    }
    Popup.prototype.componentDidMount = function () {
        /* Programatically create a div to overlay everything and animate it in
            Also force the body not to scroll */
        this.screenDiv = document.createElement('div');
        this.screenDiv.className = 'popup-screen';
        var body = document.querySelector('body');
        body.appendChild(this.screenDiv);
        body.classList.add(popupDisabledClass);
    };
    Popup.prototype.componentWillUnmount = function () {
        /* Remove the programatic div and let the body scroll */
        var body = document.querySelector('body');
        body.removeChild(this.screenDiv);
        body.classList.remove(popupDisabledClass);
    };
    Popup.prototype.close = function () {
        /* Animate everything in */
        var _this = this;
        this.wrapperDiv.classList.add(popupFadeClass);
        this.screenDiv.classList.add(popupScreenFadeClass);
        /* Cool so we can seperate concerns */
        var refCounter = { count: 0 };
        var callback = function () {
            if (refCounter.count == 1) {
                _this.props.callback();
            }
            else {
                refCounter.count += 1;
            }
        };
        /*
         * Since there are two animations going on we want to wait
         * for both of them to end. So we use a reference counter
         * in the form of a bound object.
         */
        this.wrapperDiv.addEventListener('animationend', callback);
        this.screenDiv.addEventListener('animationend', callback);
    };
    Popup.prototype.render = function () {
        var _this = this;
        return (React.createElement("div", { className: "popup-div", ref: function (input) { return _this.wrapperDiv = input; } },
            React.createElement("div", { className: "grid row" },
                React.createElement("div", { className: "row-1" },
                    React.createElement("div", { className: "col-11 popup-title-div" },
                        React.createElement("h4", { className: "popup-title" }, this.props.title))),
                React.createElement("div", { className: "row-1" },
                    React.createElement("div", { className: "col-offset-1 col-11" },
                        React.createElement("p", { className: "popup-message" }, this.props.message),
                        this.props.children)),
                React.createElement("div", { className: "row-offset-10" },
                    React.createElement("div", { className: "popup-check-button" },
                        React.createElement("button", { className: "popup-button interaction-style row-2", onClick: this.close }, "\u2714"))))));
    };
    return Popup;
}(React.Component));
exports.Popup = Popup;


/***/ }),

/***/ 7:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


module.exports = function bind(fn, thisArg) {
  return function wrap() {
    var args = new Array(arguments.length);
    for (var i = 0; i < args.length; i++) {
      args[i] = arguments[i];
    }
    return fn.apply(thisArg, args);
  };
};


/***/ }),

/***/ 8:
/***/ (function(module, exports, __webpack_require__) {

"use strict";
/* WEBPACK VAR INJECTION */(function(process) {

var utils = __webpack_require__(1);
var settle = __webpack_require__(17);
var buildURL = __webpack_require__(19);
var parseHeaders = __webpack_require__(20);
var isURLSameOrigin = __webpack_require__(21);
var createError = __webpack_require__(9);
var btoa = (typeof window !== 'undefined' && window.btoa && window.btoa.bind(window)) || __webpack_require__(22);

module.exports = function xhrAdapter(config) {
  return new Promise(function dispatchXhrRequest(resolve, reject) {
    var requestData = config.data;
    var requestHeaders = config.headers;

    if (utils.isFormData(requestData)) {
      delete requestHeaders['Content-Type']; // Let the browser set it
    }

    var request = new XMLHttpRequest();
    var loadEvent = 'onreadystatechange';
    var xDomain = false;

    // For IE 8/9 CORS support
    // Only supports POST and GET calls and doesn't returns the response headers.
    // DON'T do this for testing b/c XMLHttpRequest is mocked, not XDomainRequest.
    if (process.env.NODE_ENV !== 'test' &&
        typeof window !== 'undefined' &&
        window.XDomainRequest && !('withCredentials' in request) &&
        !isURLSameOrigin(config.url)) {
      request = new window.XDomainRequest();
      loadEvent = 'onload';
      xDomain = true;
      request.onprogress = function handleProgress() {};
      request.ontimeout = function handleTimeout() {};
    }

    // HTTP basic authentication
    if (config.auth) {
      var username = config.auth.username || '';
      var password = config.auth.password || '';
      requestHeaders.Authorization = 'Basic ' + btoa(username + ':' + password);
    }

    request.open(config.method.toUpperCase(), buildURL(config.url, config.params, config.paramsSerializer), true);

    // Set the request timeout in MS
    request.timeout = config.timeout;

    // Listen for ready state
    request[loadEvent] = function handleLoad() {
      if (!request || (request.readyState !== 4 && !xDomain)) {
        return;
      }

      // The request errored out and we didn't get a response, this will be
      // handled by onerror instead
      // With one exception: request that using file: protocol, most browsers
      // will return status as 0 even though it's a successful request
      if (request.status === 0 && !(request.responseURL && request.responseURL.indexOf('file:') === 0)) {
        return;
      }

      // Prepare the response
      var responseHeaders = 'getAllResponseHeaders' in request ? parseHeaders(request.getAllResponseHeaders()) : null;
      var responseData = !config.responseType || config.responseType === 'text' ? request.responseText : request.response;
      var response = {
        data: responseData,
        // IE sends 1223 instead of 204 (https://github.com/axios/axios/issues/201)
        status: request.status === 1223 ? 204 : request.status,
        statusText: request.status === 1223 ? 'No Content' : request.statusText,
        headers: responseHeaders,
        config: config,
        request: request
      };

      settle(resolve, reject, response);

      // Clean up request
      request = null;
    };

    // Handle low level network errors
    request.onerror = function handleError() {
      // Real errors are hidden from us by the browser
      // onerror should only fire if it's a network error
      reject(createError('Network Error', config, null, request));

      // Clean up request
      request = null;
    };

    // Handle timeout
    request.ontimeout = function handleTimeout() {
      reject(createError('timeout of ' + config.timeout + 'ms exceeded', config, 'ECONNABORTED',
        request));

      // Clean up request
      request = null;
    };

    // Add xsrf header
    // This is only done if running in a standard browser environment.
    // Specifically not if we're in a web worker, or react-native.
    if (utils.isStandardBrowserEnv()) {
      var cookies = __webpack_require__(23);

      // Add xsrf header
      var xsrfValue = (config.withCredentials || isURLSameOrigin(config.url)) && config.xsrfCookieName ?
          cookies.read(config.xsrfCookieName) :
          undefined;

      if (xsrfValue) {
        requestHeaders[config.xsrfHeaderName] = xsrfValue;
      }
    }

    // Add headers to the request
    if ('setRequestHeader' in request) {
      utils.forEach(requestHeaders, function setRequestHeader(val, key) {
        if (typeof requestData === 'undefined' && key.toLowerCase() === 'content-type') {
          // Remove Content-Type if data is undefined
          delete requestHeaders[key];
        } else {
          // Otherwise add header to the request
          request.setRequestHeader(key, val);
        }
      });
    }

    // Add withCredentials to request if needed
    if (config.withCredentials) {
      request.withCredentials = true;
    }

    // Add responseType to request if needed
    if (config.responseType) {
      try {
        request.responseType = config.responseType;
      } catch (e) {
        // Expected DOMException thrown by browsers not compatible XMLHttpRequest Level 2.
        // But, this can be suppressed for 'json' type as it can be parsed by default 'transformResponse' function.
        if (config.responseType !== 'json') {
          throw e;
        }
      }
    }

    // Handle progress if needed
    if (typeof config.onDownloadProgress === 'function') {
      request.addEventListener('progress', config.onDownloadProgress);
    }

    // Not all browsers support upload events
    if (typeof config.onUploadProgress === 'function' && request.upload) {
      request.upload.addEventListener('progress', config.onUploadProgress);
    }

    if (config.cancelToken) {
      // Handle cancellation
      config.cancelToken.promise.then(function onCanceled(cancel) {
        if (!request) {
          return;
        }

        request.abort();
        reject(cancel);
        // Clean up request
        request = null;
      });
    }

    if (requestData === undefined) {
      requestData = null;
    }

    // Send the request
    request.send(requestData);
  });
};

/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(3)))

/***/ }),

/***/ 9:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var enhanceError = __webpack_require__(18);

/**
 * Create an Error with the specified message, config, error code, request and response.
 *
 * @param {string} message The error message.
 * @param {Object} config The config.
 * @param {string} [code] The error code (for example, 'ECONNABORTED').
 * @param {Object} [request] The request.
 * @param {Object} [response] The response.
 * @returns {Error} The created error.
 */
module.exports = function createError(message, config, code, request, response) {
  var error = new Error(message);
  return enhanceError(error, config, code, request, response);
};


/***/ })

/******/ });
//# sourceMappingURL=tournament.js.map