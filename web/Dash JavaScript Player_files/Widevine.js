/**
 * The copyright in this software is being made available under the BSD License,
 * included below. This software may be subject to other third party and contributor
 * rights, including patent rights, and no such rights are granted under this license.
 *
 * Copyright (c) 2013, Dash Industry Forum.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 *  * Redistributions of source code must retain the above copyright notice, this
 *  list of conditions and the following disclaimer.
 *  * Redistributions in binary form must reproduce the above copyright notice,
 *  this list of conditions and the following disclaimer in the documentation and/or
 *  other materials provided with the distribution.
 *  * Neither the name of Dash Industry Forum nor the names of its
 *  contributors may be used to endorse or promote products derived from this software
 *  without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS AS IS AND ANY
 *  EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 *  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 *  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
 *  INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 *  NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 *  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 *  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 *  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 *  POSSIBILITY OF SUCH DAMAGE.
 */

MediaPlayer.dependencies.protection.servers.Widevine = function() {
    "use strict";

    return {

        /**
         * Returns a new or updated license server URL based on information
         * found in the CDM message
         *
         * @param url the initially established URL (from ProtectionData or initData)
         * @param message the CDM message
         * @returns {string} the URL to use in license requests
         */
        getServerURLFromMessage: function(url /*, message*/) { return url; },

        /**
         * Returns the HTTP method to be used (i.e. "GET", "POST", etc.) in
         * XMLHttpRequest.open().
         *
         * @returns {string} the HTTP method
         */
        getHTTPMethod: function() { return 'POST'; },


        /**
         * Returns the response type to set for XMLHttpRequest.responseType
         *
         * @returns {string} the response type
         */
        getResponseType: function(/*keySystemStr*/) { return 'arraybuffer'; },

        /**
         * Parses the license server response to retrieve the message intended for
         * the CDM.
         *
         * @param serverResponse the response as returned in XMLHttpRequest.response
         * @returns {Uint8Array} message that will be sent to the CDM
         */
        getLicenseMessage: function(serverResponse/*, keySystemStr*/) {
            return new Uint8Array(serverResponse);
        },

        /**
         * Parses the license server response during error conditions and returns a
         * string to display for debugging purposes
         *
         * @param serverResponse the server response
         */
        getErrorResponse: function(serverResponse/*, keySystemStr*/) {
            return String.fromCharCode.apply(null, new Uint8Array(serverResponse));
        }
    };
};

MediaPlayer.dependencies.protection.servers.Widevine.prototype = {
    constructor: MediaPlayer.dependencies.protection.servers.Widevine
};
