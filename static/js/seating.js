function checkPlan(max_rows) {
    var vals = $("ul[id*=col]");
    for(i = 0;i<vals.length;i++) {
        if ($('#'+vals[i].id+' li').length > max_cols) {
            alert('All columns must be shorter than '+max_cols);
            return false;
        }
    }
    return true;
}

var DocPos = {
	// Calculates the top-left (TL) coordinates of an element, relative to the page.
	fromElementTL : function(element) {
		var x = element.offsetLeft;
		var y = element.offsetTop;
		
		var parent = element.offsetParent;
		while(parent) {
			x = x + parent.offsetLeft;
			y = y + parent.offsetTop;
			parent = parent.offsetParent;
		}
		return new Point( x, y );
	},
	
	// Calculates the bottom-right (BR) coordinates of an element, relative to the page.
	fromElementBR : function(element) {
		var x = element.offsetWidth;
		var y = element.offsetHeight;
		
		var parent = element;
		while(parent) {
			x = x + parent.offsetLeft;
			y = y + parent.offsetTop;
			parent = parent.offsetParent;
		}
		return new Point( x, y );
	},
	
	// Calculates the position of the mouse, from an event, relative to the page.
	fromMouse : function(event) {
		var cx = event.pageX || (event.clientX + document.body.parentNode.scrollLeft + document.body.scrollLeft);
		var cy = event.pageY || (event.clientY + document.body.parentNode.scrollTop  + document.body.scrollTop );
		return new Point(cx, cy);
	}
};

// A simple (x, y) point representation with some operators.
function Point (x, y) {
	this.x = isNaN(x) ? 0 : x;
	this.y = isNaN(y) ? 0 : y;
}

Point.prototype.add = function( add ) {
	return new Point(this.x + add.x, this.y + add.y);
}

Point.prototype.subtract = function( subtract ) {
	return new Point(this.x - subtract.x, this.y - subtract.y);
}

