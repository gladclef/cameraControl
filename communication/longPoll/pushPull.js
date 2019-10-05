window["pushPull.js"] = true;

function initPushPull(onmessage, updateListenerObj, onerror, onclose)
{
	//create a new WebSocket object.
	var addr = "https://bbean.us/small/cameraControl/communication/longPoll/server.php";
	var myId = Math.floor(Math.random() * 10000);
	var lastSendTime = 0;
	var index = parseInt(serverStats['message_idx']);
	var sendRate = 50;
	var delayedUpdated = null;
	var pollXhrs = [];
	var pushTimer = null;
	var pushVals = {};
	var startTime = Date.now();

	window.addEventListener("beforeunload", function (e) {
		for (var i = 0; i < pollXhrs.length; i++) {
			if (pollXhrs[i] !== null) {
				pollXhrs[i].abort(); // todo
			}
		}
	});

	pushData = function()
	{
		pushTimer = null;
		$.ajax({
			url: addr,
			async: true,
			cache: false,
			data: pushVals,
			type: "POST",
			timeout: 10000,
			success: function(data) {
				if (data == "success") {
					// console.log("remote position updated");
				} else {
					console.error("Error! " + data);
				}
			},
			error: function(xhr, ajaxOptions, thrownError) {
				if (parseInt(xhr.status) == 0 && thrownError) {
					if ((thrownError+"").indexOf("NETWORK_ERR") > -1) {
						console.error("network error encountered");
						return;
					}
				}
				console.error("Error sending request: ("+xhr.status+") "+thrownError);
			}
		});
	};

	schedulePushData = function(data)
	{
		if (pushTimer === null)
		{
			pushTimer = setTimeout(pushData, 200);
		}
		pushVals = data;
	};

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
		index += 1;
		var data = {
			command: "setPanTilt",
			pan: pan,
			tilt: tilt,
			camera: "Derek DnD",
			remote : false,
			clientId: myId,
			message_idx : index
		};

		//convert and send data to server
		schedulePushData(data);
	};
	
	var parseData = function(msg) {
		var msg = JSON.parse(msg); //PHP sends Json data
		var pan = msg.pan;
		var tilt = msg.tilt;
		var remote = msg.remote;
		var message_idx = msg.message_idx;
		var clientId = msg.clientId;

		if (clientId == myId)
		{
			return;
		}
		if (message_idx <= index)
		{
			return;
		}
		index = message_idx;

		onmessage(pan, tilt, remote);
	};
	
	var pollData = null;
	pollData = function() {
		if (pollXhrs.length < 1 || pollXhrs[0] == null) {

			//prepare json data
			var data = {
				command: "subscribePanTilt",
				camera: "Derek DnD",
				clientId: myId,
				lastMessageId: index
			};

			// send ajax request
			var jqXHR = $.ajax({
				url: addr,
				async: true,
				cache: false,
				data: data,
				type: "POST",
				timeout: 60000,
				success: function(data) {
					pollXhrs[0] = null;
					parseData(data);
				},
				error: function(xhr, ajaxOptions, thrownError) {
					pollXhrs[0] = null;
					if (parseInt(xhr.status) == 0 && thrownError) {
						if ((thrownError+"").indexOf("NETWORK_ERR") > -1) {
							console.error("network error encountered");
							return;
						}
					}
					console.error("Error sending request: ("+xhr.status+") "+thrownError);
				}
			});
			pollXhrs[0] = jqXHR;
		}
	};
	setInterval(pollData, 10);
}