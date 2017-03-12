/**
 * Much of this code comes from the chat server created by sanwebe:
 * https://www.sanwebe.com/downloads/50-websocket-example
 */

function initWebsocketConnection(onmessage, updateListenerObj, onopen, onerror, onclose)
{
	//create a new WebSocket object.
	var wsUri = "ws://bbean.us:8080"; 	
	websocket = new WebSocket(wsUri);
	var myId = Math.floor(Math.random() * 10000);
	var lastSendTime = 0;
	var index = 0;
	var sendRate = 50;
	var delayedUpdated = null;
	
	if (onopen)
	{
		websocket.onopen = onopen;
	}

	window.addEventListener("beforeunload", function (e) {
		websocket.close(1000, "window close");
	});

	updateListenerObj.changed = function(pan, tilt)
	{
		// create a new random message id
		
		var time = (new Date()).getTime();
		if (time - lastSendTime < sendRate)
		{
			clearTimeout(delayedUpdated);
			delayedUpdated = setTimeout(function() {
				updateListenerObj.changed(pan, tilt);
			});
			return;
		}
		lastSendTime = time;

		//prepare json data
		var msg = {
			pan: pan,
			tilt: tilt,
			remote : false,
			clientId: myId,
			messageIndex : index
		};
		index += 1;
		//convert and send data to server
		var data = JSON.stringify(msg);
		console.log(data);
		websocket.send(data);
	};
	
	//#### Message received from server?
	websocket.onmessage = function(ev) {
		var msg = JSON.parse(ev.data); //PHP sends Json data
		var pan = msg.pan;
		var tilt = msg.tilt;
		var remote = msg.remote;
		var messageIndex = msg.messageIndex;
		var clientId = msg.clientId;

		if (clientId == myId)
		{
			return;
		}

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