var Seating = {
	// Add the container to our list of containers, then initialise objects.
	initialiseContainer : function(cont) {
		if (typeof this.allowEdit == "undefined") {
			this.allowEdit = !!document.getElementById('order');
		}
		
		// Remove whitespace nodes of suck.
		for (var i = 0; i < cont.childNodes.length; i++) {
			if (cont.childNodes[i].nodeType != 1) {
				cont.childNodes[i].parentNode.removeChild(cont.childNodes[i]);
				i--;
			}
		}
		
		// Flag this element as a container, so we know it is OK to use later.
		cont.container = true;
		
		// Insert a marker at the end of the container; initialiseElement will
		// insert one before each item, this making the pattern correct.
		cont.appendChild(this.createMarker());
		var items = cont.getElementsByTagName("li");
		for (var i = 0; i < items.length; i++) {
			Seating.initialiseElement(items[i]);
		}
	},
	
	// Set up events on this element to init drag and drop.
	initialiseElement : function(element) {
		// Wrap the contents of element so we have:
		// <table class="seating_item"><tbody><tr><td><element/></td></tr></tbody></table>
		// (The <tbody> is needed or we screw up in at least IE.)
		
		var wrapTable = document.createElement("table");
		var wrapTBody = document.createElement("tbody");
		var wrapTR = document.createElement("tr");
		var wrapTD = document.createElement("td");
		wrapTable.className = "seating_item";
		wrapTable.border = 0;
		wrapTable.cellPadding = 0;
		wrapTable.cellSpacing = 0;
		while (element.firstChild) {
			wrapTD.appendChild(element.firstChild);
		}
		wrapTR.appendChild(wrapTD);
		wrapTBody.appendChild(wrapTR);
		wrapTable.appendChild(wrapTBody);
		element.appendChild(wrapTable);
		element.className += " seating_item";
		if (this.allowEdit) {
			element.className += " allow_edit";
			element.onmousedown = Seating.elementOnMouseDown;
		}
		
		// Place a marker before the item; see comment in initialiseContainer.
		element.parentNode.insertBefore(this.createMarker(), element);
	},
	
	createMarker : function() {
		var marker = document.createElement("div");
		marker.className = "marker";
		return marker;
	},
	
	// Stores the element being dragged.
	dragging : null,
	// Stores data on the current drop target. See updateDropMarker and cleareDropMarker.
	dropOn : null,
	// Stores the mouse position when dragging started.
	offset : null,
	
	// This is the mousedown event of an element. It starts the drag+drop.
	elementOnMouseDown : function (event) {
		var mousepos = DocPos.fromMouse(event || window.event);
		var pos = DocPos.fromElementTL(this);
		Seating.offset = mousepos;
		Seating.dragging = this;
		Seating.dragging.className += " seating_moving";
		
		document.onmousemove = Seating.documentOnMouseMove;
		document.onmouseup = Seating.documentOnMouseUp;
		return false;
	},

	// This is the handler while dragging.
	documentOnMouseMove : function (event) {
		var mousepos = DocPos.fromMouse(event || window.event);
		var obj = Seating.dragging;
		var offset = Seating.offset;
		var newPos = mousepos.subtract(offset);
		
		// Move the dragged element to its new position.
		obj.style["left"] = newPos.x + "px";
		obj.style["top"] = newPos.y + "px";
		
		Seating.updateDropMarker(event);
		return false;
	},
	
	documentOnMouseUp : function (event) {
		var obj = Seating.dragging;
		var marker = obj.previousSibling;
		
		// Check if we're an empty item or we're from the empty list.
		var emptyItem = obj.className.match(/empty/i);
		
		if (obj.parentNode.id == "unassigned_empty") {
			// We are being dragged FROM the empty container, so create a new
			// empty item to replace it.
			var clone = obj.cloneNode(true);
			clone.className = clone.className.replace(/ ?seating_moving/i, "");
			clone.style["left"] = "";
			clone.style["top"] = "";
			clone.onmousedown = Seating.elementOnMouseDown;
		}
		
		document.onmousemove = null;
		document.onmouseup = null;
		Seating.clearDropMarker();
		
		// Get drop location.
		var dropOn = Seating.calculateDropElement(event);
		if (dropOn) {
			if (dropOn.node) {
				if (dropOn.before) {
					// Use other marker for this case, or we mess up dropping on
					// ourselves (yeah, I know).
					marker = obj.nextSibling;
					
					dropOn.node.parentNode.insertBefore(obj, dropOn.node);
					dropOn.node.parentNode.insertBefore(marker, dropOn.node);
				} else {
					dropOn.node.parentNode.insertBefore(obj, dropOn.node.nextSibling);
					dropOn.node.parentNode.insertBefore(marker, dropOn.node.nextSibling);
				}
			} else {
				dropOn.marker.parentNode.appendChild(obj);
				dropOn.marker.parentNode.appendChild(marker);
			}
		} else {
			if (emptyItem) {
				// Empty item dropped outside == death.
				obj.parentNode.removeChild(obj.nextSibling);
				obj.parentNode.removeChild(obj);
			} else {
				var unassignedList = document.getElementById("unassigned");
				unassignedList.appendChild(obj);
				unassignedList.appendChild(marker);
			}
		}
		
		if (clone) {
			// We've got a clone waiting to go in to the empty list, so put
			// it in. We don't insert it earlier as that would mess up
			// calculateDropElement.
			var emptyList = document.getElementById("unassigned_empty");
			emptyList.appendChild(clone);
			emptyList.appendChild(Seating.createMarker());
		}
		
		// Clear object's dragging flags.
		obj.className = obj.className.replace(/ ?seating_moving/i, "");
		obj.style["left"] = "";
		obj.style["top"] = "";
		
		// Now serialise the data...
		var data = "";
		var items = document.getElementsByTagName("ul");
		for (var i = 0; i < items.length; i++) {
			if (items[i].container == null) continue;
			if (items[i].id == "unassigned_empty") continue;
			data = data + items[i].id + "(";
			var sibling = items[i].firstChild;
			while(sibling != null) {
				if (sibling.nodeName.toLowerCase() != "li") {
					sibling = sibling.nextSibling;
					continue;
				}
				data += sibling.id + ",";
				sibling = sibling.nextSibling;
			}
			data += ");";
		}
		document.getElementById('order').value = data;
	},
	
	// Reposition the drop-marker if appropriate.
	updateDropMarker : function (event) {
		var dropOn = this.calculateDropElement(event);
		
		// If the same marker is involved previous and now, don't do anything.
		if (dropOn && this.dropOn && (dropOn.marker == this.dropOn.marker)) {
			return;
		}
		
		// Update drop marker, so we show the correct place it'll insert.
		this.clearDropMarker();
		this.dropOn = dropOn;
		if (dropOn) {
			dropOn.marker.className += " insert";
		}
	},
	
	// Remove all traces of the drop-marker.
	clearDropMarker : function() {
		if (!this.dropOn) {
			return;
		}
		
		var marker = this.dropOn.marker;
		marker.className = marker.className.replace(/ ?insert/i, "");
		
		this.dropOn = null;
	},

    fillOrderField : function () {
		// Now serialise the data...
		var data = "";
		var items = document.getElementsByTagName("ul");
		for (var i = 0; i < items.length; i++) {
			if (items[i].container == null) continue;
			if (items[i].id == "unassigned_empty") continue;
			data = data + items[i].id + "(";
			var sibling = items[i].firstChild;
			while(sibling != null) {
				if (sibling.nodeName.toLowerCase() != "li") {
					sibling = sibling.nextSibling;
					continue;
				}
				data += sibling.id + ",";
				sibling = sibling.nextSibling;
			}
			data += ");";
		}
		document.getElementById('order').value = data;
    },
	
	// Calculates the element being dropped on, and whether to insert above or below it.
	calculateDropElement : function (event) {
		var mousepos = DocPos.fromMouse(event || window.event);
		
		var emptyItem = this.dragging.className.match(/empty/i);
		
		var items = document.getElementsByTagName("ul");
		for (var i = 0; i < items.length; i++) {
			// Don't drop on anything we're not managing.
			if (items[i].container == null) continue;
			// Don't drop anything on the empty spawn point.
			if (items[i].id == "unassigned_empty") continue;
			// Don't drop (empty) items on the unassigned list.
			if (emptyItem && (items[i].id == "unassigned")) continue;
			var tl = DocPos.fromElementTL(items[i]);
			var br = DocPos.fromElementBR(items[i]);
			
			if ((mousepos.x < tl.x) || (mousepos.x > br.x) || (mousepos.y < tl.y) || (mousepos.y > br.y)) {
				// Not inside column, next!
				continue;
			}
			
			// Inside bounds of this column.
			var sibling = items[i].firstChild;
			var lastMarker = null;
			while (sibling) {
				if (sibling.nodeName.toLowerCase() == "div") {
					lastMarker = sibling;
				}
				if (sibling.nodeName.toLowerCase() != "li") {
					sibling = sibling.nextSibling;
					continue;
				}
				var tl2 = DocPos.fromElementTL(sibling);
				var br2 = DocPos.fromElementBR(sibling);
				
				// If the mouse is above the bottom of this item, and it's not
				// the moving item, use it as the drop point.
				if ((mousepos.y <= br2.y) && !(sibling.className.match(/seating_moving/i))) {
					var before = ((mousepos.y - tl2.y) / (br2.y - tl2.y)) < 0.5;
					var marker = (before ? sibling.previousSibling : sibling.nextSibling);
					return { node: sibling, marker: marker, before: before };
				}
				sibling = sibling.nextSibling;
			}
			return { node: null, marker: lastMarker, before: false };
		}
		return null;
	}
}


