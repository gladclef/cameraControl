var canvas;
var crosshairs;
var windowFocus = true;
var mouseDown;
var incomingMessenger;
var outgoingMessenger;

if (window.a_toExec === undefined) window.a_toExec = [];

function initWatchers()
{
	// from http://stackoverflow.com/questions/3479734/javascript-jquery-test-if-window-has-focus
	$(window).focus(function() {
		windowFocus = true;
		console.log("windowFocus: " + windowFocus);
	}).blur(function() {
		windowFocus = false;
		console.log("windowFocus: " + windowFocus);
	});

	$(window).mousedown(function() {
		mouseDown = true;
		console.log("mouseDown: " + mouseDown);
	}).mouseup(function() {
		mouseDown = false;
		console.log("mouseDown: " + mouseDown);
	});
}

function createCrosshairsImage()
{
	var size = (canvas.width() + canvas.height()) / 2 / 5;
	size += "px";

	// from http://stackoverflow.com/questions/17634019/javascript-load-an-image-from-url-and-display
	var img = $('<img />', {
		src: 'images/crosshairs.png',
		width: size,
		height: size
	});
	img.appendTo($("body"));
	return img;
}

function initCanvas()
{
	canvas = $("#canvas_container");

	// get the desired width and height to fill the screen
	var w = parseInt($(window).width());
	var h = parseInt($(window).height());

	// set the canvas size
	canvas.css({
		"width": w + "px",
		"height": h + "px"
	});
	$("body").css({
		"overflow": "hidden"
	})

	// set the canvase style
	canvas.css({
		"background-color": "rgb(200, 200, 200)",
		"margin": "0 auto",
		"position": "fixed",
		"left": 0,
		"top": 0
	});
}

function initCrosshairs()
{
	var img = createCrosshairsImage();

	crosshairs = {
		pan: serverStats["pan"] + 0,
		tilt: serverStats["tilt"] + 0,
		remotePan: 0,
		remoteTilt: 0,
		getImg: function() {
			return img;
		},
		getX: function(pan) {
			var ratio = canvas.width() / serverStats["pan_range"] / 2;
			var offset = canvas.width() / 2;
			return offset + ratio * pan;
		},
		getY: function(tilt) {
			var ratio = canvas.height() / serverStats["tilt_range"] / 2;
			var offset = canvas.height() / 2;
			return offset + ratio * tilt;
		},
		updateImagePosition: function() {
			img.css({
				left: (crosshairs.getX(crosshairs.pan) - img.width() / 2) + "px",
				top: (crosshairs.getY(crosshairs.tilt) - img.height() / 2) + "px",
				position: "fixed",
    			"pointer-events": "none"
			});
		},
		updatePanTiltByPixel: function(x, y) {
			var ratioX = canvas.width() / serverStats["pan_range"] / 2;
			var offsetX = canvas.width() / 2;
			crosshairs.pan = Math.floor((x - offsetX) / ratioX);
			var ratioY = canvas.height() / serverStats["tilt_range"] / 2;
			var offsetY = canvas.height() / 2;
			crosshairs.tilt = Math.floor((y - offsetY) / ratioY);
		},
		updateRemoteCrosshairs: function(remotePan, remoteTilt) {
			crosshairs.remotePan = remotePan;
			crosshairs.remoteTilt = remoteTilt;
			var imgSize = img.width() / 2;

			var lines = d3.select("#canvas_container").selectAll("line").data([false, true]);
			lines = lines.enter().append("line").merge(lines);
			lines.attr("x1", function(vert) { return crosshairs.getX(remotePan) - (vert?0:imgSize); })
				.attr("y1", function(vert) { return crosshairs.getY(remoteTilt) - (vert?imgSize:0); })
				.attr("x2", function(vert) { return crosshairs.getX(remotePan) + (vert?0:imgSize); })
				.attr("y2", function(vert) { return crosshairs.getY(remoteTilt) + (vert?imgSize:0); })
				.attr("stroke", "black")
				.attr("stroke-width", "1")
				.attr("pointer-events", "none")
		}
	};

	crosshairs.updateImagePosition();
}

function update(e)
{
	var x = e.clientX || e.pageX;
	var y = e.clientY || e.pageY;
	crosshairs.updatePanTiltByPixel(x, y);
	crosshairs.updateImagePosition();
	crosshairs.updateRemoteCrosshairs(serverStats["remotePan"], serverStats["remoteTilt"]);
}

function localUpdate(e)
{
	update(e);
	outgoingMessenger.changed(crosshairs.pan, crosshairs.tilt);
}

function initIncomingMessenger()
{
	incomingMessenger = function(pan, tilt, remote)
	{
		if (remote)
		{
			serverStats["remotePan"] = pan;
			serverStats["remoteTilt"] = tilt;
			update({
				clientX: crosshairs.getX(crosshairs.pan),
				clientY: crosshairs.getY(crosshairs.tilt)
			});
		}
		else
		{
			serverStats["pan"] = pan;
			serverStats["tilt"] = tilt;
			update({
				clientX: crosshairs.getX(pan),
				clientY: crosshairs.getY(tilt)
			});
		}
	}	
}

function initOutgoingMessenger()
{
	outgoingMessenger = {};
}

a_toExec[a_toExec.length] = {
	"name": "main",
	"dependencies": ["serverStats", "jQuery", "communication_websocket"],
	"function": function() {
		initCanvas();
		initCrosshairs();
		initWatchers();
		initIncomingMessenger();
		initOutgoingMessenger();

		initWebsocketConnection(incomingMessenger, outgoingMessenger);

		canvas.click(function(e) {
			localUpdate(e);
		});
		canvas.mousemove(function(e) {
			if (windowFocus && mouseDown) {
				localUpdate(e);
			}
		});
		canvas[0].addEventListener("touchmove", (function(e) {
			if (windowFocus) {
				e = e.originalEvent || e;
				e = e.targetTouches || e.changedTouches || e.touches || e;
				e = e[0] || e["0"] || e;
				localUpdate(e);
			}
		}), false);
	}
}