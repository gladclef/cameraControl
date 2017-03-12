/**
 * Much of this code comes from the chat server created by sanwebe:
 * https://www.sanwebe.com/downloads/50-websocket-example
 */

function initWebsocketConnection(onmessage, updateListenerObj, onopen, onerror, onclose)
{
	//create a new WebSocket object.
	var wsUri = "ws://bbean.us:9000/demo/server.php"; 	
	websocket = new WebSocket(wsUri); 
	
	if (onopen)
	{
		websocket.onopen = onopen;
	}

	updateListenerObj.changed = function(pan, tilt)
	{
		//prepare json data
		var msg = {
			pan: pan,
			tilt: tilt,
			remote : false
		};
		//convert and send data to server
		websocket.send(JSON.stringify(msg));
	};
	
	//#### Message received from server?
	websocket.onmessage = function(ev) {
		var msg = JSON.parse(ev.data); //PHP sends Json data
		var pan = msg.pan;
		var tilt = msg.tilt;
		var remote = msg.remote;

		onmessage(pan, tilt, remote);
	};
	
	websocket.onerror	= function(ev) {
		if (onerror) {
			onerror(ev);
		} else {
			window.alert("communication error");
			window.alert(ev);
		}
	}
	websocket.onclose 	= function(ev) {
		if (onclose) {
			onclose(ev);
		} else {
			window.alert("websocket closed");
			window.alert(ev);
		}
	}
}